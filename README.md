# Way2sms
Python module to send sms within india via way2sms.
### Features
  - Set environment variable **WAY2SMS_MOBILE** and **WAY2SMS_PASSWORD** to login, if environment variable is not set, login credential will be asked from standard input.
  - Send any legnth of SMS. if text legnth exceeded, it will send multiple sms, to send rest of content. 
  - Send to multiple mobile numbers.
  - File input support (phone numbers and sms)
  - Save session
  - Command line helper (run.py)
  - Check daily limit of sms
  - See the sent sms history N days old.
  - Logout
### Dependency
```bash
pip install -r requirements.txt
```
## way2sms.py
```python
w = Way2sms()
w.sms(text='SMS content', mobile=9999999999)
w.sms(text='SMS content', mobile=[9999999999, 9999999998])
w.history(day_ago)
w.logout()
```
>sms() method take two keyword parameter
  - **text** = str()
  - **mobile** can be interger or list
 >histrory(N) N is days

# run.py
```bash
usage: run.py [-h] [-n CONTACT] [-t TEXT] [-s DAY] [-c] [-a ADD] [-l]

optional arguments:
  -h, --help            show this help message and exit
  -n CONTACT, --number CONTACT
                        Contact number file
  -t TEXT, --text TEXT  Text SMS content file
  -s DAY, --sent DAY    N day old sent sms
  -c, --check           Check daily sms limit
  -a ADD, -add ADD      Add contact to your address book
  -l, --logout          To logout from session
```
>In contact either you can provide number, numbers or file path containing numbers with space or new line separated.
Same way, text can be provided in between quote or file path.