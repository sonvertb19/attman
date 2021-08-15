"""AttendanceManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/',views.UserRegistration.as_view(),name="UserRegistration"),
    path('login/',views.user_login,name="login"),
    path('',views.Index,name="index"),
    path('logout/',views.logout_view,name="logout"),
    path('logout_user/',views.logout_user,name="logout_user"),
    path('subject_list/',views.SubjectListView,name="subject_list"),
    path('update_list/<int:pk>',views.SubjectUpdateView.as_view(),name="update"),
    path('delete_subject/<int:pk>',views.SubjectDeleteView.as_view(),name="delete"),
    path('dayslist',views.Dayslist,name="days"),
    path('timetable/add/',views.TimetableCreateView,name='timetable'),
    path('timetable_list/',views.TimetableList,name="timetable_list"),
    path('update_timetable/<int:pk>',views.TimetableUpdateView.as_view(),name="update_timetable"),
    path('delete_timetable/<int:pk>',views.TimetableDeleteView.as_view(),name="delete_timetable"),
    path('attendance/',views.AttendanceView,name="attendance"),
    path('mark_attendance/', views.mark_attendance, name="mark_attendance"),
    path('add_sem_details/', views.add_sem_details.as_view(), name = "add_sem_details"),
    path('attendance/subject/', views.SubjectWiseAttendanceList, name = "subject_wise_attendance"),
]
