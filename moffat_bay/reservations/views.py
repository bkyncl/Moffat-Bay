from django.shortcuts import render, redirect
from account.forms import MailListForm
from django.contrib import messages

# Create your views here.
def home(request):
    mailform = MailListForm(request.POST or None)
    if request.method == "POST":
        if mailform.is_valid():
            mailform.save()
            messages.success(request, "Thank you for signing up for our mailing list!")
            return redirect('reservations-home')
    context = {
        'title':'Landing Page',
        'mailform': mailform,
    }
    return render(request, 'reservations/home.html', context)