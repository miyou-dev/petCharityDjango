from django.db import models

from administrator.models import Administrator
from pet.models import PetBreed, PetImage
from user.models import User


class PetDonate(models.Model):
    class Meta:
        verbose_name = '宠物帮助众筹'
        verbose_name_plural = verbose_name
        db_table = 'T_PetDonate'
        ordering = ['-id']

    admin = models.ForeignKey(Administrator, on_delete=models.CASCADE, verbose_name='发起管理员')
    breed = models.ForeignKey(PetBreed, on_delete=models.CASCADE, default=1, verbose_name='品种')
    sex = models.SmallIntegerField('性别', choices=((0, '公'), (1, '母')), default=0)
    name = models.CharField('名字', max_length=255)
    weight = models.DecimalField('体重', max_digits=20, decimal_places=5, default=0)
    birth = models.DateField('出生日期', null=True)
    description = models.TextField('描述')
    amount = models.IntegerField('众筹金额', default=100)
    state = models.SmallIntegerField('状态', choices=((0, '待发布'), (1, '众筹中'), (2, '众筹结束')), default=0)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    publish_time = models.DateTimeField('发布时间', null=True)
    finish_time = models.DateTimeField('结束时间', null=True)

    def __str__(self):
        return f'{self.name} {self.breed}'


class PetDonateImageMap(models.Model):
    donate = models.ForeignKey(PetDonate, on_delete=models.CASCADE, verbose_name='宠物帮助众筹', related_name='FK_donate')
    image = models.ForeignKey(PetImage, on_delete=models.CASCADE, verbose_name='宠物图片',
                              related_name='FK_donate_image')
    cover = models.BooleanField('封面', default=False)

    class Meta:
        verbose_name = '宠物帮助众筹图片映射'
        verbose_name_plural = verbose_name
        db_table = 'T_PetDonateImageMap'

    def __str__(self):
        return f'{self.donate} {self.image}'


class PetDonationList(models.Model):
    class Meta:
        verbose_name = '宠物帮助众筹捐赠名单'
        verbose_name_plural = verbose_name
        db_table = 'T_PetDonationList'
        ordering = ['-id']

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    donate = models.ForeignKey(PetDonate, on_delete=models.CASCADE, verbose_name='宠物帮助众筹')
    amount = models.IntegerField('捐赠金额', default=0)
    order = models.CharField('订单号', max_length=255)
    remarks = models.CharField('备注', max_length=255, default='')
    donate_time = models.DateTimeField('捐赠时间', auto_now_add=True)

    def __str__(self):
        return f'{self.user}  {self.donate} {self.amount}'
