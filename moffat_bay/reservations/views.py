from django.shortcuts import render, redirect
from users.forms import MailListForm
from django.contrib import messages
from django.urls import reverse
from django.views.generic import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import NightlyCostPriceUpdateForm, NightlyCostPriceChangeForm
from .models import Stay_Costs
from .utilities import *

#main landing page view:
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

#about us page view:
def about(request):
    mailform = MailListForm(request.POST or None)
    #add any extra logic needed here
    context = {
        'title':'About The Lodge',
        'mailform': mailform,
        #add anything else we want returned and displayed on about page here
    }
    return render(request, 'reservations/about_us.html', context)


#add additional site views here (about, reservations, etc)


#Custom admin page views:
#Nightly Cost Price update by percentage View:
# *** this is located in the admin page****
class NightlyCostPriceUpdateView(FormView):
    form_class = NightlyCostPriceUpdateForm
    template_name = 'reservations/admin/nightly_cost_update.html'
    permission_required = ['user.is_admin']

    def form_valid(self, form):
        percentage = form.cleaned_data['costChange']
        # get product ids from url
        product_ids = self.request.GET.get('id').split(',')
        # Get the selected products
        products = Stay_Costs.objects.filter(id__in=product_ids)
        for product in products:
            product.price = product.price + (product.price * percentage / 100)
            product.save()
        messages.success(self.request, ('Prices updated successfully'))
        return redirect('/admin/reservations/stay_costs')

    def form_invalid(self, form):
        #display error if form is not valid
        messages.error(self.request, ('Error updating prices'))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        #add context data
        context = super().get_context_data(**kwargs)
        context['title'] = ('Update Moffat-Bay Prices')
        context['label'] =('Please enter percentage of price change:')
        context['form_url'] = reverse('price_update')

        # get product ids from url
        product_ids = self.request.GET.get('id').split(',')
        context['stay_costs'] = Stay_Costs.objects.filter(id__in=product_ids)
        return context
    
    #change prices by directly entering the price
class NightlyCostPriceChangeView(FormView):
    form_class = NightlyCostPriceChangeForm
    template_name = 'reservations/admin/nightly_cost_update.html'
    permission_required = ['user.is_admin']

    def form_valid(self, form):
        newCost = form.cleaned_data['costChange']
        # get product ids from url
        product_ids = self.request.GET.get('id').split(',')

        # Get the selected products
        products = Stay_Costs.objects.filter(id__in=product_ids)
        for product in products:
            product.price = newCost
            product.save()
        messages.success(self.request, ('Prices updated successfully'))
        return redirect('/admin/reservations/stay_costs')

    def form_invalid(self, form):
        """
        Display an error message if the form is invalid.
        """
        messages.error(self.request, ('Error updating prices'))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        #add context data
        context = super().get_context_data(**kwargs)
        context['title'] = ('Update Moffat-Bay Prices')
        context['form_url'] = reverse('price_change')
        context['label'] =('Please enter new price:')

        # get product ids from url
        product_ids = self.request.GET.get('id').split(',')
        context['stay_costs'] = Stay_Costs.objects.filter(id__in=product_ids)
        return context