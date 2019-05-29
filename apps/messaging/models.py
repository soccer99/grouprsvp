from django.db import models


class MO(models.Model):  # Incoming sms message
    phone_number = models.CharField(max_length=12)
    content = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class MTRequest(models.Model):  # Send message (before send)
    phone_number = models.CharField(max_length=12)
    content = models.TextField()
    aggregator_id = models.CharField(max_length=64, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class MTSent(models.Model):  # Send message (Status)
    phone_number = models.CharField(max_length=12)
    request = models.ForeignKey(MTRequest, on_delete=models.CASCADE)
    aggregator_id = models.CharField(max_length=64, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class SMSDR(models.Model):
    from_phone_number = models.CharField(max_length=12)
    to_phone_number = models.CharField(max_length=12)
    status = models.CharField(max_length=32)
    mt_request = models.ForeignKey(MTRequest, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class EmailMessage(models.Model):
    email = models.CharField(max_length=120)
    content = models.TextField(blank=True)
    template_id = models.CharField(max_length=120, blank=True, null=True)
