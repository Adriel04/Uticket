from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from django import forms
from .models import User, nfc_Info

#auth

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def user_panel (request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to a login page if not logged in
    
    if request.user.id != user_id:
        return redirect('panel', user_id=request.user.id)

    # Get the NFC info for the user
    nfc_infos = nfc_Info.objects.filter(user_id=user_id).order_by('-date')

    # Calculate total credit
    total_credit = sum(info.credit for info in nfc_infos)
    
    return render(request, 'panel.html', {'user_id': user_id, 'credit': total_credit, 'history':nfc_infos})


# recharge function
@login_required
def recharge (request, user_id):
    if request.user.id != user_id:
        return redirect('panel', user_id=request.user.id)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = int(amount)
            if amount <= 0:
                messages.error(request, "The amount must be greater than zero.")
                return redirect('recharge', user_id=user_id)
            
            nfc_record = nfc_Info.objects.get(user_id=user_id)
            nfc_record.credit += amount
            nfc_record.save()
            
            messages.success(request, "Credit added successfully!")
            return redirect('panel', user_id=user_id)
        
        except ValueError:
            messages.error(request, "Invalid amount entered.")
            return redirect('recharge', user_id=user_id)
        # except nfc_Info.DoesNotExist:
        #     messages.error(request, "NFC record not found.")
        #     return redirect('panel', user_id=user_id)
    
    return render(request, 'recharge.html', {'user_id': user_id})



class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"