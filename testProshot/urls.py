from django.urls import path
from testProshot import views


app_name = 'testProshot'

urlpatterns = [
  path('', views.listviewIndex.as_view(), name='index'),
  path('addSubset', views.Addsubset.as_view(), name='addSubset'),
  path('editSubset/<pk>', views.EditSubset.as_view(), name='editSubset'),
  path('deleteSubset/<pk>', views.deleteSubset.as_view(), name='deleteSubset'),
  path('addQuestion', views.addQuestion.as_view(), name ='addQuestion'),
  #path('addQuestion', views.AddQuestionn.as_view(), name ='addQuestion'),
  path('editTest/<pk>', views.editTest.as_view(), name ='editTest'),

  path('editQuestion/<pk>', views.editQuestion.as_view(), name ='editQuestion'),
  
  path('deleteQuestion/<pk>', views.deleteQuestion.as_view(), name ="deleteQuestion"),
  path('test/<int:test_id>', views.showQuestions, name ="testFotografico"),
  path('save', views.saveAnswers , name = 'save'),
  path('resultado/', views.test_certificate , name = "test_cert"),
  path('rendirtest/',views.rendirTest, name="rendirTest"),
  path('resultados/',views.listFeedbackView.as_view(), name="verResultados"),
  path('certificate/<int:id>', views.resultadoPdfView.as_view() , name = "certificatePDF"),

]
 