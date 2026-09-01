from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services_list, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('projects/', views.projects_list, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('process/', views.process_view, name='process'),
    path('request-a-quote/', views.request_quote, name='request_quote'),
    path('quote/success/<int:pk>/', views.quote_success, name='quote_success'),
    path('contact/', views.contact_view, name='contact'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]
