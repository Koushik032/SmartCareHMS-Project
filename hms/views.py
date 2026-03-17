from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import DoctorPatientBookmark, Patient, Doctor, Appointment, ContactMessage, Receptionist, Prescription
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count
from django.http import HttpResponse
from django.template.loader import get_template
from datetime import timedelta
from django.db.models import Sum
from decimal import Decimal
from decimal import ROUND_HALF_UP

from .forms import (
    PatientRegisterForm,
    LoginForm,
    ContactForm,
    AddDoctorForm,
    AppointmentForm,
    ReceptionistRegisterForm,
    DoctorRegisterForm,
    PrescriptionForm,
    WalkInPatientAppointmentForm,
    AdminAddReceptionistForm,
    AdminAddPatientForm,
    AdminProfileForm, 
    AdminPasswordForm,
    DoctorProfileForm, 
    DoctorPasswordForm,
    ReceptionistProfileForm,
    ReceptionistPasswordForm,PatientProfileForm, PatientPasswordForm,
)


# -------------------------
# Public Pages
# -------------------------

def home(request):
    return render(request, 'hms/home_cards.html')


def about(request):
    return render(request, 'hms/about.html')


def contact_page(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully.")
            return redirect('contact')

    return render(request, 'hms/contact.html', {'form': form})


# -------------------------
# Authentication
# -------------------------

def admin_login(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid admin credentials.")

    return render(request, 'hms/login_role.html', {
        'form': form,
        'role': 'Admin',
        'register_url': None
    })


def doctor_login(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None and hasattr(user, 'doctor'):
                if user.doctor.is_approved:
                    login(request, user)
                    return redirect('doctor_dashboard')
                else:
                    messages.warning(request, "Your doctor account is waiting for admin approval.")
            else:
                messages.error(request, "Invalid doctor credentials.")

    return render(request, 'hms/login_role.html', {
        'form': form,
        'role': 'Doctor',
        'register_url': 'doctor_register'
    })

def patient_login(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None and hasattr(user, 'patient'):
                login(request, user)
                return redirect('patient_dashboard')
            else:
                messages.error(request, "Invalid patient credentials.")

    return render(request, 'hms/login_role.html', {
        'form': form,
        'role': 'Patient',
        'register_url': 'patient_register'
    })


def receptionist_login(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None and hasattr(user, 'receptionist'):
                login(request, user)
                return redirect('receptionist_dashboard')
            else:
                messages.error(request, "Invalid receptionist credentials.")

    return render(request, 'hms/login_role.html', {
        'form': form,
        'role': 'Receptionist',
        'register_url': 'receptionist_register'
    })

# -------------------------
# Registration
# -------------------------

def patient_register(request):
    form = PatientRegisterForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            Patient.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                contact=form.cleaned_data['contact'],
                gender=form.cleaned_data['gender'],
                photo=form.cleaned_data.get('photo')
            )

            messages.success(request, "Patient account created successfully.")
            return redirect('patient_login')

    return render(request, 'hms/register_role.html', {
        'form': form,
        'role': 'Patient'
    })


def doctor_register(request):
    form = DoctorRegisterForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            Doctor.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                contact=form.cleaned_data['contact'],
                specialist=form.cleaned_data['specialist'],
                hospital_name=form.cleaned_data['hospital_name'],
                location=form.cleaned_data['location'],
                about=form.cleaned_data['about'],
                consultancy_fee=form.cleaned_data['consultancy_fee'],
                photo=form.cleaned_data.get('photo'),
                is_approved=False
            )

            messages.success(
                request,
                "Doctor registration request submitted successfully. Please wait for admin approval."
            )
            return redirect('doctor_login')

    return render(request, 'hms/register_role.html', {
        'form': form,
        'role': 'Doctor'
    })


def receptionist_register(request):
    form = ReceptionistRegisterForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            Receptionist.objects.create(
                user=user,
                organization_name=form.cleaned_data['organization_name'],
                contact=form.cleaned_data['contact'],
                profile_picture=form.cleaned_data.get('profile_picture')
            )

            messages.success(request, "Receptionist account created successfully.")
            return redirect('receptionist_login')

    return render(request, 'hms/register_role.html', {
        'form': form,
        'role': 'Receptionist'
    })

# -------------------------
# Admin Module
# -------------------------

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')

    doctor_count = Doctor.objects.filter(is_approved=True).count()
    patient_count = Patient.objects.count()
    appointment_count = Appointment.objects.count()
    message_count = ContactMessage.objects.count()
    receptionist_count = Receptionist.objects.count()

    raw_hospitals = Receptionist.objects.values_list('organization_name', flat=True).order_by('organization_name')
    hospital_count = len(set(raw_hospitals))

    completed_appointments = Appointment.objects.filter(status='Completed').count()
    pending_appointments = Appointment.objects.filter(
        status__in=['Booked', 'Arrived', 'Waiting', 'In Consultation']
    ).count()

    if appointment_count > 0:
        completion_rate = round((completed_appointments / appointment_count) * 100)
    else:
        completion_rate = 0

    total_users = doctor_count + patient_count + receptionist_count
    if total_users > 0:
        doctor_usage_percent = round((doctor_count / total_users) * 100)
        patient_usage_percent = round((patient_count / total_users) * 100)
        receptionist_usage_percent = round((receptionist_count / total_users) * 100)
    else:
        doctor_usage_percent = 0
        patient_usage_percent = 0
        receptionist_usage_percent = 0

    top_hospitals = (
        Receptionist.objects.values('organization_name')
        .annotate(total=Count('id'))
        .order_by('-total', 'organization_name')[:5]
    )

    return render(request, 'hms/admin/dashboard.html', {
        'doctor_count': doctor_count,
        'patient_count': patient_count,
        'appointment_count': appointment_count,
        'message_count': message_count,
        'receptionist_count': receptionist_count,
        'hospital_count': hospital_count,
        'completed_appointments': completed_appointments,
        'pending_appointments': pending_appointments,
        'completion_rate': completion_rate,
        'doctor_usage_percent': doctor_usage_percent,
        'patient_usage_percent': patient_usage_percent,
        'receptionist_usage_percent': receptionist_usage_percent,
        'top_hospitals': top_hospitals,
    })

@login_required
def admin_profile(request):
    if not request.user.is_staff:
        return redirect('home')

    edit_mode = request.GET.get('edit') == '1'
    password_mode = request.GET.get('password') == '1'

    if request.method == 'POST':
        if 'save_profile' in request.POST:
            profile_form = AdminProfileForm(request.POST, user_instance=request.user)
            password_form = AdminPasswordForm(user_instance=request.user)

            if profile_form.is_valid():
                request.user.username = profile_form.cleaned_data['username']
                request.user.email = profile_form.cleaned_data['email']
                request.user.first_name = profile_form.cleaned_data['first_name']
                request.user.last_name = profile_form.cleaned_data['last_name']
                request.user.save()

                messages.success(request, "Admin profile updated successfully.")
                return redirect('admin_profile')

        elif 'change_password' in request.POST:
            profile_form = AdminProfileForm(
                initial={
                    'username': request.user.username,
                    'email': request.user.email,
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                },
                user_instance=request.user
            )
            password_form = AdminPasswordForm(request.POST, user_instance=request.user)

            if password_form.is_valid():
                request.user.set_password(password_form.cleaned_data['new_password'])
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Password changed successfully.")
                return redirect('admin_profile')
    else:
        profile_form = AdminProfileForm(
            initial={
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            },
            user_instance=request.user
        )
        password_form = AdminPasswordForm(user_instance=request.user)

    return render(request, 'hms/admin/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'edit_mode': edit_mode,
        'password_mode': password_mode,
    })
@login_required
def admin_add_receptionist(request):
    if not request.user.is_staff:
        return redirect('home')

    form = AdminAddReceptionistForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            Receptionist.objects.create(
                user=user,
                organization_name=form.cleaned_data['organization_name'],
                contact=form.cleaned_data['contact'],
                branch_address=form.cleaned_data['branch_address']
            )

            messages.success(request, "Receptionist account created successfully.")
            return redirect('admin_dashboard')

    return render(request, 'hms/admin/add_receptionist.html', {
        'form': form,
    })


@login_required
def admin_add_patient(request):
    if not request.user.is_staff:
        return redirect('home')

    form = AdminAddPatientForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            Patient.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                contact=form.cleaned_data['contact'],
                gender=form.cleaned_data['gender']
            )

            messages.success(request, "Patient account created successfully.")
            return redirect('admin_dashboard')

    return render(request, 'hms/admin/add_patient.html', {
        'form': form,
    })

@login_required
def admin_add_doctor(request):
    if not request.user.is_staff:
        return redirect('home')

    success_doctor = None
    form = AddDoctorForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            doctor = form.save(commit=False)
            doctor.user = user
            doctor.is_approved = True
            doctor.save()

            success_doctor = doctor
            form = AddDoctorForm()
            messages.success(request, "Doctor added successfully and approved automatically.")

    return render(request, 'hms/admin/add_doctor.html', {
        'form': form,
        'success_doctor': success_doctor,
    })

@login_required
def admin_patient_list(request):
    if not request.user.is_staff:
        return redirect('home')

    query = request.GET.get('q', '')
    patients = Patient.objects.select_related('user').all()

    if query:
        patients = patients.filter(contact__icontains=query)

    return render(request, 'hms/admin/patient_list.html', {
        'patients': patients,
        'query': query
    })


@login_required
def admin_doctor_list(request):
    if not request.user.is_staff:
        return redirect('home')

    query = request.GET.get('q', '')
    doctors = Doctor.objects.select_related('user').filter(is_approved=True)

    if query:
        doctors = doctors.filter(user__email__icontains=query)

    return render(request, 'hms/admin/doctor_list.html', {
        'doctors': doctors,
        'query': query
    })


@login_required
def admin_appointment_list(request):
    if not request.user.is_staff:
        return redirect('home')

    query = request.GET.get('q', '')
    appointments = Appointment.objects.select_related('patient', 'doctor', 'patient__user', 'doctor__user').all()

    if query:
        appointments = appointments.filter(patient__contact__icontains=query)

    appointments = appointments.order_by('-appointment_date', '-appointment_time')

    return render(request, 'hms/admin/appointment_list.html', {
        'appointments': appointments,
        'query': query
    })


@login_required
def admin_delete_doctor(request, pk):
    if not request.user.is_staff:
        return redirect('home')

    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.user.delete()

    messages.success(request, "Doctor deleted successfully.")
    return redirect('admin_doctor_list')


@login_required
def admin_messages(request):
    if not request.user.is_staff:
        return redirect('home')

    query = request.GET.get('q', '')
    messages_list = ContactMessage.objects.all().order_by('-created_at')

    if query:
        messages_list = messages_list.filter(contact__icontains=query)

    return render(request, 'hms/admin/messages.html', {
        'messages_list': messages_list,
        'query': query
    })

@login_required
def admin_doctor_requests(request):
    if not request.user.is_staff:
        return redirect('home')

    pending_doctors = Doctor.objects.filter(is_approved=False).select_related('user')
    return render(request, 'hms/admin/doctor_requests.html', {
        'pending_doctors': pending_doctors
    })

@login_required
def admin_approve_doctor(request, pk):
    if not request.user.is_staff:
        return redirect('home')

    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.is_approved = True
    doctor.save()

    messages.success(request, f"Doctor '{doctor.name}' approved successfully.")
    return redirect('admin_doctor_requests')

# -------------------------
# Patient Module
# -------------------------


@login_required
def patient_dashboard(request):
    if not hasattr(request.user, 'patient'):
        return redirect('home')

    patient = request.user.patient

    appointments = Appointment.objects.filter(
        patient=patient
    ).select_related('doctor').order_by('-appointment_date', '-appointment_time')

    total_appointments = appointments.count()
    pending_appointments = appointments.filter(status='Booked').count()
    completed_appointments = appointments.filter(status='Completed').count()

    completed_percentage = 0
    if total_appointments > 0:
        completed_percentage = int((completed_appointments / total_appointments) * 100)

    # Membership logic
    if completed_appointments >= 10:
        level_name = 'Gold'
        discount_percent = 15
    elif completed_appointments >= 6:
        level_name = 'Silver'
        discount_percent = 10
    elif completed_appointments >= 3:
        level_name = 'Bronze'
        discount_percent = 5
    else:
        level_name = 'Starter'
        discount_percent = 0

    # Approved doctors
    doctors = Doctor.objects.filter(is_approved=True).order_by('-id')

    # Unique organizations from receptionist model
    receptionists = Receptionist.objects.select_related('user').order_by('organization_name', '-id')

    unique_organizations = []
    seen_orgs = set()

    for rec in receptionists:
        org_name = rec.organization_name.strip() if rec.organization_name else ''
        if not org_name or org_name in seen_orgs:
            continue

        # same organization-er moddhe jader profile picture ache tader first prefer korbe
        preferred_with_picture = Receptionist.objects.filter(
            organization_name=org_name,
            profile_picture__isnull=False
        ).exclude(profile_picture='').first()

        preferred = preferred_with_picture if preferred_with_picture else rec

        # template-e easy use-er jonno custom attribute
        preferred.organization_photo = preferred.profile_picture

        unique_organizations.append(preferred)
        seen_orgs.add(org_name)

    context = {
        'patient': patient,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'completed_appointments': completed_appointments,
        'completed_percentage': completed_percentage,
        'level_name': level_name,
        'discount_percent': discount_percent,
        'recent_appointments': appointments[:10],
        'doctors': doctors,
        'organizations': unique_organizations,
    }
    return render(request, 'hms/patient/dashboard.html', context)




def get_patient_level_and_discount(completed_count):
    if completed_count >= 10:
        return "Gold", 15
    elif completed_count >= 6:
        return "Silver", 10
    elif completed_count >= 3:
        return "Bronze", 5
    return "Starter", 0



@login_required
def patient_profile(request):
    if not hasattr(request.user, 'patient'):
        return redirect('home')

    patient = request.user.patient
    edit_mode = request.GET.get('edit') == '1'
    password_mode = request.GET.get('password') == '1'

    total_appointments = Appointment.objects.filter(patient=patient).count()
    completed_appointments = Appointment.objects.filter(patient=patient, status='Completed').count()
    pending_appointments = Appointment.objects.filter(
        patient=patient,
        status__in=['Booked', 'Arrived', 'Waiting', 'In Consultation']
    ).count()

    if request.method == 'POST':
        if 'save_profile' in request.POST:
            profile_form = PatientProfileForm(
                request.POST,
                user_instance=request.user
            )
            password_form = PatientPasswordForm(user_instance=request.user)

            if profile_form.is_valid():
                request.user.username = profile_form.cleaned_data['username']
                request.user.email = profile_form.cleaned_data['email']
                request.user.save()

                patient.first_name = profile_form.cleaned_data['first_name']
                patient.last_name = profile_form.cleaned_data['last_name']
                patient.contact = profile_form.cleaned_data['contact']
                patient.gender = profile_form.cleaned_data['gender']
                patient.save()

                messages.success(request, "Profile updated successfully.")
                return redirect('patient_profile')

        elif 'change_password' in request.POST:
            profile_form = PatientProfileForm(
                initial={
                    'first_name': patient.first_name,
                    'last_name': patient.last_name,
                    'contact': patient.contact,
                    'gender': patient.gender,
                    'username': request.user.username,
                    'email': request.user.email,
                },
                user_instance=request.user
            )
            password_form = PatientPasswordForm(
                request.POST,
                user_instance=request.user
            )

            if password_form.is_valid():
                request.user.set_password(password_form.cleaned_data['new_password'])
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Password changed successfully.")
                return redirect('patient_profile')

    else:
        profile_form = PatientProfileForm(
            initial={
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'contact': patient.contact,
                'gender': patient.gender,
                'username': request.user.username,
                'email': request.user.email,
            },
            user_instance=request.user
        )
        password_form = PatientPasswordForm(user_instance=request.user)

    return render(request, 'hms/patient/profile.html', {
        'patient': patient,
        'profile_form': profile_form,
        'password_form': password_form,
        'edit_mode': edit_mode,
        'password_mode': password_mode,
        'total_appointments': total_appointments,
        'completed_appointments': completed_appointments,
        'pending_appointments': pending_appointments,
    })


@login_required
def patient_prescriptions(request):
    if not hasattr(request.user, 'patient' ):
        return redirect('home')

    patient = request.user.patient
    prescriptions = Prescription.objects.filter(patient=patient).select_related(
        'doctor', 'appointment'
    ).order_by('-created_at')

    return render(request, 'hms/patient/prescriptions.html', {
        'prescriptions': prescriptions,
        'patient': patient,
    })


@login_required
def patient_hospitals(request):
    if not hasattr(request.user, 'patient'):
        return redirect('home')

    receptionists = Receptionist.objects.select_related('user').order_by('organization_name', '-id')

    unique_organizations = []
    seen_orgs = set()

    for rec in receptionists:
        org_name = rec.organization_name.strip() if rec.organization_name else ''
        if not org_name or org_name in seen_orgs:
            continue

        # Same organization-er moddhe jader profile picture ache tader first prefer korbe
        preferred_with_picture = Receptionist.objects.filter(
            organization_name=org_name,
            profile_picture__isnull=False
        ).exclude(profile_picture='').first()

        preferred = preferred_with_picture if preferred_with_picture else rec

        # Template-e easy use-er jonno custom attribute
        preferred.organization_photo = preferred.profile_picture

        unique_organizations.append(preferred)
        seen_orgs.add(org_name)

    context = {
        'organizations': unique_organizations
    }

    return render(request, 'hms/patient/hospitals.html', context)


@login_required
def patient_hospital_doctors(request, organization_name):
    if not hasattr(request.user, 'patient'):
        return redirect('home')

    doctors = Doctor.objects.filter(
        hospital_name__iexact=organization_name,
        is_approved=True
    ).order_by('name')

    return render(request, 'hms/patient/hospital_doctors.html', {
        'organization_name': organization_name,
        'doctors': doctors,
    })

@login_required
def patient_doctors(request):
    if not hasattr(request.user, 'patient'):
        return redirect('home')

    doctors = Doctor.objects.filter(is_approved=True)

    return render(request, 'hms/patient/doctors.html', {
        'doctors': doctors
    })

@login_required
def patient_prescription_detail(request, pk):
    if not hasattr(request.user, 'patient'):
        return redirect('home')

    prescription = get_object_or_404(
        Prescription,
        id=pk,
        patient=request.user.patient
    )

    return render(request, 'hms/patient/prescription_detail.html', {
        'prescription': prescription
    })


@login_required
def book_appointment(request):
    if not hasattr(request.user, 'patient'):
        return redirect('home')

    patient = request.user.patient
    selected_doctor_id = request.GET.get('doctor')
    bkash_number = "017XXXXXXXX"

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
    else:
        initial_data = {}
        if selected_doctor_id:
            initial_data['doctor'] = selected_doctor_id
        form = AppointmentForm(initial=initial_data)

    doctors = Doctor.objects.filter(is_approved=True)

    completed_appointments = Appointment.objects.filter(
        patient=patient,
        status='Completed'
    ).count()

    level_name, discount_percent = get_patient_level_and_discount(completed_appointments)

    doctor_data = [
        {
            'id': doctor.id,
            'name': doctor.name or '',
            'hospital_name': doctor.hospital_name or '',
            'location': doctor.location or '',
            'fee': float(doctor.consultancy_fee or 0),
            'discount_percent': discount_percent,
            'discount_amount': round((float(doctor.consultancy_fee or 0) * discount_percent) / 100, 2),
            'final_fee': round(
                float(doctor.consultancy_fee or 0) -
                ((float(doctor.consultancy_fee or 0) * discount_percent) / 100),
                2
            ),
        }
        for doctor in doctors
    ]

    if request.method == 'POST':
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient

            original_fee = appointment.doctor.consultancy_fee or 0
            discount_amount = (original_fee * discount_percent) / 100
            final_fee = original_fee - discount_amount

            appointment.consultancy_fee = round(final_fee, 2)

            # Payment logic
            if appointment.payment_method == 'Bkash':
                appointment.payment_number = bkash_number
                appointment.payment_status = 'Paid'
            elif appointment.payment_method == 'Cash':
                appointment.payment_number = ''
                appointment.transaction_id = ''
                appointment.payment_status = 'Unpaid'
            else:
                appointment.payment_number = ''
                appointment.transaction_id = ''
                appointment.payment_status = 'Pending'

            appointment.save()

            messages.success(
                request,
                f"Your appointment was successfully booked. Level: {level_name}, Discount: {discount_percent}%."
            )
            return redirect('patient_history')

    return render(request, 'hms/patient/book_appointment.html', {
        'form': form,
        'doctor_data': doctor_data,
        'level_name': level_name,
        'discount_percent': discount_percent,
        'bkash_number': bkash_number,
    })




@login_required
def patient_history(request):
    if not hasattr(request.user, 'patient'):
        return redirect('home')

    patient = request.user.patient
    now = timezone.localtime()

    appointments = (
        Appointment.objects.filter(patient=patient)
        .select_related('doctor')
        .order_by('-appointment_date', '-appointment_time')
    )

    total_appointments = appointments.count()
    completed_count = appointments.filter(status='Completed').count()
    booked_count = appointments.filter(status='Booked').count()
    cancelled_count = appointments.filter(status='Cancelled').count()

    for a in appointments:
        # prescription check
        a.has_prescription = Prescription.objects.filter(appointment=a).exists()

        # appointment datetime বানানো
        try:
            naive_dt = datetime.combine(a.appointment_date, a.appointment_time)
            appointment_dt = timezone.make_aware(
                naive_dt,
                timezone.get_current_timezone()
            )
        except Exception:
            appointment_dt = None

        # display status logic
        if a.status == 'Completed':
            a.display_status = 'Completed'
        elif a.status == 'Cancelled':
            a.display_status = 'Cancelled'
        elif a.status == 'Booked':
            if appointment_dt and appointment_dt < now and not a.has_prescription:
                a.display_status = 'Missed'
            else:
                a.display_status = 'Booked'
        else:
            a.display_status = a.status

        # cancel only if future booked
        a.can_cancel = (
            a.status == 'Booked'
            and appointment_dt is not None
            and appointment_dt > now
        )

    context = {
        'appointments': appointments,
        'total_appointments': total_appointments,
        'completed_count': completed_count,
        'booked_count': booked_count,
        'cancelled_count': cancelled_count,
    }
    return render(request, 'hms/patient/history.html', context)



@login_required
def patient_cancel_appointment(request, appointment_id):
    if not hasattr(request.user, 'patient'):
        return redirect('home')

    patient = request.user.patient
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=patient
    )

    now = timezone.localtime()
    naive_dt = datetime.combine(appointment.appointment_date, appointment.appointment_time)
    appointment_dt = timezone.make_aware(
        naive_dt,
        timezone.get_current_timezone()
    )

    if appointment.status == 'Booked' and appointment_dt > now:
        appointment.status = 'Cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully.')
    else:
        messages.error(request, 'This appointment can no longer be cancelled.')

    return redirect('patient_history')


@login_required
def patient_view_prescription(request, appointment_id):
    if not hasattr(request.user, 'patient'):
        return redirect('home')

    patient = request.user.patient

    appointment = get_object_or_404(
        Appointment.objects.select_related('doctor', 'patient'),
        id=appointment_id,
        patient=patient
    )

    prescription = get_object_or_404(
        Prescription,
        appointment=appointment
    )

    context = {
        'appointment': appointment,
        'prescription': prescription,
    }
    return render(request, 'hms/patient/view_prescription.html', context)



# -------------------------
# Doctor Module
# -------------------------

@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, 'doctor'):
        return redirect('home')

    doctor = request.user.doctor
    query = request.GET.get('q', '').strip()

    today = timezone.localdate()
    now = timezone.localtime()
    current_month = today.month
    current_year = today.year

    # Search-aware recent appointments block
    appointments = Appointment.objects.filter(
        doctor=doctor
    ).select_related('patient', 'patient__user').order_by('-appointment_date', '-appointment_time')

    if query:
        appointments = appointments.filter(
            Q(patient__first_name__icontains=query) |
            Q(patient__last_name__icontains=query) |
            Q(patient__contact__icontains=query)
        )

    # All doctor appointments for full analytics
    all_appointments = Appointment.objects.filter(doctor=doctor)

    total_count = all_appointments.count()

    today_count = all_appointments.filter(appointment_date=today).count()
    booked_count = all_appointments.filter(status='Booked').count()
    cancelled_count = all_appointments.filter(status='Cancelled').count()
    completed_count = all_appointments.filter(status='Completed').count()

    upcoming_qs = all_appointments.filter(
        Q(appointment_date__gt=today) |
        Q(appointment_date=today, appointment_time__gte=now.time()),
        status='Booked'
    ).select_related('patient', 'patient__user').order_by('appointment_date', 'appointment_time')

    upcoming_count = upcoming_qs.count()

    # New backend functionality 1:
    next_upcoming_appointment = upcoming_qs.first()

    online_count = all_appointments.filter(appointment_mode='Online').count()
    offline_count = all_appointments.filter(appointment_mode='Offline').count()

    monthly_completed_qs = all_appointments.filter(
        status='Completed',
        appointment_date__month=current_month,
        appointment_date__year=current_year
    )

    monthly_completed_count = monthly_completed_qs.count()

    monthly_earnings_raw = monthly_completed_qs.aggregate(
        total=Sum('consultancy_fee')
    )['total'] or Decimal('0')

    today_earnings_raw = all_appointments.filter(
        status='Completed',
        appointment_date=today
    ).aggregate(
        total=Sum('consultancy_fee')
    )['total'] or Decimal('0')

    # Force 2 decimal places
    monthly_earnings = Decimal(monthly_earnings_raw).quantize(
        Decimal('0.01'),
        rounding=ROUND_HALF_UP
    )
    today_earnings = Decimal(today_earnings_raw).quantize(
        Decimal('0.01'),
        rounding=ROUND_HALF_UP
    )

    unique_patient_count = all_appointments.values('patient').distinct().count()

    # New backend functionality 2:
    repeat_patient_count = (
        all_appointments.values('patient')
        .annotate(total_visits=Count('id'))
        .filter(total_visits__gt=1)
        .count()
    )

    # New backend functionality 3:
    today_pending_count = all_appointments.filter(
        appointment_date=today,
        status='Booked'
    ).count()

    recent_appointments = all_appointments.select_related(
        'patient', 'patient__user'
    ).order_by('-appointment_date', '-appointment_time')[:5]

    recent_patients = (
        all_appointments.select_related('patient', 'patient__user')
        .order_by('-appointment_date', '-appointment_time')
    )

    recent_patient_ids = []
    recent_patient_list = []
    for ap in recent_patients:
        if ap.patient.id not in recent_patient_ids:
            recent_patient_ids.append(ap.patient.id)
            recent_patient_list.append(ap.patient)
        if len(recent_patient_list) == 5:
            break

    bookmarked_patients = Patient.objects.filter(
        doctorpatientbookmark__doctor=doctor
    ).distinct()[:6]

    patient_load_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = all_appointments.filter(appointment_date=day).count()
        patient_load_data.append({
            'label': day.strftime('%a'),
            'count': count,
            'height': max(count * 18, 24) if count > 0 else 18,
        })

    max_load = max([item['count'] for item in patient_load_data], default=1)

    appointment_completion_rate = 0
    if total_count > 0:
        appointment_completion_rate = int((completed_count / total_count) * 100)

    online_ratio = 0
    if total_count > 0:
        online_ratio = int((online_count / total_count) * 100)

    return render(request, 'hms/doctor/dashboard.html', {
        'doctor': doctor,
        'appointments': appointments[:3],
        'query': query,

        'today_count': today_count,
        'booked_count': booked_count,
        'cancelled_count': cancelled_count,
        'completed_count': completed_count,
        'upcoming_count': upcoming_count,
        'online_count': online_count,
        'offline_count': offline_count,

        'monthly_completed_count': monthly_completed_count,
        'monthly_earnings': monthly_earnings,
        'today_earnings': today_earnings,
        'unique_patient_count': unique_patient_count,

        'recent_appointments': recent_appointments,
        'recent_patients': recent_patient_list,
        'bookmarked_patients': bookmarked_patients,

        'patient_load_data': patient_load_data,
        'max_load': max_load,
        'appointment_completion_rate': appointment_completion_rate,
        'online_ratio': online_ratio,

        # New useful doctor dashboard data
        'next_upcoming_appointment': next_upcoming_appointment,
        'repeat_patient_count': repeat_patient_count,
        'today_pending_count': today_pending_count,
        'total_count': total_count,
    })

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Appointment, Prescription
from .forms import PrescriptionForm


@login_required
def doctor_add_prescription(request, appointment_id):
    if not hasattr(request.user, 'doctor'):
        return redirect('home')

    doctor = request.user.doctor

    appointment = get_object_or_404(
        Appointment.objects.select_related('patient', 'doctor'),
        id=appointment_id,
        doctor=doctor
    )

    existing_prescription = Prescription.objects.filter(appointment=appointment).first()
    if existing_prescription:
        messages.info(request, "Prescription already added for this appointment.")
        return redirect('doctor_pending_appointments')

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.doctor = doctor
            prescription.patient = appointment.patient
            prescription.symptoms_snapshot = appointment.symptoms
            prescription.save()

            appointment.status = 'Completed'
            appointment.save(update_fields=['status'])

            messages.success(request, "Prescription added successfully and appointment marked as completed.")
            return redirect('doctor_pending_appointments')
    else:
        form = PrescriptionForm()

    return render(request, 'hms/doctor/add_prescription.html', {
        'form': form,
        'appointment': appointment,
    })

@login_required
def doctor_toggle_bookmark_patient(request, patient_id):
    if not hasattr(request.user, 'doctor'):
        return redirect('home')

    doctor = request.user.doctor
    patient = get_object_or_404(Patient, id=patient_id)

    bookmark = DoctorPatientBookmark.objects.filter(
        doctor=doctor,
        patient=patient
    ).first()

    if bookmark:
        bookmark.delete()
        messages.success(request, "Patient removed from bookmarked list.")
    else:
        DoctorPatientBookmark.objects.create(
            doctor=doctor,
            patient=patient
        )
        messages.success(request, "Patient added to bookmarked list.")

    return redirect('doctor_dashboard')

@login_required
def doctor_profile(request):
    if not hasattr(request.user, 'doctor'):
        return redirect('home')

    doctor = request.user.doctor
    edit_mode = request.GET.get('edit') == '1'
    password_mode = request.GET.get('password') == '1'

    doctor_appointments = Appointment.objects.filter(doctor=doctor)
    total_appointments = doctor_appointments.count()
    online_appointments = doctor_appointments.filter(appointment_mode='Online').count()
    completed_appointments = doctor_appointments.filter(status='Completed').count()

    if request.method == 'POST':
        if 'save_profile' in request.POST:
            profile_form = DoctorProfileForm(
                request.POST,
                request.FILES,
                user_instance=request.user
            )
            password_form = DoctorPasswordForm(user_instance=request.user)

            if profile_form.is_valid():
                request.user.username = profile_form.cleaned_data['username']
                request.user.email = profile_form.cleaned_data['email']
                request.user.save()

                doctor.name = profile_form.cleaned_data['name']
                doctor.specialist = profile_form.cleaned_data['specialist']
                doctor.hospital_name = profile_form.cleaned_data['hospital_name']
                doctor.location = profile_form.cleaned_data['location']
                doctor.contact = profile_form.cleaned_data['contact']
                doctor.consultancy_fee = profile_form.cleaned_data['consultancy_fee']
                doctor.about = profile_form.cleaned_data['about']
                if profile_form.cleaned_data.get('photo'):
                    doctor.photo = profile_form.cleaned_data['photo']
                doctor.save()

                messages.success(request, "Doctor profile updated successfully.")
                return redirect('doctor_profile')

        elif 'change_password' in request.POST:
            profile_form = DoctorProfileForm(
                initial={
                    'name': doctor.name,
                    'specialist': doctor.specialist,
                    'hospital_name': doctor.hospital_name,
                    'location': doctor.location,
                    'contact': doctor.contact,
                    'consultancy_fee': doctor.consultancy_fee,
                    'about': doctor.about,
                    'username': request.user.username,
                    'email': request.user.email,
                    'photo': doctor.photo,
                },
                user_instance=request.user
            )
            password_form = DoctorPasswordForm(request.POST, user_instance=request.user)

            if password_form.is_valid():
                request.user.set_password(password_form.cleaned_data['new_password'])
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Password changed successfully.")
                return redirect('doctor_profile')

    else:
        profile_form = DoctorProfileForm(
            initial={
                'name': doctor.name,
                'specialist': doctor.specialist,
                'hospital_name': doctor.hospital_name,
                'location': doctor.location,
                'contact': doctor.contact,
                'consultancy_fee': doctor.consultancy_fee,
                'about': doctor.about,
                'username': request.user.username,
                'email': request.user.email,
                'photo': doctor.photo,
            },
            user_instance=request.user
        )
        password_form = DoctorPasswordForm(user_instance=request.user)

    return render(request, 'hms/doctor/profile.html', {
        'doctor': doctor,
        'profile_form': profile_form,
        'password_form': password_form,
        'edit_mode': edit_mode,
        'password_mode': password_mode,
        'total_appointments': total_appointments,
        'online_appointments': online_appointments,
        'completed_appointments': completed_appointments,
    })


id="doctor-appointments-updated"
@login_required
def doctor_appointments(request):
    if not hasattr(request.user, 'doctor'):
        return redirect('home')

    doctor = request.user.doctor
    query = request.GET.get('q', '').strip()
    from_date = request.GET.get('from_date', '').strip()
    to_date = request.GET.get('to_date', '').strip()

    appointments = Appointment.objects.filter(
        doctor=doctor,
        status__in=['Completed', 'Missed', 'Cancelled by Patient', 'Cancelled by Doctor']
    ).select_related('patient', 'patient__user').order_by('-appointment_date', '-appointment_time')

    if query:
        appointments = appointments.filter(patient__contact__icontains=query)

    if from_date:
        appointments = appointments.filter(appointment_date__gte=from_date)

    if to_date:
        appointments = appointments.filter(appointment_date__lte=to_date)

    for a in appointments:
        a.display_status = a.status
        a.has_prescription = Prescription.objects.filter(appointment=a).exists()

    context = {
        'doctor': doctor,
        'appointments': appointments,
        'query': query,
        'from_date': from_date,
        'to_date': to_date,
        'total_visible': appointments.count(),
    }
    return render(request, 'hms/doctor/appointments.html', context)


@login_required
def doctor_pending_appointments(request):
    if not hasattr(request.user, 'doctor'):
        return redirect('home')

    doctor = request.user.doctor
    today = timezone.localdate()

    appointments = Appointment.objects.filter(
        doctor=doctor,
        status='Booked'
    ).select_related('patient', 'patient__user').order_by(
        'appointment_date',
        'appointment_time'
    )

    for a in appointments:
        a.display_status = a.status
        a.has_prescription = Prescription.objects.filter(appointment=a).exists()

    context = {
        'doctor': doctor,
        'appointments': appointments,
        'today': today,
        'total_visible': appointments.count(),
    }
    return render(request, 'hms/doctor/pending_appointments.html', context)


@login_required
def doctor_patients(request):
    if not hasattr(request.user, 'doctor'):
        return redirect('home')

    doctor = request.user.doctor
    query = request.GET.get('q', '').strip()

    completed_appointments = Appointment.objects.filter(
        doctor=doctor,
        status='Completed'
    ).select_related('patient', 'patient__user').order_by('-appointment_date', '-appointment_time')

    if query:
        completed_appointments = completed_appointments.filter(
            Q(patient__first_name__icontains=query) |
            Q(patient__last_name__icontains=query) |
            Q(patient__contact__icontains=query)
        )

    patient_ids = []
    patients = []

    for ap in completed_appointments:
        if ap.patient_id not in patient_ids:
            patient_ids.append(ap.patient_id)
            patients.append(ap.patient)

    context = {
        'doctor': doctor,
        'patients': patients,
        'query': query,
        'total_patients': len(patients),
    }
    return render(request, 'hms/doctor/patients.html', context)


@login_required
def doctor_patient_detail(request, patient_id):
    if not hasattr(request.user, 'doctor'):
        return redirect('home')

    doctor = request.user.doctor

    patient = get_object_or_404(
        Patient.objects.select_related('user'),
        id=patient_id
    )

    has_access = Appointment.objects.filter(
        doctor=doctor,
        patient=patient,
        status='Completed'
    ).exists()

    if not has_access:
        return redirect('doctor_patients')

    completed_appointments = Appointment.objects.filter(
        doctor=doctor,
        patient=patient,
        status='Completed'
    ).order_by('-appointment_date', '-appointment_time')

    prescriptions = Prescription.objects.filter(
        appointment__doctor=doctor,
        appointment__patient=patient
    ).select_related('appointment').order_by('-id')

    context = {
        'doctor': doctor,
        'patient': patient,
        'completed_appointments': completed_appointments,
        'prescriptions': prescriptions,
    }
    return render(request, 'hms/doctor/patient_detail.html', context)

@login_required
def doctor_complete_appointment(request, pk):
    if not hasattr(request.user, 'doctor'):
        return redirect('home')

    appointment = get_object_or_404(
        Appointment,
        pk=pk,
        doctor=request.user.doctor
    )

    if appointment.status == 'Booked':
        appointment.status = 'Completed'
        appointment.save()
        messages.success(request, "Appointment marked as completed.")

    return redirect('doctor_appointments')


@login_required
def doctor_cancel_appointment(request, pk):
    if not hasattr(request.user, 'doctor'):
        return redirect('home')

    appointment = get_object_or_404(
        Appointment,
        pk=pk,
        doctor=request.user.doctor
    )

    if appointment.status == 'Booked':
        appointment.status = 'Cancelled by Doctor'
        appointment.save()
        messages.success(request, "Appointment cancelled successfully.")

    return redirect('doctor_dashboard')

@login_required
def doctor_view_prescription(request, appointment_id):
    if not hasattr(request.user, 'doctor'):
        return redirect('home')

    doctor = request.user.doctor

    prescription = get_object_or_404(
        Prescription.objects.select_related('doctor', 'patient', 'appointment'),
        appointment_id=appointment_id,
        doctor=doctor
    )

    return render(request, 'hms/doctor/view_prescription.html', {
        'prescription': prescription,
        'doctor': doctor,
    })


# -------------------------
# Receptionist Module
# -------------------------

@login_required
def receptionist_dashboard(request):
    if not hasattr(request.user, 'receptionist'):
        return redirect('home')

    receptionist = request.user.receptionist
    org_name = receptionist.organization_name
    query = request.GET.get('q', '')
    filter_date = request.GET.get('date', '')

    doctors = Doctor.objects.filter(hospital_name__iexact=org_name, is_approved=True)

    appointments = Appointment.objects.filter(
        doctor__hospital_name__iexact=org_name
    ).select_related('patient', 'doctor').order_by('appointment_date', 'appointment_time')

    today = timezone.localdate()

    if query:
        appointments = appointments.filter(
            patient__contact__icontains=query
        ) | appointments.filter(
            patient__first_name__icontains=query
        ) | appointments.filter(
            patient__last_name__icontains=query
        )

    if filter_date:
        appointments = appointments.filter(appointment_date=filter_date)

    today_appointments = Appointment.objects.filter(
        doctor__hospital_name__iexact=org_name,
        appointment_date=today
    ).select_related('patient', 'doctor').order_by('appointment_time')

    patient_ids = appointments.values_list('patient_id', flat=True).distinct()
    patients = Patient.objects.filter(id__in=patient_ids)

    waiting_count = today_appointments.filter(status='Waiting').count()
    arrived_count = today_appointments.filter(status='Arrived').count()
    completed_count = today_appointments.filter(status='Completed').count()
    urgent_count = today_appointments.filter(urgency_level='Emergency').count()

    now = timezone.localtime()
    for appointment in today_appointments:
        appointment.display_status = appointment.status
        appointment_datetime = timezone.make_aware(
            datetime.combine(appointment.appointment_date, appointment.appointment_time)
        )
        if appointment.status in ['Booked', 'Arrived', 'Waiting'] and appointment_datetime < now:
            appointment.display_status = 'Missed'

    return render(request, 'hms/receptionist/dashboard.html', {
        'receptionist': receptionist,
        'patients': patients,
        'doctors': doctors,
        'appointments': appointments,
        'today_appointments': today_appointments,
        'query': query,
        'filter_date': filter_date,
        'waiting_count': waiting_count,
        'arrived_count': arrived_count,
        'completed_count': completed_count,
        'urgent_count': urgent_count,
        'today_date': today,
    })

@login_required
def receptionist_walkin_with_appointment(request):
    if not hasattr(request.user, 'receptionist'):
        return redirect('home')

    receptionist = request.user.receptionist
    org_name = receptionist.organization_name

    doctors = Doctor.objects.filter(
        hospital_name__iexact=org_name,
        is_approved=True
    ).order_by('name')

    form = WalkInPatientAppointmentForm(
        request.POST or None,
        doctor_queryset=doctors
    )

    if request.method == 'POST':
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            patient = Patient.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                contact=form.cleaned_data['contact'],
                gender=form.cleaned_data['gender']
            )

            doctor = form.cleaned_data['doctor']

            original_fee = doctor.consultancy_fee or 0
            discount_percent = 0
            discount_amount = (original_fee * discount_percent) / 100
            final_fee = original_fee - discount_amount

            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=form.cleaned_data['appointment_date'],
                appointment_time=form.cleaned_data['appointment_time'],
                consultancy_fee=round(final_fee, 2),
                appointment_mode=form.cleaned_data['appointment_mode'],
                problem_category=form.cleaned_data['problem_category'],
                urgency_level=form.cleaned_data['urgency_level'],
                symptoms=form.cleaned_data['symptoms'],
                meeting_link=form.cleaned_data['meeting_link'],
                visit_note=form.cleaned_data['visit_note'],
                status='Booked'
            )

            messages.success(
                request,
                f"Walk-in patient registered successfully. Patient ID: {patient.id}. Appointment ID: {appointment.id}."
            )
            return redirect('receptionist_dashboard')
        else:
            messages.error(request, "Form submission failed. Please check the errors below.")

    doctor_data = [
        {
            'id': doctor.id,
            'hospital_name': doctor.hospital_name or '',
            'location': doctor.location or '',
            'fee': float(doctor.consultancy_fee or 0),
            'discount_percent': 0,
            'discount_amount': 0,
            'final_fee': float(doctor.consultancy_fee or 0),
        }
        for doctor in doctors
    ]

    return render(request, 'hms/receptionist/walkin_and_appointment.html', {
        'form': form,
        'doctor_data': doctor_data,
        'receptionist': receptionist,
    })
@login_required
def receptionist_profile(request):
    if not hasattr(request.user, 'receptionist'):
        return redirect('home')

    receptionist = request.user.receptionist
    edit_mode = request.GET.get('edit') == '1'
    password_mode = request.GET.get('password') == '1'

    total_doctors = Doctor.objects.filter(
        hospital_name__iexact=receptionist.organization_name,
        is_approved=True
    ).count()

    total_appointments = Appointment.objects.filter(
        doctor__hospital_name__iexact=receptionist.organization_name
    ).count()

    total_patients = Patient.objects.filter(
        id__in=Appointment.objects.filter(
            doctor__hospital_name__iexact=receptionist.organization_name
        ).values_list('patient_id', flat=True).distinct()
    ).count()

    today_appointments = Appointment.objects.filter(
        doctor__hospital_name__iexact=receptionist.organization_name,
        appointment_date=timezone.localdate()
    ).count()

    if request.method == 'POST':
        if 'save_profile' in request.POST:
            profile_form = ReceptionistProfileForm(
                request.POST,
                request.FILES,
                user_instance=request.user,
                receptionist_instance=receptionist
            )
            password_form = ReceptionistPasswordForm(user_instance=request.user)

            if profile_form.is_valid():
                request.user.username = profile_form.cleaned_data['username']
                request.user.email = profile_form.cleaned_data['email']
                request.user.save()

                receptionist.organization_name = profile_form.cleaned_data['organization_name']
                receptionist.contact = profile_form.cleaned_data['contact']
                receptionist.branch_address = profile_form.cleaned_data['branch_address']

                if profile_form.cleaned_data.get('profile_picture'):
                    receptionist.profile_picture = profile_form.cleaned_data['profile_picture']

                receptionist.save()

                messages.success(request, "Profile updated successfully.")
                return redirect('receptionist_profile')

        elif 'change_password' in request.POST:
            profile_form = ReceptionistProfileForm(
                initial={
                    'organization_name': receptionist.organization_name,
                    'contact': receptionist.contact,
                    'branch_address': receptionist.branch_address,
                    'username': request.user.username,
                    'email': request.user.email,
                    'profile_picture': receptionist.profile_picture,
                },
                user_instance=request.user,
                receptionist_instance=receptionist
            )
            password_form = ReceptionistPasswordForm(
                request.POST,
                user_instance=request.user
            )

            if password_form.is_valid():
                request.user.set_password(password_form.cleaned_data['new_password'])
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Password changed successfully.")
                return redirect('receptionist_profile')

    else:
        profile_form = ReceptionistProfileForm(
            initial={
                'organization_name': receptionist.organization_name,
                'contact': receptionist.contact,
                'branch_address': receptionist.branch_address,
                'username': request.user.username,
                'email': request.user.email,
                'profile_picture': receptionist.profile_picture,
            },
            user_instance=request.user,
            receptionist_instance=receptionist
        )
        password_form = ReceptionistPasswordForm(user_instance=request.user)

    return render(request, 'hms/receptionist/profile.html', {
        'receptionist': receptionist,
        'profile_form': profile_form,
        'password_form': password_form,
        'edit_mode': edit_mode,
        'password_mode': password_mode,
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'today_appointments': today_appointments,
    })

@login_required
def receptionist_create_appointment(request):
    if not hasattr(request.user, 'receptionist'):
        return redirect('home')

    receptionist = request.user.receptionist
    org_name = receptionist.organization_name

    form = AppointmentForm(request.POST or None)

    # receptionist only own organization doctors
    doctor_queryset = Doctor.objects.filter(
        hospital_name__iexact=org_name,
        is_approved=True
    )
    form.fields['doctor'].queryset = doctor_queryset

    # all patients for dropdown
    patient_queryset = Patient.objects.all().select_related('user')

    # patient-wise discount data for JS
    patient_data = []
    for patient in patient_queryset:
        completed_appointments = Appointment.objects.filter(
            patient=patient,
            status='Completed'
        ).count()

        level_name, discount_percent = get_patient_level_and_discount(completed_appointments)

        patient_data.append({
            'id': patient.id,
            'name': f"{patient.first_name} {patient.last_name}",
            'discount_percent': discount_percent,
            'level_name': level_name,
        })

    selected_patient = None

    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        selected_patient = get_object_or_404(Patient, id=patient_id)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = selected_patient

            # selected patient discount হিসাব
            completed_appointments = Appointment.objects.filter(
                patient=selected_patient,
                status='Completed'
            ).count()

            level_name, discount_percent = get_patient_level_and_discount(completed_appointments)

            original_fee = appointment.doctor.consultancy_fee or 0
            discount_amount = (original_fee * discount_percent) / 100
            final_fee = original_fee - discount_amount

            appointment.consultancy_fee = round(final_fee, 2)
            appointment.save()

            messages.success(
                request,
                f"Appointment created successfully. Patient level: {level_name}, Discount: {discount_percent}%."
            )
            return redirect('receptionist_dashboard')

    # initial/default selected patient discount
    default_discount_percent = 0
    if selected_patient:
        completed_appointments = Appointment.objects.filter(
            patient=selected_patient,
            status='Completed'
        ).count()
        _, default_discount_percent = get_patient_level_and_discount(completed_appointments)

    # doctor data with default patient discount for first render
    doctor_data = [
        {
            'id': doctor.id,
            'hospital_name': doctor.hospital_name or '',
            'location': doctor.location or '',
            'fee': float(doctor.consultancy_fee or 0),
            'discount_percent': default_discount_percent,
            'discount_amount': round((float(doctor.consultancy_fee or 0) * default_discount_percent) / 100, 2),
            'final_fee': round(
                float(doctor.consultancy_fee or 0) -
                ((float(doctor.consultancy_fee or 0) * default_discount_percent) / 100),
                2
            ),
        }
        for doctor in doctor_queryset
    ]

    return render(request, 'hms/receptionist/create_appointment.html', {
        'form': form,
        'patients': patient_queryset,
        'patient_data': patient_data,
        'doctor_data': doctor_data,
        'receptionist': receptionist,
    })

@login_required
def receptionist_doctors(request):
    if not hasattr(request.user, 'receptionist'):
        return redirect('home')

    receptionist = request.user.receptionist
    query = request.GET.get('q', '')

    doctors = Doctor.objects.filter(
        hospital_name__iexact=receptionist.organization_name,
        is_approved=True
    ).order_by('name')

    if query:
        doctors = doctors.filter(
            Q(name__icontains=query) |
            Q(specialist__icontains=query) |
            Q(contact__icontains=query)
        )

    return render(request, 'hms/receptionist/doctors.html', {
        'receptionist': receptionist,
        'doctors': doctors,
        'query': query,
    })


@login_required
def receptionist_patients(request):
    if not hasattr(request.user, 'receptionist'):
        return redirect('home')

    receptionist = request.user.receptionist
    query = request.GET.get('q', '')

    appointments = Appointment.objects.filter(
        doctor__hospital_name__iexact=receptionist.organization_name
    ).select_related('patient')

    patient_ids = appointments.values_list('patient_id', flat=True).distinct()
    patients = Patient.objects.filter(id__in=patient_ids).select_related('user').order_by('first_name')

    if query:
        patients = patients.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(contact__icontains=query) |
            Q(user__email__icontains=query)
        )

    return render(request, 'hms/receptionist/patients.html', {
        'receptionist': receptionist,
        'patients': patients,
        'query': query,
    })

@login_required
def receptionist_all_appointments(request):
    if not hasattr(request.user, 'receptionist'):
        return redirect('home')

    receptionist = request.user.receptionist

    query = request.GET.get('q', '').strip()
    from_date = request.GET.get('from_date', '').strip()
    to_date = request.GET.get('to_date', '').strip()

    appointments = Appointment.objects.filter(
        doctor__hospital_name__icontains=receptionist.organization_name
    ).select_related(
        'doctor', 'patient', 'patient__user'
    ).order_by('-appointment_date', '-appointment_time')

    if query:
        appointments = appointments.filter(
            Q(doctor__name__icontains=query) |
            Q(patient__first_name__icontains=query) |
            Q(patient__last_name__icontains=query) |
            Q(patient__contact__icontains=query) |
            Q(doctor__hospital_name__icontains=query)
        )

    if from_date:
        appointments = appointments.filter(appointment_date__gte=from_date)

    if to_date:
        appointments = appointments.filter(appointment_date__lte=to_date)

    return render(request, 'hms/receptionist/all_appointments.html', {
        'receptionist': receptionist,
        'appointments': appointments,
        'query': query,
        'from_date': from_date,
        'to_date': to_date,
    })


@login_required
def receptionist_update_appointment_status(request, pk, status):
    if not hasattr(request.user, 'receptionist'):
        return redirect('home')

    receptionist = request.user.receptionist
    allowed_statuses = ['Arrived', 'Waiting', 'In Consultation', 'Completed', 'Missed']

    if status not in allowed_statuses:
        return redirect('receptionist_dashboard')

    appointment = get_object_or_404(
        Appointment,
        pk=pk,
        doctor__hospital_name__iexact=receptionist.organization_name
    )

    appointment.status = status
    appointment.save()

    messages.success(request, f"Appointment status updated to {status}.")
    return redirect('receptionist_dashboard')

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import ReportShow, ReportShowFile, Appointment, Prescription
from .forms import PatientReportShowForm, ReportPrescriptionUpdateForm


@login_required
def patient_report_show(request):
    if not hasattr(request.user, 'patient'):
        return redirect('home')

    patient = request.user.patient
    today = timezone.localdate()

    if request.method == 'POST':
        form = PatientReportShowForm(request.POST, request.FILES, patient=patient)
        report_file = request.FILES.get('report_file')

        if form.is_valid():
            selected_doctor = form.cleaned_data['doctor']

            previous_appointment = Appointment.objects.filter(
                patient=patient,
                doctor=selected_doctor
            ).order_by('-appointment_date', '-appointment_time').first()

            if not previous_appointment:
                messages.error(request, "No previous appointment found with this doctor.")
                return redirect('patient_report_show')

            day_diff = (today - previous_appointment.appointment_date).days

            if day_diff > 7:
                messages.error(request, "Your reporting showing date in expired.")
                return redirect('patient_report_show')

            report_show = form.save(commit=False)
            report_show.patient = patient
            report_show.doctor = selected_doctor
            report_show.previous_appointment = previous_appointment
            report_show.submitted_date = today
            report_show.status = 'Pending'
            report_show.save()

            if report_file:
                ReportShowFile.objects.create(
                    report_show=report_show,
                    file=report_file
                )

            messages.success(request, "Appointment report submitted successfully.")
            return redirect('patient_report_show')
    else:
        form = PatientReportShowForm(patient=patient)

    previous_doctors = Appointment.objects.filter(
        patient=patient
    ).select_related('doctor').order_by('-appointment_date')

    return render(request, 'hms/patient/report_show.html', {
        'form': form,
        'patient': patient,
        'previous_doctors': previous_doctors,
    })


@login_required
def doctor_report_show_list(request):
    if not hasattr(request.user, 'doctor'):
        return redirect('home')

    doctor = request.user.doctor

    reports = ReportShow.objects.filter(
        doctor=doctor,
        status='Pending'
    ).select_related('patient', 'previous_appointment').prefetch_related('files').order_by(
        '-submitted_date',
        '-id'
    )

    return render(request, 'hms/doctor/report_show_list.html', {
        'doctor': doctor,
        'reports': reports,
        'total_visible': reports.count(),
    })


@login_required
def doctor_report_show_detail(request, report_id):
    if not hasattr(request.user, 'doctor'):
        return redirect('home')

    doctor = request.user.doctor

    report = get_object_or_404(
        ReportShow.objects.select_related('patient', 'doctor', 'previous_appointment').prefetch_related('files'),
        id=report_id,
        doctor=doctor
    )

    previous_prescription = Prescription.objects.filter(
        appointment=report.previous_appointment
    ).select_related('doctor', 'patient').first()

    return render(request, 'hms/doctor/report_show_detail.html', {
        'doctor': doctor,
        'report': report,
        'previous_prescription': previous_prescription,
    })


@login_required
def doctor_report_show_update(request, report_id):
    if not hasattr(request.user, 'doctor'):
        return redirect('home')

    doctor = request.user.doctor

    report = get_object_or_404(
        ReportShow.objects.select_related('patient', 'doctor', 'previous_appointment'),
        id=report_id,
        doctor=doctor,
        status='Pending'
    )

    if request.method == 'POST':
        form = ReportPrescriptionUpdateForm(request.POST)
        if form.is_valid():
            prev = report.previous_appointment

            new_appointment = Appointment.objects.create(
                patient=report.patient,
                doctor=report.doctor,
                appointment_date=timezone.localdate(),
                appointment_time=timezone.localtime().time().replace(microsecond=0),
                consultancy_fee=prev.consultancy_fee,
                appointment_mode=prev.appointment_mode,
                problem_category=prev.problem_category,
                urgency_level=prev.urgency_level,
                symptoms=report.report_note or prev.symptoms,
                meeting_link='',
                payment_method=prev.payment_method,
                transaction_id='',
                payment_number='',
                payment_status='Unpaid',
                visit_note='Follow-up report update',
                status='Completed'
            )

            prescription = form.save(commit=False)
            prescription.appointment = new_appointment
            prescription.doctor = report.doctor
            prescription.patient = report.patient
            prescription.symptoms_snapshot = report.report_note or prev.symptoms
            prescription.save()

            report.status = 'Processed'
            report.save(update_fields=['status'])

            messages.success(request, "Report updated successfully and moved to appointments.")
            return redirect('doctor_report_show_list')
    else:
        form = ReportPrescriptionUpdateForm()

    return render(request, 'hms/doctor/report_show_update.html', {
        'doctor': doctor,
        'report': report,
        'form': form,
    })

from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MedicalTest, TestReport, TestReportItem
from .forms import TestReportForm


@login_required
def receptionist_create_test_report(request):
    if not hasattr(request.user, 'receptionist'):
        return redirect('home')

    receptionist = request.user.receptionist

    if request.method == 'POST':
        form = TestReportForm(request.POST)
        if form.is_valid():
            selected_tests = form.cleaned_data['tests']

            report = form.save(commit=False)
            report.receptionist = receptionist
            report.organization_name = receptionist.organization_name
            report.total_cost = sum((t.price for t in selected_tests), Decimal('0.00'))
            report.save()

            for test in selected_tests:
                TestReportItem.objects.create(
                    report=report,
                    medical_test=test,
                    test_name=test.name,
                    test_price=test.price
                )

            messages.success(request, "Test report created successfully.")
            return redirect('receptionist_all_test_reports')
    else:
        form = TestReportForm()

    available_tests = MedicalTest.objects.filter(is_active=True).order_by('name')

    return render(request, 'hms/receptionist/create_test_report.html', {
        'form': form,
        'receptionist': receptionist,
        'available_tests': available_tests,
    })


@login_required
def receptionist_all_test_reports(request):
    if not hasattr(request.user, 'receptionist'):
        return redirect('home')

    receptionist = request.user.receptionist

    reports = TestReport.objects.filter(
        organization_name__iexact=receptionist.organization_name
    ).order_by('-created_at')

    return render(request, 'hms/receptionist/all_test_reports.html', {
        'reports': reports,
        'receptionist': receptionist,
    })


@login_required
def receptionist_view_test_report(request, report_id):
    if not hasattr(request.user, 'receptionist'):
        return redirect('home')

    receptionist = request.user.receptionist

    report = get_object_or_404(
        TestReport.objects.prefetch_related('items'),
        id=report_id,
        organization_name__iexact=receptionist.organization_name
    )

    return render(request, 'hms/receptionist/view_test_report.html', {
        'report': report,
        'receptionist': receptionist,
    })

def logout_view(request):
    logout(request)
    return redirect('home')


