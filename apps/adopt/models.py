from django.db import models

from pet.models import Pet, PetImage
from user.models import User


class PetAdopt(models.Model):
    class Meta:
        verbose_name = '宠物领养'
        verbose_name_plural = verbose_name
        db_table = 'T_PetAdopt'
        ordering = ['-id']

    pet = models.OneToOneField(Pet, on_delete=models.CASCADE, verbose_name='关联宠物')
    title = models.CharField('标题', max_length=255)
    description = models.TextField('描述')
    requirements = models.TextField('领养要求', null=True)
    create_time = models.DateTimeField('发布时间', auto_now_add=True)

    def __str__(self):
        return f'{self.pet}'
