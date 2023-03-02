from django.db import models


class Province(models.Model):
    class Meta:
        verbose_name = '省'
        verbose_name_plural = verbose_name
        db_table = 'T_Province'
        ordering = ['id']

    province = models.CharField('省', unique=True, max_length=255)

    def __str__(self):
        return self.province


class City(models.Model):
    class Meta:
        verbose_name = '市'
        verbose_name_plural = verbose_name
        db_table = 'T_City'
        ordering = ['id']

    city = models.CharField('市', max_length=255)
    belong_province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name='所属省')

    def __str__(self):
        return self.city


class Area(models.Model):
    class Meta:
        verbose_name = '区'
        verbose_name_plural = verbose_name
        db_table = 'T_Area'
        ordering = ['id']

    area = models.CharField('区', max_length=255)
    belong_city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='所属市')

    def __str__(self):
        return self.area
