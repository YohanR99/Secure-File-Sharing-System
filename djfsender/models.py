from django.db import models
from django.contrib.auth.models import User
from accounts.models import Department
from datetime import datetime
from autoslug import AutoSlugField
from shortuuid.django_fields import ShortUUIDField
from .utilities.validate_files import check_file


class FileSender(models.Model):
    file_id = ShortUUIDField(
        length=10,
        max_length=13,
        alphabet='21345687abcdefg1234',
        verbose_name='File ID',
        primary_key=True
    )

    original_file_name = models.CharField(  # ✅ More descriptive name
        max_length=255,
        help_text='Original file name as uploaded by user'
    )

    slug = AutoSlugField(
        populate_from='original_file_name',
        unique_with=['file_id', 'created__day'],
    )

    file = models.FileField(
        upload_to='uploads/',  # ✅ Optional: saves to /media/uploads/
        validators=[check_file]
    )

    file_hash = models.CharField(max_length=200, help_text='SHA256 hash of file before upload to Pinata')
    ipfs_hash = models.CharField(max_length=300)
    pin_size = models.IntegerField(help_text='Size in KB', default=0)
    pin_time_stamp = models.CharField(max_length=100, help_text='Timestamp of IPFS pin', default='')
    file_description = models.TextField(help_text='File description')

    created = models.DateTimeField(auto_now_add=True, help_text='Record creation time')
    last_updated = models.DateTimeField(default=datetime.now, help_text='Last updated time')

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text='User who uploaded the file'
    )

    allowed_departments = models.ManyToManyField(
        Department,
        blank=True,
        help_text='Departments allowed to download this file'
    )

    allowed_users = models.ManyToManyField(
        User,
        related_name='accessible_files',
        blank=True,
        help_text='Specific users allowed to download this file'
    )

    def __str__(self):
        return self.original_file_name

    class Meta:
        ordering = ['created']
