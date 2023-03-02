from django.db import models


class Administrator(models.Model):
    phone = models.CharField('手机号', unique=True, max_length=11)
    password = models.CharField('密码', max_length=255)
    nickname = models.CharField('昵称', max_length=255, null=True)
    qq = models.CharField('QQ', unique=True, max_length=10, null=True)
    sex = models.SmallIntegerField('性别', choices=((0, '保密'), (1, '男'), (2, '女')), default=0)
    introduction = models.CharField('简介', max_length=255, default='')
    head = models.ImageField('头像', upload_to="user/head/", null=True)
    token = models.CharField('token', max_length=1023, null=True)
    create_time = models.DateTimeField('注册时间', auto_now_add=True)

    class Meta:
        verbose_name = '管理员用户'
        verbose_name_plural = verbose_name
        db_table = 'T_Administrator'

    def __str__(self):
        return f'{self.phone} {self.nickname}'
