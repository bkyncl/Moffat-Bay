from django.shortcuts import render, redirect
from django.contrib import messages
from account.forms import AccountForm, AccountUpdateForm
from django.contrib.auth.decorators import login_required

#Register new user view: if request is POST, checks if form is valid. if valid, saves form, redirects to login.
# if form is not valid, or request is not POST, renders register.html page with registration form. 
# ----NOTE: NEED TO HAVE REGISTRATION FORM SHOW AN ERROR TO USER IF EMAIL IS DUPLICATED.
#-----NOTE: MESSAGES ARE NOT DISPLAYING PROPERLY.
def register(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('first_name') + " " + form.cleaned_data.get('last_name')
            messages.success(request, f'User account has been created for {name}!')
            return redirect('login')
    else:
        form = AccountForm()
        
    context = {
        'form': AccountForm,
    }
    return render(request, 'account/register.html', context)

#View profile view - returns profile page, showing user account profile. Requires user to be logged in. 
@login_required
def profile(request):
    return render(request, 'account/profile.html')

#Update profile view - provides a form for users to update their profile, including address, phone, email. 
#if form is POST and valid, saves the new info to db. if not, renders the form on update_profile.html.
@login_required
def update_profie(request):
    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account information has been updated!')
            return redirect('profile')
    else:
        form = AccountUpdateForm(instance=request.user)

    context = {
        'form' : form
    }

    return render(request, 'account/update_profile.html', context)