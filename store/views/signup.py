from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from store.models.product import Product
from store.models.category import Category
from store.models.customer import Customer
from django.views import View



class Signup(View):

    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        error_msg = None
        if request.method == "GET":
            return render(request, 'signup.html')
        else:
            postData = request.POST
            print(request.POST)
            first_name = postData.get('firstname')
            last_name = postData.get('lastname')
            phone = postData.get('phone')
            email = postData.get('email')
            password = postData.get('password')

            customer = Customer(first_name=first_name,
                                    last_name=last_name,
                                    phone=phone,
                                    email=email,
                                    password=password)

            error_msg = self.validateCustomer(customer)

            
            value = {'first_name' : first_name,
                    'last_name' : last_name,
                    'phone' : phone,
                    'email' : email}

            if not error_msg:
                
                customer.password = make_password(customer.password)
                customer.register()
                return redirect('homepage')

            else:
                data = {'error' : error_msg,
                        'values' : value}
                return render(request, 'signup.html', data)


    def validateCustomer(self, customer):
        error_msg = None
        if(not customer.first_name):
            error_msg = "First Name is Required"
        elif(not customer.last_name):
            error_msg = "Last Name is Required"
        elif(not customer.phone):
            error_msg = "Phone is Required"
        elif(not customer.email):
            error_msg = "Email is Required"
        elif customer.emailExists():
            error_msg = "Email Already Exists"

        return error_msg