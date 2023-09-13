from django.db import models

# Create your models here.
class doctor(models.Model):
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    fees = models.DecimalField(max_digits=8, decimal_places=2)
    time = models.TimeField()
    room = models.CharField(max_length=10)
    image = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return self.name
    
class Speciality(models.Model):
    name= models.CharField(max_length=100)
    description = models.TextField( max_length=300 ,null=True, blank=True)

    def __str__(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    added = models.DateField()
    expiry = models.DateField()
    image = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    doctors = models.ForeignKey(doctor, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15,null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    doctor_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Contacting(models.Model):
    name = models.CharField(max_length=100, default='', blank=True)
    email = models.EmailField(default='', blank=True)
    message = models.CharField(max_length=500, default='', blank=True)

    def __str__(self):
        return self.name