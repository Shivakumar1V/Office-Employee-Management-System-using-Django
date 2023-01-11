from django.shortcuts import render, HttpResponse, redirect
from emp_app.models import Employee, Department, Role
from django.contrib import messages
import json
from django.db.models import Q

# Create your views here.

def index(request):
    return render(request, 'index.html')

def allEmp(request):
    emps = Employee.objects.all()
    context = {
        'emps' : emps
    }
    return render(request, 'all_emp.html', context)

def addEmp(request):
    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        emp_dept = request.POST.get('department')
        emp_role = request.POST.get('role')
        salary = request.POST.get('salary')
        bonus = request.POST.get('bonus')
        phone = request.POST.get('phone_number')
        hire_date = request.POST.get('hire_date')
        if emp_dept == "department" or emp_role == "role":
            messages.warning(request, "Select Department and Role")
        else:
            dept = Department.objects.get(id=emp_dept)
            role = Role.objects.get(id=emp_role)
            emp = Employee(first_name=firstname, last_name=lastname, dept=dept, salary=salary, bonus=bonus, role=role, phone_num=phone, hire_date=hire_date)
            emp.save()
            messages.success(request, "Successfully added an employee")
            return redirect("/")
        return redirect("/add-emp")

    all_depts = Department.objects.all()
    all_roles = Role.objects.all()
    context = {
        'dept': all_depts,
        'role': all_roles
    }
    return render(request, 'add_emp.html', context)

def removeEmp(request, empID=None):
    if request.method == 'POST':
        if empID:
            emp = Employee.objects.get(emp_id=empID)
            emp.delete()
            messages.success(request, "Employee removed")
            return redirect("/")
        else:
            emp_id = int(request.POST.get('emp_id'))
            try:
                emp = Employee.objects.get(emp_id=emp_id)
                if emp:
                    response = json.dumps({'status':'success', 'empID':emp.emp_id, 'firstname':emp.first_name, 'lastname':emp.last_name, 'dept':emp.dept.name, 'location':emp.dept.location, 'salary':emp.salary, 'bonus':emp.bonus, 'role':emp.role.name, 'phone':emp.phone_num, 'hire_date':str(emp.hire_date)})
                    return HttpResponse(response)
            except:
                return HttpResponse('{"status":"not found"}')
    
    return render(request, 'remove_emp.html')


def filterEmp(request):
    if request.method == "POST":
        name = request.POST.get('name')
        dept = request.POST.get('department')
        role = request.POST.get('role')

        emp = Employee.objects.all()
        if name:
            emp = emp.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            dept = int(dept)
            emp = emp.filter(dept__id=dept)
        if role:
            role = int(role)
            emp = emp.filter(role__id=role)
            
        return render(request, 'all_emp.html', {'emps': emp}) 
            
    all_depts = Department.objects.all()
    all_roles = Role.objects.all()
    context = {
        'dept': all_depts,
        'role': all_roles
    }
    return render(request, 'filter_emp.html', context)

