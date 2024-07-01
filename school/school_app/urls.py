from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('haberler/', views.haberler, name='haberler'),
    path('club-detail/<int:club_id>', views.club_detail, name='club-detail'),
    path('club-activity/<int:club_id>/', views.club_activity, name='club-activity'),
    path('club-manager/', views.admin_home, name='admin-home'),
    path('club-manager/logout', views.admin_logout, name='admin-logout'),
    path('sks-admin/logout', views.sks_logout, name='sks-logout'),
    path('club-manager/login/', views.admin_login, name='admin-login'),
    path('sks-admin/', views.sks_home, name='sks-home'),
    path('sks-admin/login/', views.sks_login, name='sks-login'),
    path('create-activity/', views.create_activity, name='create_activity'),
    path('toggle-activity/<int:activity_id>/', views.toggle_activity, name='toggle_activity'),
    path('student_login/', views.student_login,name='student-login'),
    path('student_home/',views.student_home,name='student-home'),
    path('home-logout/', views.student_logout, name='student-logout'),

]
