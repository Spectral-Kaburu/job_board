from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'company', 'location', 'description']
        read_only_fields = ['posted_by', 'posted_at', 'updated_at']
