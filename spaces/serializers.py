from rest_framework import serializers

from .models import Space


class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = ["name"]
