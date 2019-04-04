# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class crawl_data(models.Model):
	requested_url = models.TextField(primary_key=True)
	image =  models.CharField(max_length=250)
	crawled_from_url = models.CharField(max_length=250)
	depth_level = models.IntegerField()
	created_at = models.DateField()
	modified_at = models.DateField()

	class Meta:
		managed=True
		db_table='app_crawl_data'
		unique_together=(('image','crawled_from_url'))

