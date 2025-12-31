from django.urls import path
from .views import IndexView,AboutView,CourseView,CourseDetail,ContentDetailView, download_file

app_name = 'upskill'

urlpatterns = [
     path('',IndexView.as_view(),name='index'),
     path('subject/<slug:subject_slug>',IndexView.as_view(),name='courses_of_subject'),
     path('about/',AboutView.as_view(),name='about'),
     path('courses/',CourseView.as_view(),name='courses'),
     path('course/<slug:slug>/detail/',CourseDetail.as_view(),name='detail'),
     path('lesson/<int:pk>/',ContentDetailView.as_view(),name='content_detail'),
     path('content/<int:content_id>/download/',download_file,name='content_file_download'),
]
