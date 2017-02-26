# Way2sms


Python module to send sms within india via way2sms.
### Features
  - Send any legnth of SMS. if text legnth exceeded, it will send multiple sms to send rest of content. 
  - Send to multiple mobile numbers.


```python
Way2sms().sms(string='SMS content', mobile=9999999999)
Way2sms().sms(string='text', mobile=[9999999999, 9999999998]
```
>sms() method take two keyword parameter
  - **string**=str()
  - **mobile** can be interger or list

### Todos

 - logout of session
