from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns=[
    path("",views.home,name="home"),
    path("home",views.home,name="home"),
    path("login",views.admin_login,name="login"),
    path("contact",views.Contact,name="contact"),
    path("doctors",views.doctors,name="doctors"),
    path("pharmacy",views.pharmacy,name="pharmacy"),
    path("speciality",views.speciality,name="speciality"),
    path('logout/', views.log, name='log'),
    path('about',views.about,name="about"),
    path("cancer",views.cancer,name="cancer"),
    path("cardio",views.cardio,name="cardio"),
    path("gastro",views.gastro,name="gastro"),
    path('gyno', views.gyno, name='gyno'),
    path('neuro',views.neuro,name="neuro"),
    path('admin2 ',views.admin,name="admin"),
    path("Adddoctors",views.Adddoctors,name="Adddoctors"),
    path("Addpharmacy",views.Addpharmacy,name="Addpharmacy"),
    path("Addspeciality",views.Addspeciality,name="Addspeciality"),
    path("logout",views.admin_logout,name="logout"),
    path('search/', views.search, name='search'),
    path('buy/<int:medicine_id>/', views.buy_medicine, name='buy_medicine'),
    path('book-appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path("confirmation",views.confirmation,name="confirmation"),
    path('view-doctors/<int:speciality_id>/', views.view_doctors, name='view_doctors'),
     path('contconfirmation', views.contconfirmation, name='contconfirmation'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)