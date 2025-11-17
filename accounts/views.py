from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # automatically log them in
            return redirect('/')  # redirect to homepage
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})
