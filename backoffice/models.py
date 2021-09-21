from django.db import models
from django.contrib.auth.models import User 
from multiselectfield import MultiSelectField
"""

class test(models.Model):

    name_test = models.CharField(max_length=200)
    timer = models.IntegerField()
    #cantida de preguntas
    #fecha de creacion 
    def __str__(self):
        return self.name_test

class subset(models.Model):
    name_subset = models.CharField(max_length=30)
    value = models.IntegerField()

    def __str__(self):
        return self.name_subset


class Question(models.Model):

    question_text = models.CharField(max_length=200, null=True)
    question_imagen = models.ImageField(upload_to='test1/',null=True)
    question_url = models.CharField(max_length=200,null=True)
    score = models.ForeignKey(subset, on_delete=models.SET_NULL , null=True)
    test= models.ForeignKey(test, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_valid  = models.BooleanField()
    def __str__(self):
        return self.choice_text
    

class Feedback(models.Model):
    #user = models.ManyToManyField(User)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, related_name='Feedback' )
    totalscore = models.IntegerField()


class Answered(models.Model):    
    question = models.ForeignKey(Question,on_delete=models.SET_NULL, null=True)
    choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True)
    feedback = models.ForeignKey(Feedback,on_delete=models.CASCADE)


"""