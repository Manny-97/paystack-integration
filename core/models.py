from django.db import models
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
        return f"Payment: {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref

        super().save(*args, **kwargs)

    def amount_save(self):
        return self.amount * 100

    def verify_payment(self):
        paystack = PayStack()
        breakpoint()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False