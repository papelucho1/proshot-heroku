from rest_framework import serializers

from .models import Person, Post, PostPicture

class PersonSerializer(serializers.ModelSerializer):
  posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

  class Meta:
    model = Person
    fields = (
      'id',
      'first_name',
      'last_name',
      'email',
      'phone',
      'city',
      'region',
      'instagram',
      'portafolio',
      'rutaImagen',
      'idioma',
      'categoriasEspecialidad',
      'disponibilidad',
      'status',
      'posts'
    )

class PostPictureSerializer(serializers.ModelSerializer): 
  class Meta:
    model = PostPicture
    fields = (
      'id',
      'post',
      'image'
    )
    
class PostSerializer(serializers.ModelSerializer):
  author = serializers.ReadOnlyField(source='author.first_name')
  pictures =  serializers.SlugRelatedField(many=True, read_only=True, slug_field='image')
  categoryName = serializers.ReadOnlyField(source="category.categoryName")
  colorCategory = serializers.ReadOnlyField(source="category.color")
  class Meta:
    model = Post
    fields = (
      'id',
      'author',
      'title',
      'content',
      'precontent',
      'created_on',
      'pictures',
      'categoryName',
      'colorCategory'
    )
