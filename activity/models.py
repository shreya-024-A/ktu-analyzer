from django.db import models
from django.contrib.auth.models import User
import hashlib

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)
    branch = models.CharField(max_length=50, blank=True)
    batch = models.CharField(max_length=10, blank=True)

class Certificate(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]
    LEVEL_CHOICES = [('I', 'Level I'), ('II', 'Level II'), ('III', 'Level III'), ('IV', 'Level IV'), ('V', 'Level V')]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    activity_name = models.CharField(max_length=200)
    level = models.CharField(max_length=5, choices=LEVEL_CHOICES, null=True, blank=True)
    file = models.FileField(upload_to='certificates/')
    file_hash = models.CharField(max_length=64, unique=True) # Duplicate prevention
    points_awarded = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Hash file to prevent duplicates
        if not self.pk:
            md5 = hashlib.md5()
            for chunk in self.file.chunks():
                md5.update(chunk)
            self.file_hash = md5.hexdigest()
        super().save(*args, **kwargs)