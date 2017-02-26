import getpass
import urllib
import textwrap
import requests
import time
url = 'http://www.way2sms.com'


class Way2sms(object):
    def __init__(self):
        self.ses = requests.session()
        self.ses.headers.update({'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'DNT': '1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.8'})
        response = self.ses.get(url)
        self.new_url = response.url
        usr = str(raw_input('Enter your mobile number:'))
        pas = getpass.getpass()
        if self.ses.post(self.new_url+'Login1.action', 'username='+str(usr)+'&password='+str(pas)).ok:
            print "Login successfully"
        else:
            print "Login failed"
        self.token = self.ses.cookies['JSESSIONID']
        self.token = self.token[4:]

    def sms(self, **kwargs):
        if 'mobile' not in kwargs:
            mobile = str(raw_input('Send sms to: '))
        else:
            mobile = kwargs['mobile']
        if 'string' not in kwargs:
            string = str(raw_input('Enter TEXT SMS: '))
        else:
            string = kwargs['string']
        if type(mobile) is int:
            mobile = list(str(mobile).split())
        if type(mobile) is list:
            for mobile_no in mobile:
                lofstr = textwrap.wrap(string, 140)
                for string in lofstr:
                    msglen = len(string)
                    qstring = urllib.quote(string)
                    self.ses.post(self.new_url+'smstoss.action', 'ssaction=ss&Token='+str(self.token)+'&mobile='+str(mobile_no)+'&message='+qstring+'&msgLen='+str(140-msglen))
                    time.sleep(3)
if __name__ == '__main__':
    Way2sms().sms()
