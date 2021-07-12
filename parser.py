import re
from urllib.parse import unquote


def has_tag(url):
    and_tag = re.compile('&[\D]+=')  # https://webapps.stackexchange.com/questions/9863/are-the-parameters-for-www-youtube-com-watch-documented
    match = and_tag.search(url)  # check '&' before '?' due to Youtube
    if not re.compile('youtube.com(/|((%2)F))watch').search(url):  # need whitelist of URLs, n.b. Youtube channels can have '?' tags, see https://stackoverflow.com/questions/6259443/how-to-match-a-line-not-containing-a-word
        general_tag = re.compile('\?|((%3)F)')  # most sites use '?' or %3F (separate %3 and F due to python string format)
        match = general_tag.search(url)
    return match


def delete_tag(url):
    and_tag = re.compile('&[\D]+=(.+)')
    url = re.sub(and_tag, '', url)
    if not re.compile('youtube.com(/|((%2)F))watch').search(url):
        general_tag = re.compile('(\?|((%3)F))(.+)')
        url = re.sub(general_tag, '', url)
    return url


def is_redirect(url):
    url_tag = re.compile('(=|(%3D))http')  # Google uses /url?...=http, Facebook uses ?u=http, others use ?url=http  (see https://nakedsecurity.sophos.com/2020/05/15/how-scammers-abuse-google-searchs-open-redirect-feature/, https://web.archive.org/web/20110817024348/http://blog.anta.net/2009/01/29/509/)
    match = url_tag.search(url)
    return match


def extract_redirect(url):
    url = re.sub('(.+)(=|(%3D))http', 'http', url)
    return url


def is_amp(url):
    # Types of AMP links https://searchengineland.com/amp-links-large-281987
    amp = re.compile('(cdn\.ampproject\.org)|(//amp.)|(/amp/?$)')  # /amp includes also amp. since it's usually https://amp.domain.tld/whatever
    match = amp.search(url)
    return match


def delele_amp(url):
    cache_amp = re.compile('(.+)cdn\.ampproject\.org/(c/)?(s/)?')
    google_amp = re.compile('(.+)google\.(\w)+/amp/(s/)?')  # Sometimes the s does not appear in google.com/amp/s/domain.tld/whatever
    origin_amp_prepended = re.compile('(.+)amp\.')
    origin_amp_appended = re.compile('/amp(/)?$')  # end slash optional, $ means end of string
    
    for amp in [cache_amp, google_amp, origin_amp_prepended, origin_amp_appended]:
        url = re.sub(amp, '', url)
    if not re.match('http', url):  # re.match() only matches beginning of string
        url = 'https://' + url
    return url


def in_unicode(url):
    return re.compile('(%\w)+').search(url)


def decode_unicode(url):
    return unquote(url)


def parser(url):
    if is_redirect(url):
        url = extract_redirect(url)
    if is_amp(url):
        url = delele_amp(url)
    if has_tag(url):
        url = delete_tag(url)
    if in_unicode(url):  # if before delete_tag, saves the 'or' in tags & redirects but might be slower (need to test this)
        url = decode_unicode(url)
    # force https?
    return url
