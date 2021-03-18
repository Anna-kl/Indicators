from django.contrib import admin
from .models import dayOfWorks, conctereDays, Tokens

# Register your models here.
admin.site.register(dayOfWorks)
admin.site.register(conctereDays)
admin.site.register(Tokens)
