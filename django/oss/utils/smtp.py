# 该模块用于实例化SMTP

from smtplib import SMTP
import logging
import sys

EMAIL_HOST = "smtp.163.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = "fruler@163.com"
EMAIL_HOST_PASSWORD = "wy6666"

class NewSMTP(SMTP):
    # _instance = None
    #
    # # 单例模式
    # def __new__(cls, *args, **kwargs):
    #     if not cls._instance:
    #         cls._instance = super(NewSMTP, cls).__new__(cls)
    #     return cls._instance


    # 重新实例化
    def reinstantiation(self):
        try:
            self.quit()
        except Exception as e:
            logging.error("close smtp server error!")

        del sys.modules["utils.smtp"]
        from utils.smtp import smtp_instance
        return smtp_instance


# 重新实例化
smtp_instance = NewSMTP(EMAIL_HOST, EMAIL_PORT)
smtp_instance.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)


