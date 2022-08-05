from django.db import models
from django.urls import reverse
import secrets
from .paystack import PayStack
# Create your models here.


class Payment(models.Model):
    # full_name = models.CharField(max_length=40)
    # last_name = models.TextField(max_length=250)
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref).first()
            if not object_with_similar_ref:
                self.ref = ref

        super().save(*args, **kwargs)

    def amount_save(self):
        ans = self.amount * 100
        return ans

    def verify_payment(self):
        paystack = PayStack()

        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            self.paystack_response = result
            if result['amount']/100 == self.amount:
                self.completed = True
            self.save()
        
            return True
        return False