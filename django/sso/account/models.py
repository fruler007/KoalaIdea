from django.db import models

# Create your models here.
# 用户信息表
class UserProfile(models.Model):
    username = models.CharField(max_length=128, null=False)
    email = models.EmailField(max_length=128, null=True)
    mobile = models.CharField(max_length=64)
    password = models.CharField(max_length=128, null=False)
    reg_date = models.DateTimeField(auto_now_add=True)
    last_login_date = models.DateTimeField(auto_now=True)


# 用户权限表
class ServPermssions(models.Model):
    # 0 未启用
    # 1 已启用
    # 2 锁定
    user = models.ForeignKey(UserProfile)
    com_choice = (
        (0, "未启用"),
        (1, "已启用"),
        (2, "锁定"),
    )
    mall = models.IntegerField(choices=com_choice, default=0, help_text="商城")
    blog = models.BooleanField(choices=com_choice, default=0, help_text="博客")