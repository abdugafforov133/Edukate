from django.shortcuts import render
from django.views import View
from django.views.generic import ListView,TemplateView,DetailView
from .models import Subject,Course,Module, Content


import os
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .models import File, Content
# Create your views here.


# def index(request):
#     if request.method == 'POST':
#         pass
    
#     else:
#         pass

#     return render(request,'upskill/index.html')


# class IndexView(View):
    
#     def get(self,request,subject_slug = None):
        
#         if subject_slug is None:
#             subjects = Subject.objects.all()
#         else:
#             pass
    
#         context = {
#             'subjects':subjects.order_by('id')
#         }
        
#         return render(request,'upskill/index.html',context)
    

class IndexView(ListView):
    model = Subject
    template_name = 'upskill/index.html'
    context_object_name = 'subjects'
    ordering = ['id']

    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        subject_slug = self.kwargs.get('subject_slug')
        
        courses = Course.objects.all()
        
        if subject_slug:
            courses = courses.filter(subject__slug = subject_slug)
        
        context['courses'] = courses
        
        
        return context
    
    
class AboutView(TemplateView):
    template_name = 'upskill/about.html'



class CourseView(TemplateView):
    template_name = 'upskill/course.html'
    
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context
    
    
class CourseDetail(DetailView):
    template_name = 'upskill/detail.html'
    queryset = Course.objects.all()
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        course = self.get_object()
        context =  super().get_context_data(**kwargs)
        context['modules'] = enumerate(course.modules.all(), start=1)
        return context
    

    

class ContentDetailView(DetailView):
    template_name = 'upskill/content_detail.html'
    context_object_name = 'content'
    model = Content
    



def download_file(request, content_id):
    content = get_object_or_404(Content, id=content_id)

    # faqat file bo‘lsa
    if content.content_type.model != 'file':
        raise Http404("Not a file content")

    file_item = content.item  # bu File model

    file_path = file_item.file.path
    file_name = os.path.basename(file_path)

    response = FileResponse(
        open(file_path, 'rb'),
        as_attachment=True,
        filename=file_name
    )
    return response