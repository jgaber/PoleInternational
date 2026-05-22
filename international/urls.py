from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('contacts/', views.contact, name='contact'),
    path('EU-research-call/', views.eu_form, name='eu_form'),
    path('external-info/<slug:link_slug>/', views.external_link_info, name='external_link_info'),
    path("horizon-pillars/", views.horizon_pillars_view, name="horizon_pillars"),


]
