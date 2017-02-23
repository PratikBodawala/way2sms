import getpass
import urllib

import requests
# this is base url for way2sms
url = 'http://www.way2sms.com'


class Way2sms(object):
    def __init__(self):
        ses = requests.session()
        ses.headers.update({'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'DNT': '1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.8'})
        response = ses.get(url)
        # print response.history
        # if response.history:
        #     print "Request was redirected"
        #     for resp in response.history:
        #         # print resp.status_code, resp.url
        #     print "Final destination:"
        #     print response.status_code, response.url
        # else:
        #     # print "Request was not redirected"
        new_url = response.url
        # new_url is redirected url
        usr = str(raw_input('Enter your mobile number:'))
        pas = getpass.getpass()
        ses.post(new_url+'Login1.action', 'username='+usr+'&password='+str(pas))
        # print ses.cookies
        # print page.headers, page.cookies, page.status_code
        # print new_url
        # print page.content

    def sms(self, mobile):
        string = str(raw_input('Enter content: '))
        urllib.quote(string)
if __name__ == '__main__':
    # w = Way2sms().sms()
    string = str(raw_input('Enter content: '))
    print string
    print urllib.quote(string)
