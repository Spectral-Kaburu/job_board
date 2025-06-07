from rest_framework import serializers  
from users.models import User # Import custom User model from users app
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

"""Module: serializers 
    Converts complex data types to python data types that can be rendered into JSON, XML, etc
    It also handles validation and deserialization"""


# Map model instances to JSON and back
class RegisterSerializer(serializers.ModelSerializer):
    # Email field with uniqueness validator to check duplicates before saving
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]  # Validate password
    ) # Ensures password is accepted during input but never returned

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password'] # These fields will be serialized/deserialized when sending/receiving data.

    def create(self, validated_data):   # validated_data contains validated input data
        user = User.objects.create_user(    # type: ignore
            email = validated_data['email'],
            password = validated_data['password'],
            first_name = validated_data.get('first_name', ''),
            last_name = validated_data.get('last_name', '')
        )  
        return user
