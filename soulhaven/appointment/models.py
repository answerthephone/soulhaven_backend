from django.db import models


class Appointment(models.Model):
    """
    Stores appointment requests made by users via the homepage.

    Fields:
    - full_name: The full name of the person requesting the appointment.
    - phone_number: Contact number for the requester.
    - sent_at: Timestamp automatically set when the appointment is created.

    Methods:
    - __str__(): Returns a human-readable string with the name and phone number.
    """
    full_name = models.CharField("ФИО", max_length=100)
    phone_number = models.CharField("Номер телефона", max_length=20)
    sent_at = models.DateTimeField("Дата отправки", auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"