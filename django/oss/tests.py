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

body = "关于服务器的问题处理办法"
message = MIMEText(body, 'html', 'utf-8')
message["subject"] = "关于服务器处理办法"
message["From"] = EMAIL_HOST_USER
message["To"] = "xialongjun@lb-tech.net"
print(message.as_string())

smtp_instance.sendmail(EMAIL_HOST_USER, ["xialongjun@lb-tech.net",], message.as_string())
# print(id(smtp_instance))
# smtp_instance2 = smtp_instance.reinstantiation()
# print(id(smtp_instance), id(smtp_instance2))
# smtp_instance2.sendmail(EMAIL_HOST_USER, [EMAIL_HOST_USER,], message.as_string())
# from utils.smtp import smtp_instance as a111
# print(1111,id(a111))


