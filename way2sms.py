import getpass
import urllib
import textwrap
import requests
import time
import os
import datetime
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from prettytable import ALL as ALL
import cPickle as pickle
import sys
url = 'http://www.way2sms.com'


class Way2sms(object):
    """mobile and string are keywords parameter of sms method."""
    def __init__(self):
        self.ses = None
        response = requests.get(url)
        self.new_url = response.url
        if os.path.exists('.token'):
            with open('.token', 'r') as Token:
                self.ses, self.token, self.new_url = pickle.load(Token)
            page = self.ses.get(self.new_url+'ebrdg?id='+self.token).text
            if 'Welcome to Way2SMS' in page:
                print 'session is ok'

            else:
                print 'session expired'
                self.token = None
                self.ses = requests.session()
                self.ses.headers.update({'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'DNT': '1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.8'})
                usr = str(raw_input('Enter your mobile number:'))
                pas = getpass.getpass()
                if self.ses.post(self.new_url + 'Login1.action', 'username=' + str(usr) + '&password=' + str(pas)).ok:
                    print "Login successfully"
                    self.token = self.ses.cookies['JSESSIONID']
                    self.token = self.token[4:]
                    with open('.token', 'w') as Token:
                        pickle.dump((self.ses, self.token, self.new_url), Token)
                else:
                    print "Login failed"

        else:
            self.token = None
            self.ses = requests.session()
            self.ses.headers.update({'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
                                     'Upgrade-Insecure-Requests': '1',
                                     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                                     'Content-Type': 'application/x-www-form-urlencoded',
                                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                     'DNT': '1', 'Accept-Encoding': 'gzip, deflate',
                                     'Accept-Language': 'en-US,en;q=0.8'})
            usr = str(raw_input('Enter your mobile number:'))
            pas = getpass.getpass()
            if self.ses.post(self.new_url + 'Login1.action', 'username=' + str(usr) + '&password=' + str(pas)).ok:
                print "Login successfully"
                self.token = self.ses.cookies['JSESSIONID']
                self.token = self.token[4:]
                with open('.token', 'w') as Token:
                    pickle.dump((self.ses, self.token, self.new_url), Token)
            else:
                print "Login failed"

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
                    page = self.ses.post(self.new_url+'smstoss.action', 'ssaction=ss&Token='+str(self.token)+'&mobile='+str(mobile_no)+'&message='+qstring+'&msgLen='+str(140-msglen)).text
                    time.sleep(3)
                    if "Rejected : Can't submit your message, finished your day quota." not in page:
                        print mobile_no, 'sent successfully.'
                    else:
                        print 'quota finished!'
                        sys.exit(1)

    def history(self, day):
        date = (datetime.date.today() - datetime.timedelta(days=int(day))).strftime('%d/%m/%Y')
        page = self.ses.post(self.new_url+'sentSMS.action?dt='+str(date)+'&Token='+str(self.token))
        soup = BeautifulSoup(page.text, 'html.parser')
        # print soup.prettify()
        part = soup.find_all('div', {'class': 'mess'})
        print 'SMS history for date:', date
        table = PrettyTable(hrules=ALL)
        table.field_names = ['Time', 'Mobile no', 'SMS']
        for div in part:
            t = div.find('p', {'class': 'time'})
            time = t.find('span').text
            no = div.find('b').text
            divrb = div.find('div', {'class': 'rb'})
            p = divrb.find('p').text
            table.add_row([time, no, p])
        print table

    def logout(self):
        self.ses.get(self.new_url+'main.action')
        try:
            os.remove('.token')
        finally:
            print 'Log-out!'
            sys.exit(0)
    def check_limit(self):
        date = datetime.date.today().strftime('%d/%m/%Y')
        page = self.ses.post(self.new_url + 'sentSMS.action?dt=' + str(date) + '&Token=' + str(self.token))
        soup = BeautifulSoup(page.text, 'html.parser')
        # print soup.prettify()
        sms = len(soup.find_all('div', {'class': 'mess'}))
        print 'You have {} sms left.'.format(100 - sms)

if __name__ == '__main__':
    Way2sms().check_limit()
    # Way2sms().history(13)
