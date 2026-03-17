from django import forms
from django.contrib.auth.models import User
from .models import ContactMessage, Appointment, Doctor, Patient, Prescription, Receptionist, ContactMessage


class StyledFormMixin:
    def apply_style(self):
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


from django import forms
from django.contrib.auth.models import User
from .models import Patient, Doctor, Receptionist


class PatientRegisterForm(forms.Form, StyledFormMixin):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    username = forms.CharField(max_length=100)
    contact = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female')],
        widget=forms.RadioSelect
    )
    photo = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_contact(self):
        contact = self.cleaned_data['contact']
        if Patient.objects.filter(contact=contact).exists():
            raise forms.ValidationError("Contact already exists.")
        return contact

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class DoctorRegisterForm(forms.Form, StyledFormMixin):
    name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    contact = forms.CharField(max_length=20)
    specialist = forms.CharField(max_length=100)
    hospital_name = forms.CharField(max_length=150)
    location = forms.CharField(max_length=150)
    about = forms.CharField(widget=forms.Textarea)
    consultancy_fee = forms.DecimalField(max_digits=10, decimal_places=2)
    photo = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()
        self.fields['about'].widget.attrs.update({'rows': 4})

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class ReceptionistRegisterForm(forms.Form, StyledFormMixin):
    organization_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    contact = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    profile_picture = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class LoginForm(forms.Form, StyledFormMixin):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()


class ContactForm(forms.ModelForm, StyledFormMixin):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'contact', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()


from django import forms
from .models import Doctor

from django import forms
from django.contrib.auth.models import User
from .models import Doctor


class AddDoctorForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Doctor
        fields = [
            'username',
            'email',
            'password',
            'confirm_password',
            'name',
            'specialist',
            'hospital_name',
            'location',
            'contact',
            'consultancy_fee',
            'about',
            'photo',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'specialist': forms.TextInput(attrs={'class': 'form-control'}),
            'hospital_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'consultancy_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class AppointmentForm(forms.ModelForm):
    appointment_mode = forms.ChoiceField(
        choices=Appointment.MODE_CHOICES,
        widget=forms.RadioSelect
    )

    urgency_level = forms.ChoiceField(
        choices=Appointment.URGENCY_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Appointment
        fields = [
            'doctor',
            'appointment_date',
            'appointment_time',
            'appointment_mode',
            'problem_category',
            'urgency_level',
            'symptoms',
            'meeting_link',
            'visit_note',
            'payment_method',
            'transaction_id',
        ]
        widgets = {
            'appointment_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'appointment_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'problem_category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'symptoms': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Describe your symptoms or current problem...'
            }),
            'meeting_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter online meeting link'
            }),
            'visit_note': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional visit note'
            }),
            'doctor': forms.Select(attrs={
                'class': 'form-select'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'transaction_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter bKash transaction ID'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['doctor'].queryset = Doctor.objects.filter(is_approved=True)

        self.fields['payment_method'].choices = [
            ('', 'Select Payment Method'),
            ('Cash', 'Cash'),
            ('Bkash', 'Bkash'),
        ]
        self.fields['payment_method'].required = False
        self.fields['transaction_id'].required = False

    def clean(self):
        cleaned_data = super().clean()

        appointment_mode = cleaned_data.get('appointment_mode')
        meeting_link = cleaned_data.get('meeting_link')
        payment_method = cleaned_data.get('payment_method')
        transaction_id = cleaned_data.get('transaction_id')

        # Online হলে meeting link লাগবে
        if appointment_mode == 'Online' and not meeting_link:
            self.add_error('meeting_link', 'Meeting link is required for online appointments.')

        # Online হলে শুধু Bkash allowed
        if appointment_mode == 'Online':
            if payment_method != 'Bkash':
                self.add_error('payment_method', 'Online appointment requires bKash payment.')

        # Offline হলে Cash বা Bkash যেকোনোটা
        if appointment_mode == 'Offline':
            if payment_method not in ['Cash', 'Bkash']:
                self.add_error('payment_method', 'Please choose Cash or bKash for offline appointment.')

        # Bkash হলে transaction ID লাগবে
        if payment_method == 'Bkash' and not transaction_id:
            self.add_error('transaction_id', 'Transaction ID is required for bKash payment.')

        # Cash হলে transaction ID থাকা উচিত না
        if payment_method == 'Cash':
            cleaned_data['transaction_id'] = ''

        return cleaned_data

    
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Prescription

class DoctorProfileForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    specialist = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    hospital_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    location = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    contact = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    consultancy_fee = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    about = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username=username)
        if self.user_instance:
            qs = qs.exclude(id=self.user_instance.id)
        if qs.exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            qs = User.objects.filter(email=email)
            if self.user_instance:
                qs = qs.exclude(id=self.user_instance.id)
            if qs.exists():
                raise forms.ValidationError("Email already exists.")
        return email


class DoctorPasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        if self.user_instance and not self.user_instance.check_password(current_password):
            raise forms.ValidationError("Current password is incorrect.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")

        if self.user_instance and new_password:
            validate_password(new_password, self.user_instance)

        return cleaned_data


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['prescription_text', 'test', 'advice']
        widgets = {
            'prescription_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 7,
                'placeholder': 'Write medicines and dosage...'
            }),
            'test': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write required tests if needed...'
            }),
            'advice': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write patient advice...'
            }),
        }

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Patient

class PatientProfileForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    contact = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female')],
        widget=forms.RadioSelect
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username=username)
        if self.user_instance:
            qs = qs.exclude(id=self.user_instance.id)
        if qs.exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            qs = User.objects.filter(email=email)
            if self.user_instance:
                qs = qs.exclude(id=self.user_instance.id)
            if qs.exists():
                raise forms.ValidationError("Email already exists.")
        return email


class PatientPasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        if self.user_instance and not self.user_instance.check_password(current_password):
            raise forms.ValidationError("Current password is incorrect.")
        return current_password
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")

        if self.user_instance and new_password:
            validate_password(new_password, self.user_instance)

        return cleaned_data
    
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class AdminProfileForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username=username)
        if self.user_instance:
            qs = qs.exclude(id=self.user_instance.id)
        if qs.exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            qs = User.objects.filter(email=email)
            if self.user_instance:
                qs = qs.exclude(id=self.user_instance.id)
            if qs.exists():
                raise forms.ValidationError("Email already exists.")
        return email


class AdminPasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        if self.user_instance and not self.user_instance.check_password(current_password):
            raise forms.ValidationError("Current password is incorrect.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")

        if self.user_instance and new_password:
            validate_password(new_password, self.user_instance)

        return cleaned_data

from django import forms
from django.contrib.auth.models import User
from .models import Receptionist, Patient


class AdminAddReceptionistForm(forms.Form):
    organization_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    contact = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    branch_address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class AdminAddPatientForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    contact = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female')],
        widget=forms.RadioSelect
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_contact(self):
        contact = self.cleaned_data['contact']
        if contact and Patient.objects.filter(contact=contact).exists():
            raise forms.ValidationError("Contact already exists.")
        return contact

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

from django import forms

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class ReceptionistProfileForm(forms.Form):
    organization_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    contact = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    branch_address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        self.receptionist_instance = kwargs.pop('receptionist_instance', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username=username)
        if self.user_instance:
            qs = qs.exclude(id=self.user_instance.id)
        if qs.exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            qs = User.objects.filter(email=email)
            if self.user_instance:
                qs = qs.exclude(id=self.user_instance.id)
            if qs.exists():
                raise forms.ValidationError("Email already exists.")
        return email


class ReceptionistPasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        if self.user_instance and not self.user_instance.check_password(current_password):
            raise forms.ValidationError("Current password is incorrect.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")

        if self.user_instance and new_password:
            validate_password(new_password, self.user_instance)

        return cleaned_data

from django import forms
from django.contrib.auth.models import User
from .models import Patient, Appointment, Doctor


class WalkInPatientAppointmentForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    contact = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female')],
        widget=forms.RadioSelect
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    appointment_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    appointment_mode = forms.ChoiceField(
        choices=Appointment.MODE_CHOICES,
        widget=forms.RadioSelect
    )
    problem_category = forms.ChoiceField(
        choices=Appointment.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    urgency_level = forms.ChoiceField(
        choices=Appointment.URGENCY_CHOICES,
        widget=forms.RadioSelect
    )
    symptoms = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-control',
            'placeholder': 'Describe symptoms or patient complaint...'
        })
    )
    meeting_link = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter online meeting link'
        })
    )
    visit_note = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter chamber / branch / visit note'
        })
    )

    def __init__(self, *args, **kwargs):
        doctor_queryset = kwargs.pop('doctor_queryset', Doctor.objects.none())
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = doctor_queryset

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_contact(self):
        contact = self.cleaned_data['contact']
        if Patient.objects.filter(contact=contact).exists():
            raise forms.ValidationError("Contact number already exists.")
        return contact

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        appointment_mode = cleaned_data.get('appointment_mode')
        meeting_link = cleaned_data.get('meeting_link')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        if appointment_mode == 'Online' and not meeting_link:
            self.add_error('meeting_link', 'Meeting link is required for online appointments.')

        return cleaned_data
    
from django import forms
from .models import ReportShow, Doctor, Appointment, Prescription


from django import forms
from .models import ReportShow, Doctor, Appointment


class PatientReportShowForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.none(),
        empty_label="Select Previous Doctor"
    )
    previous_prescription = forms.FileField(required=False)
    report_file = forms.FileField(required=False)

    class Meta:
        model = ReportShow
        fields = ['doctor', 'previous_prescription', 'report_note']
        widgets = {
            'report_note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your current report/update note...'
            }),
        }

    def __init__(self, *args, **kwargs):
        patient = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)

        if patient:
            previous_doctor_ids = Appointment.objects.filter(
                patient=patient
            ).values_list('doctor_id', flat=True).distinct()

            self.fields['doctor'].queryset = Doctor.objects.filter(id__in=previous_doctor_ids)

        self.fields['doctor'].widget.attrs.update({'class': 'form-control'})
        self.fields['previous_prescription'].widget.attrs.update({'class': 'form-control'})
        self.fields['report_file'].widget.attrs.update({'class': 'form-control'})


class ReportPrescriptionUpdateForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['prescription_text', 'test', 'advice']
        widgets = {
            'prescription_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 7,
                'placeholder': 'Write medicines and dosage...'
            }),
            'test': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write required tests if needed...'
            }),
            'advice': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write patient advice...'
            }),
        }


from django import forms
from .models import TestReport, MedicalTest


class TestReportForm(forms.ModelForm):
    tests = forms.ModelMultipleChoiceField(
        queryset=MedicalTest.objects.filter(is_active=True),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'id': 'id_tests'
        }),
        required=True
    )

    class Meta:
        model = TestReport
        fields = ['patient_name', 'age', 'gender', 'contact_number']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(
                choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
                attrs={'class': 'form-control'}
            ),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
        }