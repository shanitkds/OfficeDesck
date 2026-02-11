from django.urls import path
from .views import ExpemseClimeRequestAPIView,ExpenceApprovelAPIView,SalaryAddAPIView,ViewUniqSalary
urlpatterns = [
    path('expence-create/',ExpemseClimeRequestAPIView.as_view(),name="expence-createv"),
    path('expence-action/<int:id>/',ExpenceApprovelAPIView.as_view(),name="expence-createv"),
    path('crete-update-salary/',SalaryAddAPIView.as_view(),name="crete-update-salary"),
    path('salary-uniq/<int:id>/',ViewUniqSalary.as_view(),name="salary-uniq"),
]