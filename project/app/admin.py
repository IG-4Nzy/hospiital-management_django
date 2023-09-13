from django.contrib import admin
from .models import doctor, Speciality, Medicine, Appointment

admin.site.register(doctor)
admin.site.register(Speciality)
admin.site.register(Medicine)
admin.site.register(Appointment)