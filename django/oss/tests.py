from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header
import logging
import time
from utils.smtp import smtp_instance

EMAIL_HOST = "smtp.163.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = "fruler@163.com"
EMAIL_HOST_PASSWORD = "wy6666"

body = "Python 邮件测试"
message = MIMEText(body, 'html', 'utf-8')
message["subject"] = Header("邮件测试", 'utf-8')
message["from"] = Header("xialongjun@lb-tech.net", 'utf--8')
message["to"] = EMAIL_HOST_USER


smtp_instance.sendmail(EMAIL_HOST_USER, [EMAIL_HOST_USER,], message.as_string())
print(id(smtp_instance))
smtp_instance2 = smtp_instance.reinstantiation()
print(id(smtp_instance), id(smtp_instance2))
smtp_instance2.sendmail(EMAIL_HOST_USER, [EMAIL_HOST_USER,], message.as_string())
from utils.smtp import smtp_instance as a111
print(1111,id(a111))


