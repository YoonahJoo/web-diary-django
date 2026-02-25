from django import forms
from .models import Diary, DiaryFolder
from django.contrib.auth.models import User


class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '제목을 입력하세요',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '내용을 입력하세요',
                'rows': 5,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }


class DiaryFolderForm(forms.ModelForm):
    class Meta:
        model = DiaryFolder
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '폴더 이름을 입력하세요',
            }),
        }

        def clean_name(self):
            name = self.cleaned_data.get('name')
            if DiaryFolder.objects.filter(name=name, user=self.instance.user).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('이미 존재하는 폴더 이름입니다.')
            return name


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '사용자 이름을 입력하세요',
            }),
        }
