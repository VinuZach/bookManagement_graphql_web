from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(AuthorDetails)
admin.site.register(Books)
admin.site.register(Genre)