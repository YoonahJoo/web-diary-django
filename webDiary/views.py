from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import DiaryFolder, Diary
from .forms import DiaryFolderForm, DiaryForm, CustomUserChangeForm
from django.db import IntegrityError


# 홈 화면 뷰
def home(request):
    return render(request, 'home.html')


# 로그인 처리 뷰
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        # 로그인 시도
        if form.is_valid():
            # 사용자 인증
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # 로그인 성공
                login(request, user)
                return redirect('folder_list')  # 로그인 후 리디렉션
            else:
                # 인증 실패 (잘못된 사용자 이름/비밀번호)
                return render(request, 'login.html', {'form': form, 'login_error': '사용자 이름 또는 비밀번호가 잘못되었습니다.'})

        # 폼 오류가 있을 경우, 폼과 함께 다시 렌더링
        return render(request, 'login.html', {'form': form, 'login_error': '사용자 이름 또는 비밀번호가 잘못되었습니다.'})

    else:
        form = AuthenticationForm()  # GET 요청 시 빈 폼을 생성

    return render(request, 'login.html', {'form': form})


# 계정 생성 뷰
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '계정이 성공적으로 생성되었습니다. 로그인 해주세요!')
            return redirect('login')
        else:
            messages.error(request, '계정 생성에 실패했습니다. 다시 시도해주세요.')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
# 계정 설정 뷰
def account_settings(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('folder_list')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'account_settings.html', {'form': form})


@login_required()
# 폴더 생성 뷰
def folder_create(request):
    if request.method == 'POST':
        form = DiaryFolderForm(request.POST)
        if form.is_valid():
            try:
                folder = form.save(commit=False)
                folder.user = request.user  # 현재 사용자와 연결
                folder.save()
                return redirect('folder_list')  # 목록 페이지로 리디렉션
            except IntegrityError:
                form.add_error('name', '이미 존재하는 폴더 이름입니다.')  # 중복 오류 메시지
    else:
        form = DiaryFolderForm()
    return render(request, 'folder_create.html', {'form': form})


@login_required()
# 폴더 목록 뷰
def folder_list(request):
    folders = DiaryFolder.objects.filter(user=request.user)
    return render(request, 'folder_list.html', {'folders': folders})


@login_required
# 폴더 수정 뷰
def folder_edit(request, folder_name):
    folder = get_object_or_404(DiaryFolder, name=folder_name, user=request.user)  # 폴더 가져오기

    if request.method == 'POST':
        form = DiaryFolderForm(request.POST, instance=folder)
        if form.is_valid():
            try:
                form.save()
                return redirect('folder_list')  # 폴더 목록으로 리디렉션
            except IntegrityError:
                form.add_error('name', '이미 존재하는 폴더 이름입니다.')
        else:
            messages.error(request, '입력된 폴더 이름이 유효하지 않습니다.')
    else:
        form = DiaryFolderForm(instance=folder)  # 기존 폴더 이름을 기본값으로 설정

    return render(request, 'folder_edit.html', {'form': form, 'folder': folder})


@login_required
# 폴더 삭제 뷰
def folder_delete(request, folder_name):
    folder = get_object_or_404(DiaryFolder, name=folder_name)

    if request.method == 'POST':
        folder.delete()
        return redirect('folder_list')  # 폴더 목록 페이지로 리디렉션

    # 삭제 확인 페이지를 생략하고 바로 삭제가 이루어짐
    return redirect('folder_list')


@login_required()
# 폴더 세부 정보 뷰
def folder_detail(request, folder_name):
    folder = get_object_or_404(DiaryFolder, name=folder_name)
    diaries = folder.diaries.all()  # 해당 폴더의 일기 목록
    return render(request, 'folder_detail.html', {'folder': folder, 'diaries': diaries})


@login_required
# 일기 생성 뷰
def diary_create(request, folder_name):
    folder = get_object_or_404(DiaryFolder, name=folder_name)
    if request.method == 'POST':
        form = DiaryForm(request.POST, request.FILES)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.folder = folder
            try:
                diary.save()
                return redirect('folder_detail', folder_name=folder.name)
            except IntegrityError:
                messages.error(request, '같은 제목의 일기가 이미 있습니다. 다른 제목을 입력해주세요.')
    else:
        form = DiaryForm()

    return render(request, 'diary_create.html', {'form': form, 'folder': folder})


@login_required
# 일기 상세 뷰
def diary_detail(request, folder_name, diary_title):
    folder = get_object_or_404(DiaryFolder, name=folder_name)
    diary = get_object_or_404(Diary, title=diary_title, folder=folder)
    return render(request, 'diary_detail.html', {'diary': diary, 'folder': folder})


@login_required
# 일기 수정 뷰
def diary_edit(request, folder_name, diary_title):
    folder = get_object_or_404(DiaryFolder, name=folder_name)
    diary = get_object_or_404(Diary, title=diary_title, folder=folder)

    if request.method == 'POST':
        form = DiaryForm(request.POST, request.FILES, instance=diary)  # request.FILES 추가
        if form.is_valid():
            form.save()
            return redirect('diary_detail', folder_name=folder.name, diary_title=diary.title)
    else:
        form = DiaryForm(instance=diary)

    return render(request, 'diary_edit.html', {'form': form, 'folder': folder, 'diary': diary})


@login_required
# 일기 삭제 뷰
def diary_delete(request, folder_name, diary_title):
    # 일기 찾기
    diary = get_object_or_404(Diary, title=diary_title, folder__name=folder_name)

    # 삭제 요청 처리 (POST 요청)
    if request.method == 'POST':
        diary.delete()
        return redirect('folder_detail', folder_name=folder_name)  # 삭제 후 폴더 상세 페이지로 리디렉션

    # 일기 삭제를 위한 POST 요청을 처리하는 페이지로 리디렉션
    return redirect('folder_detail', folder_name=folder_name)
