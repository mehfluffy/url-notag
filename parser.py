import re
from urllib.parse import unquote


def has_tag(url):
    matches = []
    
    and_tag = re.compile('&[\D]+=.+')  # https://webapps.stackexchange.com/questions/9863/are-the-parameters-for-www-youtube-com-watch-documented
    matches.append(and_tag.search(url))  # check '&' before '?' due to Youtube
    
    if not re.compile('youtube.com/watch').search(url):  # make whitelist of URLs, n.b. Youtube channels can have '?' tags, see https://stackoverflow.com/questions/6259443/how-to-match-a-line-not-containing-a-word
        general_tag = re.compile('\?|((%3)F)')  # most sites use '?' or %3F (separate 3 and F due to python string formatting)
        matches.append(general_tag.search(url))
    
    indices = [m.span()[0] for m in matches if m is not None]
    return indices


def delete_tag(url, indices):
    end = min(indices)
    return url[:end]


def is_redirect(url):
    url_tag = re.compile('u.*[=|(%3D)]http')  # Google uses /url?...=http, Facebook uses ?u=http, others use ?url=http  (see https://nakedsecurity.sophos.com/2020/05/15/how-scammers-abuse-google-searchs-open-redirect-feature/, https://web.archive.org/web/20110817024348/http://blog.anta.net/2009/01/29/509/)
    match = url_tag.search(url)
    return match


def extract_redirect(url):
    start = re.compile('[=|(%3D)]http').search(url).span()[0] + 1
    return url[start:]


def in_unicode(url):
    return re.compile(r'(%\w)+').search(url)


def decode_url(url):
    return unquote(url)


def parser(url):
    if is_redirect(url):
        url = extract_redirect(url)
    tag_indices = has_tag(url)
    if tag_indices:
        url = delete_tag(url, tag_indices)
    if in_unicode(url):  # if decode first, saves regex 'or' but might be slower
        url = decode_url(url)
    # force https?
    return url
