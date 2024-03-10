from django.shortcuts import render, redirect
from app.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password

def signup(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST['username']
        phone = request.POST['phone']
        password = request.POST['password']
        password=make_password(password)

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('signup')
        
        # Create new user
        user = User.objects.create(username=username,phone=phone, password=password)
        
        
        messages.success(request, 'Account created successfully. You can now log in.')
        return redirect('signin')
    else:
        return render(request, 'signup.html')
