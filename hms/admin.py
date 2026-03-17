from django.contrib import admin
from .models import DoctorPatientBookmark, Patient, Doctor, Appointment, ContactMessage, Prescription, Receptionist, TestReportItem, MedicalTest, ReportShow, ReportShowFile, TestReport
admin.site.register(Receptionist)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(ContactMessage)
admin.site.register(Prescription)
admin.site.register(DoctorPatientBookmark)
admin.site.register(ReportShow)
admin.site.register(ReportShowFile)
admin.site.register(MedicalTest)
admin.site.register(TestReport)
admin.site.register(TestReportItem)