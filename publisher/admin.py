from django.contrib import admin
from .models import Image, Video, Len, Camera, Review

# Register your models here.
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Len)
admin.site.register(Camera)
admin.site.register(Review)