from django.contrib import admin

# Register your models here.
from home.models import Friend, Post

admin.site.register(Post)
admin.site.register(Friend)
