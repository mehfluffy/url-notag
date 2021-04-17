# url-notag
Clean URLs of tracking redirects and tags, using regular expressions. Requires only Python built-in modules `re` and `urllib`. App usable in command-line.

## Will break:
* Sharing links
* Redirect after registration links
* Links containing useful tags that make use of '?' or '&', e.g.
    * economist.com/api/my-account?newsletter=1&auth=1
    * Youtube playlist tag (see also https://webapps.stackexchange.com/questions/9863/are-the-parameters-for-www-youtube-com-watch-documented)
    * duckduckgo.com/?q=mysearchstring
* Google AMP links that have been shortened, e.g. 
    * https://amp.abc.net.au/article/100063916 because https://www.abc.net.au/article/100063916 is not the original page, but rather https://www.abc.net.au/news/2021-04-15/australian-based-uyghurs-on-chinese-blacklist/100063916

## Ideas:
* Domain whitelist function
* Force https option
* Mailing list click-tracking links usually don't have tags, just one big hash
* Implement as chatbot or browser plugin
