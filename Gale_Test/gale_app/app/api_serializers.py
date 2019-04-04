from rest_framework import serializers
from .models import crawl_data 

class CrawlDataSerialiser(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = crawl_data
        fields = ('requested_url', 'image', 'crawled_from_url', 'depth_level', 'created_at', 'modified_at')
