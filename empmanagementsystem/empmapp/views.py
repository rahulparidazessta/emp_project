
from django.http import HttpRequest, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Employee
from .models import Department
from .models import AttendenceDetails
from .serializers import *
from .forms import EmployeeForm ,DepartmentForm
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Count




# # Create your views here.
def home(request):
    return render(request,'home.html')

def loginpage(request):
    return render(request, 'login.html')

#Basic authentication
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(request.POST.get('password'))
        # print(request.POST.get('username'))
        # print(request.user.username)
        # print(request.user.password)
        

        #print("Username: ",username, "Password: " ,password)

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username not found!")
            return redirect('/loginPage/')
        
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Password is wrong try again !")
            return redirect('/loginPage/')
        else:
            login(request, user)
            return redirect('/')
 
 #token authenticataion 
class Registeradmin(APIView):
    def post(self,request):
        serializer = userSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        user = User.objects.get(username= serializer.data['username'])
        token_obj, _ = Token.objects.get_or_create(user=user)
       
        return JsonResponse({'result': 'success', 'message': 'Login successful', 'token':str(token_obj)})


@login_required(login_url='/loginPage/')
@api_view(['GET'])
def employee_list(request):
    # Fetch all employees
    employees = Employee.objects.all()

    # Serialize the employee data
    serializer = EmployeeSerializerDisplay(employees, many=True)
    serialized_data = serializer.data

    # Annotate each department with the count of employees
    department_employee_counts = Department.objects.annotate(total_employees=Count('employees'))

    # Create a dictionary to store department names and total employee counts
    department_info = {}
    for department in department_employee_counts:
        department_info[department.Name] = department.total_employees

    # Pass both employee data and department information to the template context
    context = {
        'employees': serialized_data,
        'department_info': department_info,
    }

    # Render the template with the provided context
    for name, count in department_info.items():
        print(f"Department: {name}, Total Employees: {count}")

    return render(request, 'employe_details.html', context)



@login_required(login_url='/loginPage/')
@api_view(['GET'])
def department_list(request):
    departments = Department.objects.all()
    serializer = DepartmentSerializer(departments, many=True)
    serialized_data = serializer.data
    return render(request, 'department.html', {'departments': serialized_data})

@login_required(login_url='/loginPage/')
@api_view(['GET'])
def attendence_details(request):
    attendence = AttendenceDetails.objects.all()
    serializer = AttendenceDetailsSerializer(attendence, many=True)
    serialized_data = serializer.data
    print(serialized_data)
    return render(request, 'attendence_details.html', {'attendence': serialized_data})

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#CRUD OPERATION
#This function is meant for adding the new employees to the table
# def add_employee(request):
#     if request.method == 'POST':
#         form = EmployeeForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('employedetails/')  # Redirect to a view displaying the list of employees
#     else:
#         form = EmployeeForm()

#     # Assuming you have a Department model, pass the departments to the template
#     departments = Department.objects.all()

#     return render(request, 'add_employee.html', {'form': form, 'departments': departments})


# #METHOD BASED API
@api_view(['GET', 'POST'])
def add_employee(request):
    if request.method == 'POST':
        # print("we are here")
        serializer = EmployeeSerializerDisplay(data=request.data)
        if serializer.is_valid():
            #print("inside serializer")
            serializer.save()
            return redirect('employedetails/')
        return Response(serializer.errors, status=400) 

    elif request.method == 'GET':
        # Assuming you have a Department model, pass the departments to the template
        departments = Department.objects.all()
        return render(request, 'add_employee.html', {'departments': departments})

    else:
        return Response({'error': 'Method not allowed'}, status=405)  # Method Not Allowed


#Add with bulk_crate() method by which we can add multiple employee at a time 
# @api_view(['GET', 'POST'])
# def add_employee(request: HttpRequest):  # Ensure you're importing HttpRequest from django.http
#     if request.method == 'POST':
#         # Check if the request data contains a single employee or multiple employees
#         if isinstance(request.data, list):  # If the request data is a list, it contains multiple employees
#             employees_data = request.data
#         else:  # If the request data is not a list, assume it contains a single employee
#             employees_data = [request.data]

#         # Serialize each employee data and create Employee objects
#         employees = []
#         for employee_data in employees_data:
#             serializer = EmployeeSerializerDisplay(data=employee_data)
#             if serializer.is_valid():
#                 employees.append(Employee(**serializer.validated_data))
#             else:
#                 return Response(serializer.errors, status=400)  # Bad Request

#         # Bulk create the Employee objects
#         Employee.objects.bulk_create(employees)

#         return redirect('employedetails/')  # Redirect to employee details page

#     elif request.method == 'GET':
#         # Assuming you have a Department model, pass the departments to the template
#         departments = Department.objects.all()
#         return render(request, 'add_employee.html', {'departments': departments})

#     else:
#         return HttpResponseNotAllowed(['GET', 'POST']) 
    

#CLASS BASED VIEWS api
# class add_employee(APIView):
#     def get(self, request, *args, **kwargs):
#         # Assuming you have a Department model, pass the departments to the template
#         departments = Department.objects.all()
#         return render(request, 'add_employee.html', {'departments': departments})

#     def post(self, request, *args, **kwargs):
#         # Use EmployeeSerializer for both request data and response data
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return redirect('employedetails/')
#         return Response(serializer.errors, )

#     def put(self, request, *args, **kwargs):
#         return Response({'error': 'Method not allowed'}, )

#     def delete(self, request, *args, **kwargs):
#         return Response({'error': 'Method not allowed'}, )



def delete_employee(request, email):
    employee = get_object_or_404(Employee, email=email)

    if request.method == 'POST':
        employee.delete()
        return HttpResponseRedirect('/employee_details')  # Redirect to employee details page

    return render(request, 'delete_employee.html', {'employee': employee})

def confirm_delete_employee(request, email):
    employee = get_object_or_404(Employee, email=email)

    if request.method == 'POST':
        employee.delete()
        return HttpResponseRedirect('/add/employedetails/')  # Redirect to employee details page

    return render(request, 'employee_deleteemp.html', {'employee': employee})




# @api_view(['GET', 'POST'])
# def edit_employee(request, email):
#     employee = get_object_or_404(Employee, email=email)

#     if request.method == 'POST':
#         form = EmployeeForm(request.POST, instance=employee)
#         if form.is_valid():
#             form.save()
#             print("Before")
#             return HttpResponseRedirect('/employee_details')  # Redirect to employee details page
#     else:
#         form = EmployeeForm(instance=employee)

#     return render(request, 'edit_employee.html', {'form': form, 'employee': employee})
# @api_view(['GET', 'POST'])
# def edit_employee(request, email):
#     employee = get_object_or_404(Employee, email=email)

#     if request.method == 'POST':
#         form = EmployeeForm(request.POST, instance=employee)
#         if form.is_valid():
#             # Extract updated data from the form's cleaned_data
#             updated_data = {
#                 'Name': form.cleaned_data['Name'],
#                 'salary': form.cleaned_data['salary'],
#                 'department': form.cleaned_data['department'],
                
#             }

#             # Perform bulk update
#             Employee.objects.filter(email=email).update(**updated_data)
            
#             print("Before")
#             return HttpResponseRedirect('/employee_details')  # Redirect to employee details page
#     else:
#         form = EmployeeForm(instance=employee)

#     return render(request, 'edit_employee.html', {'form': form, 'employee': employee})


def edit_employee(request, email):
    employee = get_object_or_404(Employee, email=email)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('/employee_details')  # Assuming 'Employees' is the URL name for the employee list page
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'edit_employee.html', {'form': form, 'employee': employee})

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#CRUD FOR DEPT MANAGEMENT

# def add_department(request):
#     if request.method == 'POST':
#         form = DepartmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('department_details/')  # Redirect to a view displaying the list of employees
#     else:
#         form = DepartmentForm()

#     # Assuming you have a Department model, pass the departments to the template
#     departments = Department.objects.all()

#     return render(request, 'add_dept.html', {'form': form, 'departments': departments})


@api_view(['GET', 'POST'])
def add_department(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        serializer = DepartmentSerializer(data=request.data)
        
        if serializer.is_valid() :
            #print("serializer is valid")
            serializer.save()
            return redirect('department_details/')  # Redirect to a view displaying the list of departments
        else:
            # Handle form validation errors
            return render(request, 'add_dept.html', {'form': serializer, 'errors': serializer.errors})

    elif request.method == 'GET':
        serializer = DepartmentSerializer(departments, many=True)
        return render(request, 'add_dept.html', {'form': serializer.data, 'departments': departments})


    else:
        return Response({'error': 'Method not allowed'}, status=405)  # Method Not Allowed
    
# @api_view(['DELETE'])
# def delete_department(request, department_id):
#     # Get the department instance
#     department = get_object_or_404(Department, id=department_id)

#     if request.method == 'DELETE':
#         department.delete()
#         return Response({'message': 'Department deleted successfully'}, status=204)
#     else:
#         return Response({'error': 'Method not allowed'}, status=405)  # Method Not Allowed
