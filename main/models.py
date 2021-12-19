from django.db import models
from multiselectfield import MultiSelectField
# Create your models here.

class Patient(models.Model):
    name = models.CharField(max_length=50)    
    phone_num = models.CharField(max_length=15, null=True, blank=True)
    patient_relative_name = models.CharField(max_length=50, null=True)
    patient_relative_contact = models.CharField(max_length=15, null=True)
    address = models.TextField()
    SYMPTOMS = (
        ('Fever', 'Fever'),
        ('Dry cough', 'Dry cough'),
        ('Tiredness', 'Tiredness'),
        ('Aches and pains', 'Aches and pains'),
        ('Sore throat', 'Sore throat'),
        ('Diarrhoea', 'Diarrhoea'),
        ('Loss of taste or smell', 'Loss of taste or smell'),
        ('Difficulty in breathing or shortness of breath', 'Difficulty in breathing or shortness of breath'),
        ('Chest pain or pressure', 'Chest pain or pressure'),
        ('Loss of speech or movement', 'Loss of speech or movement'),
    )

    symptoms = MultiSelectField(choices=SYMPTOMS, null=True)
    prior_ailments = models.TextField()
    bed_num = models.ForeignKey("Bed", on_delete=models.CASCADE)
    dob = models.DateField(null=True)
    doctor = models.ForeignKey("Doctor", on_delete=models.CASCADE, null=True)
    doctors_notes = models.TextField(null=True, blank=True)
    doctors_visiting_time = models.CharField(null=True, max_length=50, blank=True)
    status = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
        
class Bed(models.Model):
    bed_number = models.CharField(max_length=50)
    occupied = models.BooleanField()
    def __str__(self):
        return self.bed_number


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Report(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, blank=True, null=True)
    # date = models.DateField(blank=True, null=True)
    test1 = models.CharField(max_length=50)
    desc1 = models.CharField(max_length=50)
    test2 = models.CharField(max_length=50)
    desc2 = models.CharField(max_length=50)
    test3 = models.CharField(max_length=50)
    desc3 = models.CharField(max_length=50)
    test4 = models.CharField(max_length=50)
    desc4 = models.CharField(max_length=50)
    test5 = models.CharField(max_length=50)
    desc5 = models.CharField(max_length=50)
    test6 = models.CharField(max_length=50)
    desc6 = models.CharField(max_length=50)
    test7 = models.CharField(max_length=50)
    desc7 = models.CharField(max_length=50)
    test8 = models.CharField(max_length=50)
    desc8 = models.CharField(max_length=50)
    test9 = models.CharField(max_length=50)
    desc9 = models.CharField(max_length=50)
    test10 = models.CharField(max_length=50)
    desc10 = models.CharField(max_length=50)

    def download_report(self):
        return int(self.id)