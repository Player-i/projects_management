from rest_framework import serializers
from django.contrib.auth.forms import UserCreationForm
from home.models import MyUser, Project, Step

# Create your serializers here.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'

class EmailLoginFormSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()



class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password1', 'password2']

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        password = validated_data.pop('password1')
        user = MyUser.objects.create_user(**validated_data, password=password)
        return user

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = '__all__'  # You can also specify the fields you want to include explicitly


    # You can add any additional validation or custom behavior here if needed