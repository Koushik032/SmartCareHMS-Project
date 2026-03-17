from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_page, name='contact'),

    path('login/admin/', views.admin_login, name='admin_login'),
    path('login/doctor/', views.doctor_login, name='doctor_login'),
    path('login/patient/', views.patient_login, name='patient_login'),
    path('login/receptionist/', views.receptionist_login, name='receptionist_login'),

    path('register/doctor/', views.doctor_register, name='doctor_register'),
    path('register/patient/', views.patient_register, name='patient_register'),
    path('register/receptionist/', views.receptionist_register, name='receptionist_register'),

    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('dashboard/receptionist/', views.receptionist_dashboard, name='receptionist_dashboard'),

    path('receptionist/profile/', views.receptionist_profile, name='receptionist_profile'),
    path('patient/profile/', views.patient_profile, name='patient_profile'),
    path('doctor/profile/', views.doctor_profile, name='doctor_profile'),
    path('admin/profile/', views.admin_profile, name='admin_profile'),

    path('patient/hospitals/', views.patient_hospitals, name='patient_hospitals'),
    path('patient/hospital/<str:organization_name>/doctors/',views.patient_hospital_doctors,name='patient_hospital_doctors'),
    path('patient/doctors/', views.patient_doctors, name='patient_doctors'),
    path('patient/book-appointment/', views.book_appointment, name='book_appointment'),
    path('patient/history/', views.patient_history, name='patient_history'),
    path('patient/cancel/<int:pk>/', views.patient_cancel_appointment, name='patient_cancel_appointment'),
    path('patient/prescriptions/', views.patient_prescriptions, name='patient_prescriptions'),
    path('patient/prescription/<int:pk>/', views.patient_prescription_detail, name='patient_prescription_detail'),
    path('patient/history/prescription/<int:appointment_id>/', views.patient_view_prescription, name='patient_view_prescription'),


    # path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/bookmark-patient/<int:patient_id>/', views.doctor_toggle_bookmark_patient, name='doctor_toggle_bookmark_patient'),
    path('doctor/patients/', views.doctor_patients, name='doctor_patients'),
    path('doctor/patients/<int:patient_id>/', views.doctor_patient_detail, name='doctor_patient_detail'),
    path('doctor/pending-appointments/', views.doctor_pending_appointments, name='doctor_pending_appointments'),
    path('doctor/cancel/<int:pk>/', views.doctor_cancel_appointment, name='doctor_cancel_appointment'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('doctor/complete/<int:pk>/', views.doctor_complete_appointment, name='doctor_complete_appointment'),
    path('doctor/add-prescription/<int:appointment_id>/', views.doctor_add_prescription, name='doctor_add_prescription'),
    path('doctor/prescription/<int:appointment_id>/', views.doctor_view_prescription, name='doctor_view_prescription'),

    path('admin/patients/', views.admin_patient_list, name='admin_patient_list'),
    path('admin/doctors/', views.admin_doctor_list, name='admin_doctor_list'),
    path('admin/appointments/', views.admin_appointment_list, name='admin_appointment_list'),
    path('admin/add-doctor/', views.admin_add_doctor, name='admin_add_doctor'),
    path('admin/add-receptionist/', views.admin_add_receptionist, name='admin_add_receptionist'),
    path('admin/add-patient/', views.admin_add_patient, name='admin_add_patient'),
    path('admin/delete-doctor/<int:pk>/', views.admin_delete_doctor, name='admin_delete_doctor'),
    path('admin/doctor-requests/', views.admin_doctor_requests, name='admin_doctor_requests'),
    path('admin/approve-doctor/<int:pk>/', views.admin_approve_doctor, name='admin_approve_doctor'),
    path('admin/remove-doctor-request/<int:pk>/', views.admin_doctor_requests, name='admin_remove_doctor_request'),
    path('admin/messages/', views.admin_messages, name='admin_messages'),

    path('receptionist/appointment-status/<int:pk>/<str:status>/',views.receptionist_update_appointment_status,name='receptionist_update_appointment_status'),
    path('receptionist/create-appointment/', views.receptionist_create_appointment, name='receptionist_create_appointment'),
    path('receptionist/doctors/', views.receptionist_doctors, name='receptionist_doctors'),
    path('receptionist/patients/', views.receptionist_patients, name='receptionist_patients'),
    path('receptionist/all-appointments/', views.receptionist_all_appointments, name='receptionist_all_appointments'),
    path('receptionist/walkin-with-appointment/',views.receptionist_walkin_with_appointment,name='receptionist_walkin_with_appointment'),
    path('receptionist/test-report/create/', views.receptionist_create_test_report, name='receptionist_create_test_report'),
    path('receptionist/test-reports/', views.receptionist_all_test_reports, name='receptionist_all_test_reports'),
    path('receptionist/test-report/<int:report_id>/', views.receptionist_view_test_report, name='receptionist_view_test_report'),

    path('patient/report-show/', views.patient_report_show, name='patient_report_show'),
    path('doctor/report-show/', views.doctor_report_show_list, name='doctor_report_show_list'),
    path('doctor/report-show/<int:report_id>/', views.doctor_report_show_detail, name='doctor_report_show_detail'),
    path('doctor/report-show/<int:report_id>/update/', views.doctor_report_show_update, name='doctor_report_show_update'),

    path('logout/', views.logout_view, name='logout'),
]