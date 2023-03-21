from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField, ValidationError

from drf_yasg.utils import swagger_serializer_method

from utils.validation import judge_nickname_verify

from user.models import Contact, User, UserFollowing, UserCollect, UserFeedback
from adopt.models import PetAdopt


# 联系方式序列化
class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


# 用户共享信息序列化
class UserPublicInformationSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'pay_password', 'real_name', 'id_card', 'balance', 'token']
        depth = 3

    sex_value = CharField(source='get_sex_display', label='性别')
    identity_value = CharField(source='get_identity_display', label='身份')
    verified = SerializerMethodField(label='是否实名认证')
    followers_count = SerializerMethodField(label='关注人数')
    following_count = SerializerMethodField(label='粉丝人数')
    contact = SerializerMethodField(label='联系方式')

    @swagger_serializer_method(serializer_or_field=ContactSerializer)
    def get_contact(self, user: User):
        return ContactSerializer(user.contact, context=self.context).data

    def get_verified(self, user: User) -> bool:
        # 判断是否实名认证
        return user.id_card is not None

    def get_followers_count(self, user: User) -> int:
        return UserFollowing.objects.filter(following=user).count()

    def get_following_count(self, user: User) -> int:
        return UserFollowing.objects.filter(followers=user).count()


# 返回用户信息序列化类
class UserLoginInformationSerializer(UserPublicInformationSerializer):
    class Meta:
        model = User
        exclude = ['password', 'pay_password', 'id_card']
        depth = 3

    collect_count = SerializerMethodField(label='收藏数')
    adopt_count = SerializerMethodField(label='发布众筹数')

    def get_collect_count(self, user: User) -> int:
        return UserCollect.objects.filter(user=user).count()

    def get_adopt_count(self, user: User) -> int:
        return PetAdopt.objects.filter(pet__user=user).count()


# 用户信息修改序列化
class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'qq', 'sex', 'area', 'introduction']

    def validate_nickname(self, nickname):
        if nickname != '' and not judge_nickname_verify(nickname):
            raise ValidationError('昵称长度需大于等于1')
        return nickname


# 用户头像上传序列化
class UserImageSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['head']


class UserFollowingSerializer(ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = '__all__'

    followers = SerializerMethodField(label='关注用户信息')
    following = SerializerMethodField(label='被关注用户信息')

    @swagger_serializer_method(serializer_or_field=UserPublicInformationSerializer)
    def get_followers(self, user_focus: UserFollowing):
        return UserPublicInformationSerializer(user_focus.followers, context=self.context).data

    @swagger_serializer_method(serializer_or_field=UserPublicInformationSerializer)
    def get_following(self, user_focus: UserFollowing):
        return UserPublicInformationSerializer(user_focus.following, context=self.context).data


class UserFeedbackSerializer(ModelSerializer):
    class Meta:
        model = UserFeedback
        fields = '__all__'
