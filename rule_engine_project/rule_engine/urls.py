# rule_engine/urls.py
from django.urls import path
from .views import create_rule, evaluate_rule, modify_rule, index

urlpatterns = [
    path('', index, name='index'),
    path('create_rule/', create_rule, name='create_rule'),
    path('evaluate_rule/', evaluate_rule, name='evaluate_rule'),
    path('modify_rule/', modify_rule, name='modify_rule'),  # Make sure this is here
]
