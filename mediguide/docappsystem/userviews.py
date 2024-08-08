from django.shortcuts import render,redirect,HttpResponse
from dasapp.models import DoctorReg,Specialization,CustomUser,Appointment,Page
import random
from datetime import datetime
from django.contrib import messages
from django.core.mail import send_mail
def USERBASE(request):
    
    return render(request, 'userbase.html')

def Index(request):
    doctorview = DoctorReg.objects.all()
    page = Page.objects.all()

    context = {'doctorview': doctorview,
    'page':page,
    }
    return render(request, 'index.html',context)




def create_appointment(request):
    doctorview = DoctorReg.objects.all()
    page = Page.objects.all()

    if request.method == "POST":
        appointmentnumber = random.randint(100000000, 999999999)
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        mobilenumber = request.POST.get('mobilenumber')
        date_of_appointment = request.POST.get('date_of_appointment')
        time_of_appointment = request.POST.get('time_of_appointment')
        doctor_id = request.POST.get('doctor_id')
        additional_msg = request.POST.get('additional_msg')
        
        if not fullname.replace(' ', '').isalpha():
            messages.error(request, "Name should contain only letters.")
            return redirect('appointment')

        # Validate mobilenumber
        if not mobilenumber.isdigit() or len(mobilenumber) != 10:
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect('appointment')

        
        doc_instance = DoctorReg.objects.get(id=doctor_id)

        try:
            appointment_date = datetime.strptime(date_of_appointment, '%Y-%m-%d').date()
            today_date = datetime.now().date()

            if appointment_date <= today_date:
            
                messages.error(request, "Please select a date in the future for your appointment")
                return redirect('appointment')  
        except ValueError:
            
            messages.error(request, "Invalid date format")
            return redirect('appointment')  

        
        appointmentdetails = Appointment.objects.create(
            appointmentnumber=appointmentnumber,
            fullname=fullname,
            email=email,
            mobilenumber=mobilenumber,
            date_of_appointment=date_of_appointment,
            time_of_appointment=time_of_appointment,
            doctor_id=doc_instance,
            additional_msg=additional_msg
        )
        
        # Send email notification
        subject = 'Appointment Confirmation'
        message = (
            f'Dear {fullname},\n\n'
            f'Your appointment has been successfully booked.\n\n'
            f'Appointment Details:\n'
            f'Appointment Number: {appointmentnumber}\n'
            f'Date: {date_of_appointment}\n'
            f'Time: {time_of_appointment}\n'
            f'Doctor: {doc_instance}\n\n'
            f'Thank you for choosing Mediguide.'
        )
        from_email = 'nickatutu@gmail.com'
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

      
        messages.success(request, "Your Appointment Request Has Been Sent. We Will Contact You Soon")

        return redirect('appointment')

    context = {'doctorview': doctorview,
    'page':page}
    return render(request, 'appointment.html', context)


def User_Search_Appointments(request):
    page = Page.objects.all()
    
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            
            patient = Appointment.objects.filter(fullname__icontains=query) | Appointment.objects.filter(appointmentnumber__icontains=query)
            messages.info(request, "Search against " + query)
            context = {'patient': patient, 'query': query, 'page': page}
            return render(request, 'search-appointment.html', context)
        else:
            print("No Record Found")
            context = {'page': page}
            return render(request, 'search-appointment.html', context)
    
    context = {'page': page}
    return render(request, 'search-appointment.html', context)

def View_Appointment_Details(request,id):
    page = Page.objects.all()
    patientdetails=Appointment.objects.filter(id=id)
    context={'patientdetails':patientdetails,
    'page': page

    }

    return render(request,'user_appointment-details.html',context)




