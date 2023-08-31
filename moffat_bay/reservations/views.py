from django.shortcuts import render, redirect
from account.forms import MailListForm

# Create your views here.
def home(request):
    mailform = MailListForm(request.POST or None)
    if request.method == "POST":
        if mailform.is_valid():
            mailform.save()
            return redirect('reservations-home')
    context = {
        'title':'Landing Page',
        'mailform': mailform,
    }
    return render(request, 'reservations/home.html', context)