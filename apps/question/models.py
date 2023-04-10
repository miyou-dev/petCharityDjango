from django.db import models

from user.models import User


class QuestionClassification(models.Model):
    class Meta:
        verbose_name = '宠物问答分类'
        verbose_name_plural = verbose_name
        db_table = 'T_QuestionClassification'

    classification = models.CharField('分类', max_length=255)

    def __str__(self):
        return self.classification


class Question(models.Model):
    class Meta:
        verbose_name = '宠物问答问题'
        verbose_name_plural = verbose_name
        db_table = 'T_Question'
        ordering = ['-id']

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    classification = models.ForeignKey(QuestionClassification, on_delete=models.CASCADE, verbose_name='分类')
    question = models.TextField('问题描述')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.question


class Answer(models.Model):
    class Meta:
        verbose_name = '宠物问答答案'
        verbose_name_plural = verbose_name
        db_table = 'T_Answer'
        ordering = ['-id']

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='问题')
    answer = models.TextField('答案')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.answer
