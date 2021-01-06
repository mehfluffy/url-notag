# url-notag
Clean URLs of tracking redirects and tags, using regular expressions. Requires only Python built-in modules `re` and `urllib`. App usable in command-line.

## Will break:
* Sharing links
* Redirect after registration links
* Links containing useful tags that make use of '?' or '&', e.g.
    * https://www.economist.com/api/my-account?newsletter=1&auth=1
    * Youtube playlist tag

## Ideas:
* Domain whitelist function
* Force https option
* Implement as chatbot or browser plugin