from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.form, name='form'),
    path('report/', views.report, name='report'),
    path('report/showreport/', views.showreport, name='showreport'),
    path('login/', views.login, name='login')
]