from django.contrib import admin
from videos.models import (Videos, Categories, VideoCategoriesThrough, Tags, VideoTagsThrough)




class VideoCategoriesThroughInLine(admin.TabularInline):
    model = VideoCategoriesThrough
    extra = 1

class VideoTagsThroughInLine(admin.TabularInline):
    model = VideoTagsThrough
    extra = 1

@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    inlines = [VideoCategoriesThroughInLine, VideoTagsThroughInLine]

admin.site.register(Categories)
admin.site.register(Tags)