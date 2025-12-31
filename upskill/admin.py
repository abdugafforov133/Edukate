from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import (
    Teacher,
    Subject,
    Course,
    Module,
    Content,
    Text,
    Video,
    File,
    Image
)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'expertise',
        'experience_years',
        'is_active',
        'created_at'
    )
    list_filter = ('is_active', 'expertise')
    search_fields = ('full_name', 'expertise')



@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1


class ContentInline(GenericTabularInline):
    model = Content
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'owner',
        'subject',
        'created_at'
    )
    list_filter = ('subject', 'created_at')
    search_fields = ('title', 'overview')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title',)
    inlines = [ContentInline]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('module', 'content_type', 'object_id')
    list_filter = ('content_type',)


class ItemBaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at')
    list_filter = ('owner',)
    search_fields = ('title',)


@admin.register(Text)
class TextAdmin(ItemBaseAdmin):
    pass


@admin.register(Video)
class VideoAdmin(ItemBaseAdmin):
    pass


@admin.register(File)
class FileAdmin(ItemBaseAdmin):
    pass


@admin.register(Image)
class ImageAdmin(ItemBaseAdmin):
    pass
