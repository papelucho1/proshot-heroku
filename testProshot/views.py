from django.shortcuts import render
from django.forms import formset_factory
from .forms import QuestionForm, subsetForm, testForm
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
from .models import Question, test, Choice, Feedback, Answered, subset
import json, random
from django.core import serializers
from django.views.generic import UpdateView, DeleteView, ListView, CreateView, View, TemplateView
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import PermissionRequiredMixin
import traceback
from statistics import mean

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


import os, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


def sendEmail(user):
    try:
        mailServer = smtplib.SMTP('smtp.gmail.com',587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        #settings.EMAIL_HOST_USER , settings.EMAIL_HOST_PASSWORD    
        mailServer.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
        
        # Construimos el mensaje simple
        mensaje = MIMEMultipart()

        mensaje['From']=settings.EMAIL_HOST_USER   #settings.EMAIL_HOST_USER 
        mensaje['To']="papelopez123@gmail.com"
        mensaje['Subject']="Tienes un correo"

        content = render_to_string('testAdmin/emailTest.html', {'user': user})
        mensaje.attach(MIMEText(content,"html"))
        mailServer.sendmail(settings.EMAIL_HOST_USER, #settings.EMAIL_HOST_USER
                "papelopez123@gmail.com",
                mensaje.as_string())
    except Exception as e:
        print(e)
    




def index(request):
    return render(request, "test/base.html")

@method_decorator([login_required,staff_member_required], name='dispatch')
class listviewIndex(ListView):
    model = Question
    template_name = "test/mantenedor.html"
    context_object_name = 'questions'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        #context['formTest'] = formTest(test.objects.get(pk=1))
        context['subset'] = subset.objects.all()
        context['test'] = test.objects.get(pk=1)
        context['answers'] = Choice.objects.all()
        context['validarTest'] = validarTest()
        return context

@method_decorator([login_required,staff_member_required], name='dispatch')
class editTest(UpdateView):    
    model= test
    form_class = testForm
    template_name = "test/CRUD/test/testEdit.html" 
    success_url = reverse_lazy('testProshot:index')

#subset 
@method_decorator([login_required,staff_member_required], name='dispatch')
class Addsubset(CreateView):
    model = subset
    form_class = subsetForm
    template_name = "test/CRUD/subset/addSubset.html"    
    success_url = reverse_lazy('testProshot:index')

@method_decorator([login_required,staff_member_required], name='dispatch')
class EditSubset(UpdateView):    
    model= subset
    form_class = subsetForm
    template_name = "test/CRUD/subset/editSubset.html"    
    success_url = reverse_lazy('testProshot:index')

@method_decorator([login_required,staff_member_required], name='dispatch')
class deleteSubset(DeleteView):
    model= subset
    template_name = "test/CRUD/subset/deleteSubset.html"
    success_url = reverse_lazy('testProshot:index')


@method_decorator([login_required,staff_member_required], name='dispatch')
class addQuestion(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "test/CRUD/question/addQuestion.html"    
    success_url = reverse_lazy('testProshot:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formQuestion"] =  QuestionForm()
        return context    

    def post(self, request, *args, **kwargs):
        data ={}
        try:
            print("agregando nueva pregunta")
            #print('request.post ',request.POST)
            formQuestion = QuestionForm(request.POST, request.FILES or None)
            if formQuestion.is_valid():
                print(" fomr valido")
                questionText = formQuestion.cleaned_data['question_text']
                questionUrl = formQuestion.cleaned_data['question_url']
                questionImage = formQuestion.cleaned_data['question_imagen']
                score = formQuestion.cleaned_data['subset']
                newquestion = Question(question_text= questionText, question_url=questionUrl, question_imagen=questionImage, score= score,test=test.objects.get(pk=1))
                newquestion.save()

                radios = json.loads(request.POST.get('radios'))       
            
                for elements in radios:
                        addAnswers = Choice(question = newquestion,  choice_text=elements[1] , is_valid = elements[2] )
                        addAnswers.save()
                print(" pregunta agregadaa")
            else:
                data['error'] = formQuestion.errors.as_json()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
                # aqui falta guardar las respuestas para la pregunta
""" 
                antes usaba el AJAX para agregar las respuestas, me funcionmaba bien pero al momento 
                de editar las respuestas asociadas a todo, me iba a la B
                    radios = json.loads(request.POST.get('radios'))
                    print(type(radios))
                    print(radios)
                    for elements in radios:
                        print(elements[1])
                        addAnswers = Choice(question = newquestion,  choice_text=elements[1] , is_valid = elements[2] )
                        addAnswers.save()
                    ser_newquestion = serializers.serialize('json', [ newquestion, ])
                    return JsonResponse({ 'newquestion': ser_newquestion}, status=200)

              
                                              
                return HttpResponseRedirect(reverse_lazy('testProshot:index'))
            return render(request, 'test/CRUD/question/addQuestion.html', {'formQuestion': formQuestion})
        except Exception as e:
            data['error'] = str(e)
 """


#questions

        
@method_decorator([login_required,staff_member_required], name='dispatch')
class editQuestion(UpdateView):

    model = Question
    form_class = QuestionForm
    template_name = 'test/CRUD/question/editQuestion.html'
    success_url = reverse_lazy('testProshot:index')

   
    
    def get_context_data(self, **kwargs):
        print("getContext editar custion")
        context = super().get_context_data(**kwargs)
        #context["questions"] = Question.objects.all() 
        print(Choice.objects.filter(question= self.get_object()))
        context['alternativas'] = Choice.objects.filter(question= self.get_object())

      

      
        return context 





@method_decorator([login_required,staff_member_required], name='dispatch')
class deleteQuestion(DeleteView):
    model= Question
    template_name = "test/CRUD/question/deleteQuestion.html"
    success_url = reverse_lazy('testProshot:index')



#Questionario
@login_required
def showQuestions(request,test_id):
    try: 
        TEST = test.objects.get(pk = test_id)
    except(KeyError, TEST.DoesNotExist):
        raise Http404
    else:    
        new_test = Feedback()
        new_test.totalscore = 0 
        new_test.user = request.user
        new_test.save()   
        #new_test.user.add(request.user)
        #new_test.user.add(User.objects.get(id=1))
        request.session['ID_TEST'] = new_test.id
        lista = []

        i = 0
        print("antes de seleccionar preguntas")
         # seleccionar la cantidad de preguntas menor por subconjuntos        
        while i < 2: #se tiene que colocar la cantidad de preguntas que se quiere obtener
            #ne este caso sería una por categoría
            for subsets in subset.objects.all():          
                questions = Question.objects.values_list('id', flat=True).filter(score=subsets).order_by('?').first()
                print(f"se saco la siguiente pregunta random {questions}")
                #for elements in questions:
                while Question.objects.get(pk=questions) in lista:
                    # salir del loop 
                    print(f" la pregunta ya esta en la lista {questions}")
                    questions = Question.objects.values_list('id', flat=True).filter(score=subsets).order_by('?').first()
                lista.append(Question.objects.get(pk=questions))
                new_answered =  Answered(feedback= new_test, question=Question.objects.get(pk=questions))
                new_answered.save()
            i+=1

            #questions = Question.objects.values_list(id, flat=True).order_by('?')[:2]
            #questions.values_list(id, flat=True)
            #lista.append(questions)
           
            #for question in Question.objects.filter(score = subsets):
                #print(question.order_by('?')[:1])
                #print(type(question))

        #questions = Question.objects.all()
    
        """      
        for element in lista:
            print(element)
            new_answered =  Answered(feedback= new_test, question=Question.objects.get(pk=element))
            new_answered.save()

        """    
        #for preguntas in Answered.objects.filter(feedback=new_test):
        #    print( " preguntas.question " , preguntas.question)
            
        #asdf = Question.objects.filter(pk=lista)
        #print("asdf",asdf)
 
            
        print(Answered.objects.filter(feedback=new_test))
        #print('filtrado de preguntas', Question.objects.filter(id= lista))
        testin = Answered.objects.filter(feedback=new_test)
        #print(Answered__question.values())
        answers = Choice.objects.all()
        #questions = Question.objects.order_by('?')[:4]
        #MyModel.objects.order_by('?')[:2]
        #questions = Question.objects.all()

        context = {
            'test': TEST,
            'questions' : questions,
            'answers'   : answers,
            'lista' : lista,
            'new_answered' : Answered.objects.filter(feedback=new_test),
            #'last_question' : Question.objects.last(),
        }
        
        return render(request ,'test/questionary.html',context )



    
@login_required
def saveAnswers(request):
    try:
        #owner = User.objects.get(pk=1)
        print("guardando respuestas!")
        answer_id = request.session['ID_TEST']
        this_answer = Feedback.objects.get(pk=answer_id)        
    except (KeyError, Feedback.DoesNotExist):
        raise Http404
    else:       
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            totalscore = 0
            #----depurar
            #------------
            print("guardando respuestas POST!")

            try:        
                for i in range(Question.objects.first().id , Question.objects.last().id + 1 ):
                    try:
                        choiced = Choice.objects.get(pk=request.POST.get("radio_"+ str(i)))
                    except ObjectDoesNotExist:
                        continue
                    else:
                        if choiced.is_valid is True:
                            print(Question.objects.get(pk=i))
                            print('la espuesta es true')
                            print(Question.objects.get(pk=i).score.value)
                            totalscore += Question.objects.get(pk=i).score.value    
                        elif choiced is None:
                            print(Question.objects.get(pk=i))
                            print('la respuesta es falsa')
                            continue
                        else:
                            continue
                        #guardar respuesta
                        respondido = Answered(question = Question.objects.get(pk=i), choice = Choice.objects.get(pk=request.POST.get("radio_"+ str(i))), feedback = this_answer)
                        respondido.save()
                this_answer.totalscore = totalscore
                this_answer.save()
                print(this_answer.user)
                #this_answer.status = 2
                #this_answer.save()
                #sendEmail(this_answer.user)
                return HttpResponseRedirect(reverse('testProshot:test_cert'))
                
                #return HttpResponseRedirect(reverse('testProshot:test_cert', args=(this_answer.user,)))
            except Exception as e:
                print (type(e))
                trace_back = traceback.format_exc()
                message = str(e)+ " " + str(trace_back)
                print (message)
                raise Http404
        else:
            raise Http404
@login_required
def test_certificate(request):
        #return render(request, 'certificate/body_BARRAT_certificate.html', context)
    

        lastFeedback = Feedback.objects.filter(user=request.user).last()
        if lastFeedback is None:
            return render(request, "test/feedback.html",{'test_not_Ready':True})

  
        respuestas = Answered.objects.filter(feedback=lastFeedback)
        resultado = Feedback.objects.get(pk=lastFeedback.id)
        choices = Choice.objects.all()
        subconjuntos = subset.objects.all()
        prueba = test.objects.get(pk=1)
        contadorSubconjunto= []
        i =0
        for respondido in respuestas:
            if respondido.choice:
                print(respondido.question.score)
                print(subset.objects.get(pk= respondido.question.score.id).value)
                print(respondido.choice)
                contadorSubconjunto.append(subset.objects.get(pk= respondido.question.score.id).id)
            else: 
                print("respuesta vacia")
            #print(respondido.choice)
        listaPuntaje = []
        listaGrupo = []

        for grupo in subconjuntos:
            print("subet", grupo.id)
            print(contadorSubconjunto.count(grupo.id))
            listaPuntaje.insert(grupo.id, contadorSubconjunto.count(grupo.id))
            listaGrupo.insert(grupo.id, grupo)
        
        print("###########lista puntaje##################")
        print("###########lista puntaje##################")
        print(listaPuntaje)
        print("###########lista puntaje##################")
        print("###########listaGrupo##################")
        print(listaGrupo)
        print("###########listaGrupoe##################")
        zipped = zip(listaGrupo, listaPuntaje)


        """
        for grupo in subconjuntos:
            for respondido in respuestas:
                if respondido.choice.is_valid and respondido.question.score.pk == grupo.pk:
                    #contadorSubconjunto[grupo.pk] = +1 
                    print('subconjunto -> ', grupo.name_subset)
                    #contadorSubconjunto2(grupo.name_subset) = i
                    #i=+1
                    contadorSubconjunto.append(grupo.pk)
                else:
                    continue
        for grupo in subconjuntos:
            print(contadorSubconjunto.count(grupo.pk))
        """
        print(type(respuestas))
        context ={
            'respuestas': respuestas,
            'feedback' : resultado,
            'prueba' : prueba,
            'resultado' : choices,
            'listaPuntaje' : listaPuntaje,
            'subconjuntos' : subconjuntos,
            'contadorSubconjunto':contadorSubconjunto,
            'zipped' : zipped,

        }
        return render(request, "test/feedback.html", context)

@login_required
def rendirTest(request):
    prueba = test.objects.get(pk=1)
    questions = Question.objects.filter(test=prueba)
    context = {
        'test' : prueba,
        'questions' : questions,
        'validarTest' : validarTest(),
    }
    return render(request, "test/dartest.html",context)


@login_required
def verResultados(request):
    return render(request, "testAdmin/resultados.html")

def validarTest():
    for subsets in subset.objects.all(): 
        if not Question.objects.filter(score=subsets):
            print('validartest Falso')
            return False
            break
    return True

@method_decorator([login_required,staff_member_required], name='dispatch')
class listFeedbackView(ListView):
    model = Feedback
    template_name = "test/resultados.html"
    context_object_name = 'feedback'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        #attrs = mean([o.totalscore for o in Feedback])
        context['test'] = test.objects.get(pk=1)
        #agragr exception mean
        try:
            mediaResultados = mean([o.totalscore for o in Feedback.objects.all()])
        except Feedback.DoesNotExist:
            mediaResultados = 0
        context['mediaResultados'] = mediaResultados
        return context








@method_decorator([login_required], name='dispatch')
class resultadoPdfView(View):
    def link_callback(self, uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path

    def get(self, request, *args, **kwargs):
        try:
            template_path = 'test/resultPDF.html' 
            context = {
                'title': 'this is your template context'
                #AGregar mas variables para la generacion del template
                }
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)

            # create a pdf
            pisa_status = pisa.CreatePDF(
                html, 
                dest=response,
                link_callback= self.link_callback)
         
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('testProshot:rendirTest'))
        