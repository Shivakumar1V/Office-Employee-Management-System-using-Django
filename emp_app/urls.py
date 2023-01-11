from django.urls import path
from emp_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all-emp', views.allEmp, name='all-emp'),
    path('add-emp', views.addEmp, name='add-emp'),
    path('remove-emp', views.removeEmp, name='remove-emp'),
    path('remove-emp/<int:empID>', views.removeEmp, name='remove-emp'),
    path('filter-emp', views.filterEmp, name='filter-emp'),
]
