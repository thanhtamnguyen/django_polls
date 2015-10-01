from django.conf.urls import url
from . import views

urlpatterns=[	
	# url(r'^specifics/(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
	# url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),

	url(r'^$', views.IndexView.as_view(), name='index'),
	
	#replace question_id with pk
	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
	url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
	
	url(r'^(?P<question_id>[0-9]+)/votes/$', views.vote, name='votes'),
	]