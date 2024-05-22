from .models import *
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password']
        # fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
    # creating the user object with in the serializer
    def create(self, validated_data):
        user = CustomUser.objects.create_user(email=validated_data["email"],
                                              password=validated_data["password"])

        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ["email", "password"]


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDetail
        fields = "__all__"


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = "__all__"
