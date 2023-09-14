# Mark Witt / Brittany Kyncl
# CSD-440: Capstone Project
# Moffat-Bay Lodge - Bravo Team

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AccountForm, AccountUpdateForm, MailListForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

#Register new user view: if request is POST, checks if form is valid. if valid, saves form, redirects to login.
# if form is not valid, or request is not POST, renders register.html page with registration form. 
def register(request):
    if request.method == 'POST':
        # Check if the account form was submitted
        if 'register_submit' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                form.save()
                name = form.cleaned_data.get('first_name') + " " + form.cleaned_data.get('last_name')
                messages.success(request, f'User account has been created for {name}!', extra_tags='account-feedback')
                return redirect('login')
            else:
                messages.error(request, form.errors, extra_tags='account-feedback')
        # Check if the mail form was submitted
        elif 'mailform_submit' in request.POST:
            mailform = MailListForm(request.POST)
            if mailform.is_valid():
                mailform.save()
                messages.success(request, "Thank you for signing up for our mailing list!", extra_tags='mail_form')
                return redirect('register')


    # Retrieve messages and filter 'mail_form' messages
    mail_form_messages = messages.get_messages(request)
    mail_form_messages = [message for message in mail_form_messages if 'mail_form' in message.tags]
        
    context = {
        'form': AccountForm,
        'mailform': MailListForm,
        'title': 'Register New Account',
        'has_mailform_messages': mail_form_messages,
    }
    return render(request, 'users/register.html', context)

#View profile view - returns profile page, showing user account profile. Requires user to be logged in. 
@login_required
def profile(request):

    # ADD MAILIST FORM & LOGIC **************************************
    mailform = MailListForm(request.POST or None)
    if request.method == "POST":
        if mailform.is_valid():
            mailform.save()
            messages.success(request, "Thank you for signing up for our mailing list!", extra_tags='mail_form')
            return redirect('profile')

    # Retrieve messages and filter 'mail_form' messages
    mail_form_messages = messages.get_messages(request)
    mail_form_messages = [message for message in mail_form_messages if 'mail_form' in message.tags]

    context = {
        'title':'Your Profile',
        'mailform': MailListForm,
        'has_mailform_messages': mail_form_messages,
    }
    return render(request, 'users/profile.html', context)

#Update profile view - provides a form for users to update their profile, including address, phone, email. 
#if form is POST and valid, saves the new info to db. if not, renders the form on update_profile.html.
@login_required
def update_profie(request):
    if request.method == 'POST':
        # Check if the account form was submitted
        if 'change_profile_submit' in request.POST:
            form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, f'Your account information has been updated!', extra_tags='account-feedback')
                return redirect('profile')
            else:
                messages.error(request, form.errors, extra_tags='account-feedback')
        # Check if the mail form was submitted
        elif 'mailform_submit' in request.POST:
            mailform = MailListForm(request.POST)
            if mailform.is_valid():
                mailform.save()
                messages.success(request, "Thank you for signing up for our mailing list!", extra_tags='mail_form')
                return redirect('update_profile')
            else:
                form = AccountUpdateForm(instance=request.user)
    else:
        form = AccountUpdateForm(instance=request.user)

    # Retrieve messages and filter 'mail_form' messages
    mail_form_messages = messages.get_messages(request)
    mail_form_messages = [message for message in mail_form_messages if 'mail_form' in message.tags]

    context = {
        'form' : form,
        'mailform': MailListForm,
        'title': 'Update Profile',
        'has_mailform_messages': mail_form_messages,
    }

    return render(request, 'users/update_profile.html', context)

#Change password view - this will be the user changing their own password - available from the user's profile page
@login_required
def change_passowrd(request):
    if request.method == 'POST':
        if 'change_password_submit' in request.POST:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!', extra_tags='account-feedback')
                return redirect('profile')
            else:
                messages.error(request, form.errors, extra_tags='account-feedback')
                #NOTE: causing an error here.....**********

        elif 'mailform_submit' in request.POST:
            mailform = MailListForm(request.POST)
            if mailform.is_valid():
                mailform.save()
                messages.success(request, "Thank you for signing up for our mailing list!", extra_tags='mail_form')
                return redirect('profile')
            else:
                form = PasswordChangeForm(request.user)
    else:
        form = PasswordChangeForm(request.user)

    # Retrieve messages and filter 'mail_form' messages
    mail_form_messages = messages.get_messages(request)
    mail_form_messages = [message for message in mail_form_messages if 'mail_form' in message.tags]

    context = {
        'mailform': MailListForm,
        'form': form,
        'title':'Change your password',
        'has_mailform_messages': mail_form_messages,
    }
    return render(request, 'users/change_password.html', context)