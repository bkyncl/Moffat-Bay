from django.shortcuts import render, redirect
from django.contrib import messages
from account.forms import AccountForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('first_name') + " " + form.cleaned_data.get('last_name')
            messages.success(request, f'User account has been created for {name}!')
            return redirect('reservations-home')
    else:
        form = AccountForm()
    context = {
        'form':AccountForm,
    }
    return render(request, 'account/register.html', context)