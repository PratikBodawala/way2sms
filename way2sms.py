import json
from getpass import getpass
import textwrap
import requests
import os
import datetime
from bs4 import BeautifulSoup
from prettytable import PrettyTable, ALL
import pickle
import sys
import re

sys.stdout.flush()
url = 'http://www.way2sms.com'


class SessionExpiredException(Exception):
    msg = "Session Expired"


class Way2sms(object):
    """mobile and string are keywords parameter of sms method."""

    def __init__(self):
        try:
            with open('.token', 'rb') as Token:
                self.ses, self.token = pickle.load(Token)
            page = self.ses.get(url + '/send-sms').text
            login_page = re.findall(r'<small>welcome</small>\s+<div class="user-title">(?P<user>[\w ]+)</div>', page)
            if len(login_page) is not 0:
                print('Welcome,', login_page[0])
            else:
                print('session expired')
                raise SessionExpiredException()

        except(FileNotFoundError, SessionExpiredException):
            self.ses = requests.session()
            self.ses.headers.update({
                'Proxy-Connection': 'keep-alive',
                'Accept': '*/*',
                'Origin': 'http://www.way2sms.com',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.53 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': 'http://www.way2sms.com/',
                'Accept-Language': 'en-US,en;q=0.9',
                'Host': 'www.way2sms.com'
            })
            import os
            while True:
                usr = os.getenv('WAY2SMS_MOBILE')
                if not usr:
                    usr = str(input('Enter your mobile number:'))
                pas = os.getenv('WAY2SMS_PASSWORD')
                if not pas:
                    pas = getpass()
                if self.ses.post('http://www.way2sms.com/re-login',
                                 data={
                                     'mobileNo': usr,
                                     'password': pas,
                                     'CatType': '',
                                     'redirectPage': '',
                                     'pid': '',
                                 }
                                 ).text == 'send-sms':
                    print("Login successfully")
                    self.token = self.ses.cookies['JSESSIONID']
                    self.token = self.token[4:]
                    with open('.token', 'wb') as Token:
                        pickle.dump((self.ses, self.token), Token)
                    break
                else:
                    print("Login failed")
            del os

    def checkwebmsgcount(self):
        return int(self.ses.post(url+'/CheckWebMsgCount', data={'type': 'sender'}).text)

    def sms(self, mobile=None, text=None):
        if mobile is None:
            mobile = str(input('Send sms to: '))

        if text is None:
            text = str(input('Enter TEXT SMS: '))

        if type(mobile) is str or type(mobile) is int:
            mobile = list(str(mobile).split(','))

        if type(mobile) is list:
            for mobile_no in mobile:
                if len(str(mobile_no)) is not 10:
                    print(mobile_no, 'is not valid')
                else:
                    lofstr = textwrap.wrap(text, 140)
                    for text in lofstr:
                        page = self.ses.post('http://www.way2sms.com/smstoss',
                                             data={
                                                 'Token': self.token,
                                                 'message': text,
                                                 'toMobile': mobile_no,
                                                 'ssaction': 'undefined',
                                                 'senderId': 'WAYSMS',
                                             }
                                             ).text
                        print('Sending SMS to', mobile_no)
                        if not int(page):
                            print('sent successfully.')
                        else:
                            print('You Have Exceeded the daily free SMS Limit. you can now send unlimited messages '
                                  'through our Services with only 20 Paise per messages , start using by topping up '
                                  'your wallet with min of "500/-" Only ')
                            sys.exit(1)

    def history(self, day):
        date = (datetime.date.today() - datetime.timedelta(days=int(day))).strftime('%Y-%m-%d')
        page = self.ses.post(url + '/sent-sms',
                             data={
                                 'pageNo': 0,
                                 'dt': str(date),
                                 'sType': 1,
                             })
        soup = BeautifulSoup(page.text, 'html.parser')
        part = soup.find('div', {'class': 'sent-list msgs-doc'})
        print('SMS history for date:', date)
        table = PrettyTable(hrules=ALL)
        table.field_names = ['Time', 'Mobile no', 'SMS']
        for div in part.find_all('li'):
            t = div.find('div', {'class': 'dtm'})
            time = t.find('span').text
            no = div.find('div', {'class': 'ctn-usr'}).text
            p = div.find('p').text
            table.add_row([time, no, p])
        print(table)

    def logout(self):
        self.ses.get('http://www.way2sms.com/Logout')
        try:
            os.remove('.token')
        finally:
            print('Log-out!')
            sys.exit(0)

    # http://www.way2sms.com/addContact
    def addContact(self, mobile, name: str, gender: str):
        return self.ses.post('http://www.way2sms.com/addContact', {'contno': mobile,
                                                                   'contname': name,
                                                                   'gender': gender.capitalize(),
                                                                   'groupid': 0,
                                                                   'token': self.token
                                                                   }).text

    def getcontact(self):
        _ = self.ses.get('http://www.way2sms.com/getContacts', params={'token': self.token}).json()
        _['contacts'] = json.loads(_['contacts'])
        return _

    def groupcontect(self):
        return self.ses.post('http://www.way2sms.com/GroupContacts').json()


if __name__ == '__main__':
    w = Way2sms()
    # w.sms(mobile=9876543210, text='Demo text message from cmd')
    # w.history(0)
    # w.logout()
