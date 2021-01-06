# url-notag
Remove tracking redirects/tags from URLs using regular expressions. Requires only Python built-in modules `re` and `urllib`. App usable in command-line.

## Will break:
* Sharing links, as in facebook.com/share.php?u=https%3A%2F%2Fmydomain.com
* Redirect after registration/sign-in links
* Other links containing useful tags that make use of '?' or '&', e.g.
    * economist.com/api/my-account?newsletter=1&auth=1
    * Youtube playlist tag (see also https://webapps.stackexchange.com/questions/9863/are-the-parameters-for-www-youtube-com-watch-documented)
    * duckduckgo.com/?q=mysearchstring

## Ideas/To-do:
* Use https (check if connection possible)
* Implement as chatbot or browser plugin 
   * Fix above broken link cases
   * Domain whitelist function
