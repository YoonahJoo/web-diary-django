import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


class DiaryFolder(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'user'], name='unique_folder_per_user')
        ]


class Diary(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    folder = models.ForeignKey(DiaryFolder, related_name='diaries', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='diary_images/', null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'folder'], name='unique_diary_title_per_folder')
        ]

# 파일 삭제 로직 추가
@receiver(post_delete, sender=Diary)
def delete_file_on_instance_delete(sender, instance, **kwargs):
    """일기 삭제 시 이미지 파일 삭제"""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Diary)
def delete_file_on_instance_update(sender, instance, **kwargs):
    """이미지 변경 시 기존 파일 삭제"""
    if not instance.pk:
        return  # 새로 생성되는 경우
    try:
        old_file = Diary.objects.get(pk=instance.pk).image
    except Diary.DoesNotExist:
        return
    # 새 파일과 기존 파일이 다르면 기존 파일 삭제
    new_file = instance.image
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
