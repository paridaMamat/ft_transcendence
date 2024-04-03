from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import User

# Create your views here.

# def home(request):
#     template = "website/home.html"
#     return render(request, template)

def user_first_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the already registered page upon successful login
            return redirect('already_registered')
        else:
            # Handle invalid login credentials (username or password)
            return render(request, 'user_first_page.html', {'error_message': 'Invalid username or password'})
    else:
        # Render the login page
        return render(request, 'user_first_page.html')
    
def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # Create a new User object
            user = User.objects.create(name=name, email=email, password=password)
            return JsonResponse({'success': True, 'message': 'User created successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    return render(request, 'login.html')  # Render the login form template for GET requests

def user_registration_page(request):
    # Add logic to handle user registration form submission here
    # For example, if the form is submitted via POST request, you can process the form data here
    if request.method == 'POST':
        # Process the form data
        pass  # Placeholder, replace with your actual logic
    return render(request, 'user_registration_page.html')

def already_registered(request):
    return render(request, 'already_registered.html')