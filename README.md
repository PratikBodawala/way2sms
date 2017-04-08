# Way2sms
Python module to send sms within india via way2sms.
### Features
  - Send any legnth of SMS. if text legnth exceeded, it will send multiple sms, to send rest of content. 
  - Send to multiple mobile numbers.
  - Save session
  - Command line helper (run.py)
  - Check daily limit of sms (limit is 100)
  - See the sent sms history N days old.
  - Logout
### Dependency
```bash
pip install -r requirements.txt
```
## way2sms.py
```python
Way2sms().sms(string='SMS content', mobile=9999999999)
Way2sms().sms(string='text', mobile=[9999999999, 9999999998]
Way2sms().history(N)
Way2sms().logout()
```
>sms() method take two keyword parameter
  - **string**=str()
  - **mobile** can be interger or list
 >histrory(N) N is days

# run.py
```bash
usage: run.py [-h] [-n CONTACT] [-t TEXT] [-s DAY] [-c] [-l]

optional arguments:
  -h, --help            show this help message and exit
  -n CONTACT, --number CONTACT
                        Contact number file
  -t TEXT, --text TEXT  Text SMS content file
  -s DAY, --sent DAY    N day old sent sms
  -c, --check           Check daily sms limit
  -l, --logout          To logout from session

```
