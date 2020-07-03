import django_filters
from django_filters import DateFilter, CharFilter, ChoiceFilter
from .models import *
from django import forms

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created', lookup_expr='gte', label='From Date', widget=forms.DateInput(attrs={
        'type': 'date'
    }))
    end_date = DateFilter(field_name='date_created', lookup_expr='lte', label='To Date', widget=forms.DateInput(attrs={
        'type': 'date'
    }))
    
    class Meta:
        model = Order
        fields = '__all__'        
        exclude = ['customer','date_created','note']