from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .models  import  doctor,Speciality,Medicine,Appointment,Contacting
from datetime import date, datetime
from django.core.mail import send_mail


def home(request):
    return render(request,'home.html')

@login_required(login_url='admin_login')
def admin(request):
    return render(request, 'admin.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin')
        else:
            return render(request, 'adminlogin.html', {'key':'Account Not found'})

    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin')

    return render(request, 'adminlogin.html')
def Contact(request):
    if request.method == 'POST':
        cname = request.POST.get('name')
        email = request.POST.get('email')
        cmessage = request.POST.get('message')

        # Save the contact details to the database
        contact = Contacting(name=cname, email=email, message=cmessage)
        contact.save()

        # Send email to the user
        subject = 'Thank you for contacting us'
        message = 'You will get assistance from our team as soon as possible. For further information, please contact hospital@gmail.com'
        from_email = 'athulas733@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        # Send email to the admin
        subject = 'New Contact Message'
        message = f'Name: {cname}\nEmail: {email}\n\nMessage:\n{cmessage}'
        from_email = 'athulas733@gmail.com'
        recipient_list = ['athulkrishnanas321@gmail.com']
        send_mail(subject, message, from_email, recipient_list)

        return render(request, 'contconfirmation.html')

    return render(request, 'contact.html')
def doctors(request):
    doctors = doctor.objects.all()
    return render(request, 'doctors.html', {'doctors': doctors})


def pharmacy(request):

    medicines = Medicine.objects.all()
    return render(request, 'pharmacy.html', {'medicines': medicines})

def speciality(request):
    speciality = Speciality.objects.all()
    return render(request, 'speciality.html', {'specialities': speciality})

def log(request):
    return render(request,'home.html')

def about(request):
    return render(request,'aboutus.html')

def neuro(request):
    return render(request,'neuro.html')

def cancer(request):
    return render(request,'cancer.html')

def cardio(request):
    return render(request,'cardio.html')

def gastro(request):
    return render(request,'gastro.html')

def gyno(request):
    return render(request,'gyno.html')


@login_required
def Adddoctors(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        speciality_id = request.POST.get('speciality')
        fees = request.POST.get('fees')
        consulting_time = request.POST.get('time')
        room_number = request.POST.get('room')
        image = request.FILES.get('image')

        speciality = Speciality.objects.get(id=speciality_id)
        
        doctors = doctor(
            name=name,
            speciality=speciality,
            fees=fees,
            time=consulting_time,
            room=room_number,
            image=image
        )
        doctors.save()
        return redirect('admin')

    specialities = Speciality.objects.all()
    return render(request, 'adddoctors.html', {'specialities': specialities})

@login_required
def Addpharmacy(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        rate = request.POST.get('rate')
        description = request.POST.get('description')
        added_date = request.POST.get('added_date')
        expiry_date = request.POST.get('expiry_date')
        image = request.FILES.get('image')

        medicine = Medicine(name=name, rate=rate, description=description, added=added_date, expiry=expiry_date, image=image)
        medicine.save()
        return redirect('admin')
    
    return render(request,'addmedicine.html')
    

@login_required
def Addspeciality(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        speciality = Speciality(name=name, description=description)
        speciality.save()
        
        return redirect('admin') 
        
    return render(request, 'addspecialities.html')

def admin_logout(request):
    logout(request)
    return redirect('home')


def search(request):
    search_query = request.POST.get('search')
    medicines = []

    if search_query:
        medicines = Medicine.objects.filter(name__icontains=search_query)
        medicine = Medicine.objects.all()

    context = {
        'search': medicines,
        'search_query': search_query,
        'img': medicine
    }
    return render(request, 'medicine.html', context)


def buy_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        payment_option = request.POST.get('payment_option')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        phone_number = request.POST.get('phone_number')

        context = {
            'medicine': medicine
        }

        subject = 'Your Order is confirmed'
        message = f'Thank you for ordering {medicine.name}. Your order is on the way. For further information and assistance, please contact hospital@gmail.com'
        from_email = 'athulas733@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        return render(request, 'ordered.html', context)

    context = {
        'medicine': medicine
    }
    return render(request, 'buymedicine.html', context)

def ordered(request):
    return render(request,'ordered.html')


def book_appointment(request, doctor_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dat = request.POST.get('date')
        time = request.POST.get('time')
        dob = request.POST.get('dob')
        age = request.POST.get('age')

        try:
            dob_obj = datetime.strptime(dob, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'bookappointment.html', {'key': 'Invalid date of birth format. Please enter the date in YYYY-MM-DD format.'})

        today = date.today()
        age = today.year - dob_obj.year - ((today.month, today.day) < (dob_obj.month, dob_obj.day))

        if age < 1:
            return render(request, 'bookappointment.html', {'key': 'age error'})
        
        dat = datetime.strptime(dat, '%Y-%m-%d').date()
        if dat < today:
            return render(request, 'bookappointment.html', {'key': 'Please select a valid date in the future.'})
        
        dob = datetime.strptime(dob, '%Y-%m-%d').date()
        if dob > today:
            return render(request, 'bookappointment.html', {'key': 'Please select a valid date of birth.'})

        doctors = get_object_or_404(doctor, id=doctor_id)

        appointment = Appointment(name=name, email=email, phone=phone, date=dat, dob=dob, time=time, age=age, doctors=doctors)
        appointment.save()

        token_number = Appointment.objects.count()
        subject = 'Your appointment is confirmed'
        message = f'Thank you for taking an online appointment for consulting Dr. {doctors.name}. Your token number is {token_number}.'
        from_email = 'athulas733@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        context = {'token_number': token_number}
        return render(request, 'confirmation.html', context)

    return render(request, 'bookappointment.html')


def confirmation(request):
    return render(request, 'confirmation.html')

def view_doctors(request, speciality_id):
    speciality = get_object_or_404(Speciality, id=speciality_id)
    doctors = doctor.objects.filter(speciality=speciality)

    context = {
        'speciality': speciality,
        'doctors': doctors
    }
    return render(request, 'viewdoctors.html', context)

def contconfirmation(request):
    return render(request,'contconfirmation.html')