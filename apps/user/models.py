from django.db import models

from address.models import Area


class Contact(models.Model):
    class Meta:
        verbose_name = '联系方式'
        verbose_name_plural = verbose_name
        db_table = 'T_Contact'

    phone = models.CharField('手机号', max_length=255, null=True)
    mail = models.CharField('邮箱', max_length=255, null=True)
    qq = models.CharField('QQ', max_length=255, null=True)
    wechat = models.CharField('微信', max_length=255, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return f'{self.phone} {self.create_time}'


class User(models.Model):
    nickname = models.CharField('昵称', max_length=255, null=True)
    phone = models.CharField('手机号', unique=True, max_length=11)
    password = models.CharField('密码', max_length=255, null=True)
    qq = models.CharField('QQ', unique=True, max_length=10, null=True)
    sex = models.SmallIntegerField('性别', choices=((0, '保密'), (1, '男'), (2, '女')), default=0)
    identity = models.SmallIntegerField('身份', choices=((-1, '受限用户'), (0, '普通用户')), default=0)
    area = models.ForeignKey(Area, on_delete=models.SET_DEFAULT, verbose_name='所属地区', default=430602)
    introduction = models.CharField('简介', max_length=255, default='')
    head = models.ImageField('头像', upload_to="user/head/", null=True)
    balance = models.DecimalField('余额', max_digits=20, decimal_places=3, default=0)
    pay_password = models.CharField('支付密码', max_length=255, default='c984aed014aec7623a54f0591da07a85fd4b762d')
    real_name = models.CharField('真实姓名', max_length=255, null=True)
    id_card = models.CharField('身份证号码', max_length=18, null=True)
    token = models.CharField('token', max_length=1023, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, verbose_name='联系方式', null=True)

    create_time = models.DateTimeField('注册时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        db_table = 'T_User'
        ordering = ['-id']

    def __str__(self):
        return f'{self.nickname} ({self.phone}'


class UserFollowing(models.Model):
    followers = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='粉丝', related_name='FK_followers')
    following = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='被关注', related_name='FK_following')
    time = models.DateTimeField('关注时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户关注'
        verbose_name_plural = verbose_name
        db_table = 'T_UserFollowing'
        ordering = ['-id']

    def __str__(self):
        return f'{self.followers} ({self.following} )'


class UserCollect(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    collect_category = models.SmallIntegerField('收藏类别', choices=((0, '未知'), (1, '众筹'), (2, '领养')), default=0)
    collect_id = models.IntegerField('收藏ID')
    collect_time = models.DateTimeField('收藏时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        db_table = 'T_UserCollect'
        ordering = ['-id']

    def __str__(self):
        return f'{self.user} {self.collect_category} {self.collect_id}'


class UserFeedback(models.Model):
    nickname = models.CharField('昵称', max_length=255)
    title = models.CharField('标题', max_length=255)
    content = models.TextField('内容')
    score = models.IntegerField('评级')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户反馈'
        verbose_name_plural = verbose_name
        db_table = 'T_UserFeedback'
        ordering = ['-id']

    def __str__(self):
        return f'{self.nickname} {self.title} {self.create_time}'
