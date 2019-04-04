# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .api_serializers import CrawlDataSerialiser
#from rest_framework import viewsets
from .models import crawl_data
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def home(request):
	print request.method
	print request.POST
	db_data = GetDbRecords()
	import requests
	import json
	from lxml import html
	api_request_to_fetch_all_records = requests.get('http://127.0.0.1:8000/gale_mini_app/api/')
	data = html.fromstring(api_request_to_fetch_all_records.content)
	final_data  = json.loads(data.text)
	final_dict = {}
	for data in final_data:
		img = data['image']
		req_url = data['requested_url']
		if req_url in final_dict.keys():
			final_dict[req_url].append(img)
		else:
			final_dict.update({req_url:[img]})

	print final_dict
	
	if request.method=="GET":
		return render(request,'index.html', {'records':db_data, 'final_dict':final_dict})
	elif request.method == 'POST':
		url = request.POST.get('url','')
		depth_level = request.POST.get('depth_level','')
		if url and depth_level:
			from threading import Thread
			Thread(target=crawl(url,depth_level)).start()
		return render(request,'index.html', {'records':db_data,'final_dict':final_dict})

def crawl(url,depth_level):
	import os
	print url
	print depth_level
	os.system("python /home/sathwickkatta/Gale_Test/scrape_browse.py --url=%s --depth_level=%s"%(str(url),str(depth_level)))


@api_view(('GET',))
def CrawledViewSet(ListAPIView):
	url_requested = ListAPIView._request.path
	if 'q=' in url_requested:
		url = url_requested.split('q=')[1]
		#url = url_requested.split('q=')[1].split('/d=')[0]
		#depth_level= url_requested.split('q=')[1].split('/d=')[-1]
		#queryset = crawl_data.objects.filter(depth_level=depth_level,requested_url=url)
		queryset = crawl_data.objects.filter(requested_url=url)
	else:
		queryset = crawl_data.objects.all()
	#queryset = crawl_data.objects.filter(depth_level=1)
	serializer_class = CrawlDataSerialiser(queryset, many=True)
	return Response(serializer_class.data)

def GetDbRecords():
	return crawl_data.objects.values('requested_url').annotate(dcount=Count('requested_url'))
