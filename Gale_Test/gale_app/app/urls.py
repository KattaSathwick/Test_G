from django.conf.urls import url
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [url(r'^$',views.home,name="home"),
		url(r'^api/',views.CrawledViewSet, name="api")
		]
#urlpatterns = [url(r'^$',TemplateView.as_view(template_name='index.html')),
#		url(r'/login',TemplateView.as_view(template_name='login.html'))
#	      ]
