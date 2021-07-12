# url-notag
Remove tracking redirects/tags from URLs, changes it to lead to the non-[AMP](https://medium.com/@danbuben/why-amp-is-bad-for-your-site-and-for-the-web-e4d060a4ff31) (i.e. original) version of the webpage, and decodes unicode (e.g. for Chinese characters) within the URL. Requires only Python built-in modules `re` and `urllib`. App usable in command-line (use the `python3` command).

## Will break:
* Sharing links, as in facebook.com/share.php?u=https%3A%2F%2Fmydomain.com
* Redirect after registration/sign-in links
* Other links containing useful tags that make use of '?' or '&', e.g.
    * https://economist.com/api/my-account?newsletter=1&auth=1
    * Youtube playlist tag (see also https://webapps.stackexchange.com/questions/9863/are-the-parameters-for-www-youtube-com-watch-documented)
    * duckduckgo.com/?q=mysearchstring
* AMP links that have been shortened, e.g. 
    * https://amp.abc.net.au/article/100063916 will be broken, because it gets parsed into https://www.abc.net.au/article/100063916 which is not the original page. The original is instead https://www.abc.net.au/news/2021-04-15/australian-based-uyghurs-on-chinese-blacklist/100063916

## Ideas:
* Domain whitelist function (can serve as workaround for broken links)
* Force https option
* Mailing list click-tracking links usually don't have tags, just one big hash
* Implement as chatbot or browser plugin
* Automated testing using URLs scraped from webpages ([beautiful soup](https://beautiful-soup-4.readthedocs.io/en/latest/))
* Detect broken links
