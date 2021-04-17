import re
from urllib.parse import unquote


def has_tag(url):
    matches = []
    
    and_tag = re.compile('&[\D]+=.+')  # https://webapps.stackexchange.com/questions/9863/are-the-parameters-for-www-youtube-com-watch-documented
    matches.append(and_tag.search(url))  # check '&' before '?' due to Youtube
    
    if not re.compile('youtube.com/watch').search(url):  # make whitelist of URLs, n.b. Youtube channels can have '?' tags, see https://stackoverflow.com/questions/6259443/how-to-match-a-line-not-containing-a-word
        general_tag = re.compile('\?|((%3)F)')  # most sites use '?' or %3F (separate %3 and F due to python string format)
        matches.append(general_tag.search(url))
    
    indices = [m.span()[0] for m in matches if m is not None]
    return indices


def delete_tag(url, indices):
    end = min(indices)
    return url[:end]


def is_redirect(url):
    url_tag = re.compile('[=|(%3D)]http')  # Google uses /url?...=http, Facebook uses ?u=http, others use ?url=http  (see https://nakedsecurity.sophos.com/2020/05/15/how-scammers-abuse-google-searchs-open-redirect-feature/, https://web.archive.org/web/20110817024348/http://blog.anta.net/2009/01/29/509/)
    match = url_tag.search(url)
    return match


def extract_redirect(url):
    start = re.compile('[=|(%3D)]http').search(url).span()[0] + 1  # span gives the start,end tuple. +1 to slice from http, not =http
    return url[start:]

def is_amp(url):
    # https://medium.com/@danbuben/why-amp-is-bad-for-your-site-and-for-the-web-e4d060a4ff31
    # Types of AMP links https://searchengineland.com/amp-links-large-281987
    amp = re.compile('(cdn\.ampproject\.org)|(/amp)')  # /amp includes also amp. since it's usually https://amp.domain.tld/whatever
    match = amp.search(url)
    return match

def delele_amp(url):
    cache_amp = re.compile('cdn\.ampproject\.org/(c/)?')
    google_amp = re.compile('google\.(\w)+/amp/(s/)?')  # Sometimes the s does not appear in google.com/amp/s/domain.tld/whatever
    origin_amp_prepended = re.compile('amp\.')
    
    indices = []
    for amp in [cache_amp, google_amp, origin_amp_prepended]:  # all are prepended tags
        match = amp.search(url)
        if match:
            indices.append(match.span()[-1])
    url = url[max(indices):]

    origin_amp_appended = re.compile('/amp(\w)+/?$')  # \w ensures no symbols like dots and dash, end slash optional, $ means end of string
    match = origin_amp_appended.search(url)
    if match:
        end = match.span()[0]
    else:
        end = None
    return 'https://' + url[:end]


def in_unicode(url):
    return re.compile('(%\w)+').search(url)


def decode_unicode(url):
    return unquote(url)


def parser(url):
    if is_redirect(url):
        url = extract_redirect(url)
    if is_amp(url):
        url = delele_amp(url)

    tag_indices = has_tag(url)
    if tag_indices:
        url = delete_tag(url, tag_indices)

    if in_unicode(url):  # if decode first, saves the 'or' in tags & redirects but might be slower
        url = decode_unicode(url)
    # force https?
    return url
