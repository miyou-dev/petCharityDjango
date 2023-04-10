from django.contrib import admin

from question.models import QuestionClassification, Question, Answer


@admin.register(QuestionClassification)
class QuestionClassificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'classification')
    search_fields = ['classification']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'create_time')
    search_fields = ['question']
    list_filter = ['user']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'create_time')
    search_fields = ['answer']
    list_filter = ['question']
