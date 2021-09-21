from django import forms
from .models import Question, subset, test
from django.forms import Textarea
from django.core.exceptions import ValidationError


class QuestionForm(forms.ModelForm):
    
    question_text = forms.CharField(max_length=200, required=False, widget=forms.Textarea)
    question_imagen = forms.ImageField(required=False)
    question_url = forms.CharField(required=False)
    subset = forms.ModelChoiceField(queryset= subset.objects.all(), empty_label="Selecciona un grupo de puntaje")

    class Meta:
        model = Question
        fields = ('question_text', 'question_imagen', 'question_url','subset')
  
    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("question_text")
        url = cleaned_data.get("question_url")
        imagen = cleaned_data.get("question_imagen")
        print("cleandataaa")
        if not text and not url and not imagen:                 
            raise ValidationError('Debes ingresar algo de encabezado')
        
        return self.cleaned_data    

class subsetForm(forms.ModelForm):

    class Meta:
        model = subset
        fields = ('name_subset','value')

class testForm(forms.ModelForm):

    class Meta:
        model = test
        fields = ('name_test','timer','isAvailable','cantidadDePreguntas')


    