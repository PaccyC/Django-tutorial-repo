from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer



class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields =["id","username","email","password1","password2","first_name","last_name"]