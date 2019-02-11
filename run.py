#!/usr/bin/python3
import argparse
import os
import sys

from way2sms import Way2sms

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--number', action='store', dest='contact', help='Contact number file')
parser.add_argument('-t', '--text', action='store', dest='text', help='Text SMS content file')
parser.add_argument('-s', '--sent', action='store', dest='day', help='N day old sent sms')
parser.add_argument('-c', '--check', action='store_true', dest='check', help='Check daily sms limit')
parser.add_argument('-a', '-add', action='store', dest='add', help='Add contact to your address book')
parser.add_argument('-l', '--logout', action="store_true", dest='logout', help='To logout from session')
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
results = parser.parse_args()
w = Way2sms()
if results.add:
    name = input('Enter Contact name:')
    mobile = input('Enter Contact number:')
    gender = input('Enter gender')
    w.addContact(mobile, name, gender)
if results.logout:
    w.logout()
if results.check:
    w.checkwebmsgcount()
    sys.exit(0)
if results.day:
    w.history(results.day)
    sys.exit(0)
if not results.contact and results.text:
    print('Please provide mobile number!')
    sys.exit(1)
if not results.text and results.contact:
    print('Please provide Text sms content!')
    sys.exit(1)
text = ''
mobile_numbers = []
if os.path.isfile(results.contact):
    contact_file = open(results.contact)
    mobile_numbers = [mobile.strip() for mobile in contact_file]
else:
    mobile_numbers = str(results.contact).split(',')
if os.path.isfile(results.text):
    text = open(results.text).read()
else:
    text = results.text
print(mobile_numbers, text)
w.sms(mobile=mobile_numbers, text=text)
