# Mark Witt / Brittany Kyncl
# CSD-440: Capstone Project
# Moffat-Bay Lodge - Bravo Team

from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_required_message(view_func):
    @login_required(login_url='login')
    def _wrapped_view(request, *args, **kwargs):
        messages.info(request, 'Please login or register to continue.')
        return view_func(request, *args, **kwargs)
    return _wrapped_view