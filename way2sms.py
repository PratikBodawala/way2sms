import getpass
import urllib
import textwrap
import requests
# this is base url for way2sms
url = 'http://www.way2sms.com'


class Way2sms(object):
    def __init__(self):
        self.ses = requests.session()
        self.ses.headers.update({'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'DNT': '1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.8'})
        response = self.ses.get(url)
        self.new_url = response.url
        # new_url is redirected url
        usr = str(raw_input('Enter your mobile number:'))
        pas = getpass.getpass()
        if self.ses.post(self.new_url+'Login1.action', 'username='+usr+'&password='+str(pas)).ok:
            print "Login successfully"
        else:
            print "Login failed"

    def sms(self, **kwargs):
        # textwrap.wrap(string, 140)
        mobile=str(raw_input('Enter mobile number: '))
        string = str(raw_input('Enter content: '))
        msglen = len(string)
        string = urllib.quote(string)
        token = self.ses.cookies['JSESSIONID']
        token = token[4:]
        print self.ses.post(self.new_url+'smstoss.action', 'ssaction=ss&Token='+str(token)+'&mobile='+str(mobile)+'&message='+string+'&msgLen='+str(140-msglen)).status_code

        print string
if __name__ == '__main__':
    w = Way2sms().sms()
    # string = str(raw_input('Enter content: '))
    # print string
    # print urllib.quote(string)
