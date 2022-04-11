from rest_framework import serializers

from .models import Project, Risk


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "space", "description"]


class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = "__all__"
