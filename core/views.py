from django.shortcuts import render
from . import forms
# Create your views here.


def initiate_payment(request):
    if request.method == 'POST':
        payment_form = forms.PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save()

            render(request, 'make_payment.html', {'payment': payment})

    else:
        payment_form = forms.PaymentForm()

    return render(request, 'initiate_payment', {'payment_form': payment_form})