from django.contrib import admin
from .models import test, Question, subset, Choice, Feedback
# Register your models here.

admin.site.register(test)
admin.site.register(Question)
admin.site.register(subset)
admin.site.register(Choice)
admin.site.register(Feedback)