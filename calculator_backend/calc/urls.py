from django.urls import path

from . import views
from .forms import CalcForm1, CalcForm2, CalcForm3, CalcForm4
from .views import CalcWizard

urlpatterns = [
    path('', views.index, name='index'),
    path('pmtsz/', views.pmtsz, name='pmtsz'),
    path('contact/', views.contact, name='contact'),
    path('form/', CalcWizard.as_view([CalcForm1, CalcForm2, CalcForm3, CalcForm4]), name="CalcWizard")
]
