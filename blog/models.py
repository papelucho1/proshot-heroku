from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractUser, User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from proShot import settings
# Create your models here.
LENGUAGES_PERSON = (
  ('en', 'Inglés'),
  ('de', 'Alemán'),
  ('fr', 'Francés'),
  ('pt', 'Portugués'),
  ('ru', 'Ruso'),
)

ESPECIALIDAD_CATEGORY =(
  (1,'Matrimonio'),
  (2,'Fiesta'),
  (3,'Eventos Musicales'),
  (4,'Eventos Deportivos'),
  (5,'Mascota'),
  (6,'Fotografía de producto'),
  (7,'Fotografía aérea'),
)

DISPONIBILIDAD_CATEGORY =(
  (1, 'Full Time'),
  (2, 'Part Time'),
  (3, 'Casual'),
  (4, 'Fin de Semanas'),
  (8, 'Festivos'),
  (5, 'Mañanas'),
  (6, 'Tardes'),
  (7, 'Noches'),

)

REGION_CHILE = [
  ('XV', 'Arica y Parinacota'),
  ('I', 'Tarapacá'),
  ('II', 'Antofagasta'),
  ('III', 'Atacama'),
  ('IV', 'Coquimbo'),
  ('V', 'Valparaíso'),
  ('RM', 'Santiago'),
  ('VI', 'Libertador General Bernardo Ohiggins'),
  ('VII', 'Maule'),
  ('XVI', 'Ñuble'),
  ('VIII', 'Biobío'),
  ('IX', 'La Araucanía'),
  ('XIV', 'Los Ríos'),
  ('X', 'Los lagos'),
  ('XI', 'Aysen'),
  ('XII', 'Magallanes y Antártica')
]
GENERO_CHOICES = [
  ('Femenino', 'Femenino'),
  ('Masculino', 'Masculino'),
  ('No Binario', 'No Binario'),
  ('Otro', 'Otro')
]
'''
class User(AbstractUser):
  is_fotografo = models.BooleanField(default=False)

'''
class Person(models.Model):

    phone = models.IntegerField(null= True)
    city = models.CharField(max_length=30)
    region = models.CharField(max_length=40, choices=REGION_CHILE)
    genero =  models.CharField(
        max_length=20,
        choices=GENERO_CHOICES,
        default= 'Selecciona uno',
    )
    is_fotografo = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Fotografo(models.Model):
    instagram = models.CharField(max_length=50, null= True)
    #url con el portafolio
    portafolio = models.URLField()
    #insertar 3 imagenes que representen al fotografo (opcional)
    rutaImagen = models.FileField(null = True)
    #idioma que domina el fotografo
    idioma = MultiSelectField(choices=LENGUAGES_PERSON,  null=True)
    #categoria de las cuales maneja en fotografia
    categoriasEspecialidad = MultiSelectField(choices = ESPECIALIDAD_CATEGORY,  null=True)
    #disponibilidad 
    disponibilidad = MultiSelectField(choices = DISPONIBILIDAD_CATEGORY,  null=True)
    #status se refiere a que si está dentro del sistema o no 
    fotografo = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


COLORES = [   
  ('blue', 'blue'),
  ('indigo', 'indigo'),
  ('purple', 'purple'),
  ('pink', 'pink'),
  ('danger', 'danger'),
  ('orange', 'orange'),
  ('brown', 'brown'),
  ('warning', 'warning'),
  ('success', 'success'),
  ('info', 'info'),
  ('cyan', 'cyan')
] 

class postCategory(models.Model):
  categoryName = models.CharField(max_length=50)
  color = models.CharField(
        max_length=20,
        choices=COLORES,
        default= 'blue',
    )
  def __str__(self):
    return self.categoryName

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = RichTextField(blank=True, null=True )
    precontent = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    category = models.ForeignKey(postCategory, on_delete= models.CASCADE )

    class Meta:
      ordering = ['created_on']

    def __str__(self):
      return self.title

    def get_absolute_url(self):
      return reverse('blog:detail', args=(str(self.id)))



class PostPicture(models.Model):
  post = models.ForeignKey(Post, related_name='pictures', on_delete=models.CASCADE)
  image = models.ImageField(upload_to='blog/')
  image_name = models.CharField(blank=True, null=True, max_length=55, default='')

  #def __str__(self):
   # return self.post.title + self.image_name