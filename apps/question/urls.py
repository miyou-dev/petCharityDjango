from django.urls import path

from question.views.answer_information_view import AnswerInformationView
from question.views.answer_view import AnswerView
from question.views.question_information_view import QuestionInformationView
from question.views.question_view import QuestionView

urlpatterns = [
    # 问 查
    path('question/<int:pk>', QuestionInformationView.as_view({'get': 'retrieve'})),
    path('question/list', QuestionInformationView.as_view({'get': 'list'})),
    # 问 增 删 改
    path('question/create', QuestionView.as_view({'post': 'create'})),
    path('question/delete/<int:pk>', QuestionView.as_view({'delete': 'destroy'})),
    path('question/partialUpdate/<int:pk>', QuestionView.as_view({'patch': 'partial_update'})),

    # 答 查
    path('answer/list', AnswerInformationView.as_view({'get': 'list'})),
    # 答 增 删 改
    path('answer/create', AnswerView.as_view({'post': 'create'})),
    path('answer/delete/<int:pk>', AnswerView.as_view({'delete': 'destroy'})),

]
