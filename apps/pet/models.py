from django.db import models

from user.models import User


class PetBreed(models.Model):
    class Meta:
        verbose_name = '宠物品种'
        verbose_name_plural = verbose_name
        db_table = 'T_PetBreed'

    name = models.CharField('名字', max_length=255)
    race = models.SmallIntegerField('种族', choices=((0, '猫'), (1, '狗'), (2, '其他')), default=0)
    path = models.ImageField('图片路径', upload_to="breed/")
    variety = models.CharField('品种', max_length=255)

    def __str__(self):
        return self.name


class PetImage(models.Model):
    class Meta:
        verbose_name = '宠物图片'
        verbose_name_plural = verbose_name
        db_table = 'T_PetImage'

    image = models.ImageField('图片', upload_to="pet/image/")
    width = models.IntegerField('图片宽', null=True)
    height = models.IntegerField('图片高', null=True)

    def __str__(self):
        return self.image.name


class Pet(models.Model):
    class Meta:
        verbose_name = '宠物'
        verbose_name_plural = verbose_name
        db_table = 'T_Pet'
        ordering = ['-id']

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    breed = models.ForeignKey(PetBreed, on_delete=models.CASCADE, default=1, verbose_name='品种')
    sex = models.SmallIntegerField('性别', choices=((0, '公'), (1, '母')), default=0)
    name = models.CharField('名字', max_length=255)
    weight = models.DecimalField('体重', max_digits=20, decimal_places=5, default=0)
    birth = models.DateField('出生日期', null=True)
    visual = models.BooleanField('可见', default=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return f'{self.name} {self.breed}'


class PetImageMap(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name='宠物', related_name='FK_pet')
    image = models.ForeignKey(PetImage, on_delete=models.CASCADE, verbose_name='宠物图片', related_name='FK_pet_image')
    cover = models.BooleanField('封面', default=False)

    class Meta:
        verbose_name = '宠物图片映射'
        verbose_name_plural = verbose_name
        db_table = 'T_PetImageMap'

    def __str__(self):
        return f'{self.pet} {self.image}'
