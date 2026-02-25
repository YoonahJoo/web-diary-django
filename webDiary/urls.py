from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),  # 첫 화면 URL
    path('login/', views.login_view, name='login'),  # 로그인 URL
    path('logout/', LogoutView.as_view(), name='logout'),  # 로그 아웃 URL
    path('signup/', views.signup, name='signup'),  # 회원 가입 URL
    path('folder/', views.folder_list, name='folder_list'),  # 폴더 URL
    path('folder/create/', views.folder_create, name='folder_create'),  # 폴더 생성 URL
    path('folder/<str:folder_name>/edit/', views.folder_edit, name='folder_edit'),  # 폴더 수정 URL
    path('folder/<str:folder_name>/delete/', views.folder_delete, name='folder_delete'),  # 폴더 삭제 URL
    path('folder/<str:folder_name>/', views.folder_detail, name='folder_detail'),  # 폴더 상세 URL
    path('folder/<str:folder_name>/create/', views.diary_create, name='diary_create'),  # 일기 생성 URL
    path('folder/<str:folder_name>/diary/<str:diary_title>/', views.diary_detail, name='diary_detail'),  # 일기 상세 URL
    path('folder/<str:folder_name>/diary/<str:diary_title>/edit/', views.diary_edit, name='diary_edit'),  # 일기 수정 URL
    path('folder/<str:folder_name>/diary/<str:diary_title>/delete/', views.diary_delete, name='diary_delete'),  # 일기 삭제 URL
    path('account/settings/', views.account_settings, name='account_settings'),  # 계정 설정 URL

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
