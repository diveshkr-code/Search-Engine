# helper function  
#    input: url
#    output: HTML content of that url
def get_page(url):
    try:
        import urllib.request
        # python3 has urllib.request whereas python2 works with only urllib
        return urllib.request.urlopen(url).read()
    except:
        return "Error with Loading the page"

#print(get_page('https://www.google.com/'))
