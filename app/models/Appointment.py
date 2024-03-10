from django.db import models
from .User import User


RELATION_CHOICES = (
    ("1", "Self"),
    ("2", "Father"),
    ("3", "Mother"),
    ("4", "Wife"),
    ("5", "Husband"),
    ("6", "Son"),
    ("7", "Daughter"),
    ("8", "Brother"),
)

GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Others", "Others"),
)

BLOOD_GROUP = (
    ("1", "A+"),
    ("2", "A-"),
    ("3", "B+"),
    ("4", "B-"),
    ("5", "O+"),
    ("6", "O-"),
)

CONSULTAION_CHOICE = (
    ("online", "online"),
    ("offline", "offline"),
)

class Appointment(models.Model):
    appointment_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_id=models.CharField(max_length=25,primary_key=True,null=False)
    patient_name = models.CharField(max_length=255, blank=True)
    contact = models.CharField(max_length=13, blank=True)
    age = models.IntegerField()
    weight = models.IntegerField()
    date = models.DateField()
    slot_time = models.TimeField()
    relation = models.CharField(max_length = 20,choices = RELATION_CHOICES,default = '1')
    blood_group = models.CharField(max_length = 20,choices = BLOOD_GROUP,default = 'Male')
    gender = models.CharField(max_length = 20,choices = GENDER,default = '1')
    meet_link = models.CharField(max_length=255, blank=True,default="none")
    predicted_file = models.URLField(blank=True)
    symptoms = models.TextField()
    status = models.BooleanField(default=False)
    consultation=models.CharField(max_length = 20,choices = CONSULTAION_CHOICE,default = 'offline')
    doctor = models.ForeignKey(User, limit_choices_to={'user_type': 'doctor'}, on_delete=models.CASCADE, related_name='appointments_as_doctor')

    # appointment_id_slug=AutoSlugField(populate_from='appointment_id',
    #                      unique=True,null=True,default=None)

    def __str__(self):
        return self.appointment_id