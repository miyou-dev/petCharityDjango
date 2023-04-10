from rest_framework.serializers import ModelSerializer, SerializerMethodField

from drf_yasg.utils import swagger_serializer_method

from question.models import Question, Answer
from user.models import UserCollect

from user.utils.serializers import UserPublicInformationSerializer


# 问答 问题 序列化
class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


# 问答 问题 信息序列化
class QuestionInformationSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        depth = 1

    user = SerializerMethodField(label='用户')
    newAnswer = SerializerMethodField(label='最新回复')
    answerCount = SerializerMethodField(label='回复数量')
    collect_count = SerializerMethodField(label='收藏人数')
    is_collect = SerializerMethodField(label='是否收藏')

    @swagger_serializer_method(serializer_or_field=UserPublicInformationSerializer)
    def get_user(self, question: Question):
        return UserPublicInformationSerializer(question.user, context=self.context).data

    def get_newAnswer(self, question: Question) -> str:
        first = Answer.objects.filter(question=question).all().first()
        print(type(first))
        if isinstance(first, Answer):
            return first.answer
        return ''

    def get_answerCount(self, question: Question) -> int:
        return Answer.objects.filter(question=question).all().count()

    def get_collect_count(self, question: Question) -> int:
        return UserCollect.objects.filter(collect_category=3, collect_id=question.id).count()

    def get_is_collect(self, question: Question) -> bool:
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return UserCollect.objects.filter(user=request.user, collect_category=3, collect_id=question.id).exists()
        return False


# 问答 答案 序列化
class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


# 问答 答案 信息序列化
class AnswerInformationSerializer(ModelSerializer):
    class Meta:
        model = Answer
        exclude = ['question']

    user = SerializerMethodField(label='用户')

    @swagger_serializer_method(serializer_or_field=UserPublicInformationSerializer)
    def get_user(self, question: Question):
        return UserPublicInformationSerializer(question.user, context=self.context).data
