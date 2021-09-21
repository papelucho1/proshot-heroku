from django.contrib import admin

from .models import Post, PostPicture, Person, postCategory, Fotografo

class PostPictureAdmin(admin.StackedInline):
  model=PostPicture

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  inlines = [PostPictureAdmin]

  class Meta:
    model=Post

@admin.register(PostPicture)
class PostPictureAdmin(admin.ModelAdmin):
  pass

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
  class Meta:
    model=Person
# Register your models here.

admin.site.register(postCategory)
admin.site.register(Fotografo)

