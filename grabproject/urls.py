from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ihsLogin, name='ihslogin'),
    path('hostproject', views.hostproject, name='hostproject'),
    path('instancebuilding', views.instancebuilding, name='instancebuilding') ,
    path('hostingsuccess', views.hostingsuccess, name='hostingsuccess') ,
    path('hostingfailed', views.hostingfailed, name='hostingfailed') ,
    
    path('loggedout', views.loggedout, name='loggedout') ,
   
]
