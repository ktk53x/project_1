from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name="index"),
    re_path(r'^code_searcher/$', views.code_searcher, name="code_searcher"),
    re_path(r'^analyse_rating/$', views.rating_analyser, name="rating_analyser"),
    re_path(r'^questions_and_attempts/$', views.questions_and_attempts, name="questions_and_attempts"),
    re_path(r'^compare_contest/$', views.contest_comparator, name="contest_comparator"),
    re_path(r'^average_gap/$', views.average_gap, name="average_gap"),
]