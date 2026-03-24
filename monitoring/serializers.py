from rest_framework import serializers
from .models import Keyword
from .models import Flag


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'name']

class FlagSerializer(serializers.ModelSerializer):
    keyword = serializers.CharField(source='keyword.name')
    content = serializers.CharField(source='content_item.title')

    class Meta:
        model = Flag
        fields = ['id', 'keyword', 'content', 'score', 'status']