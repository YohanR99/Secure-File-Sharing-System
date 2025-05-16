from django.conf import settings
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseForbidden, FileResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .service import FileSenderService
from .forms import FileSenderForm
from .models import FileSender
from accounts.models import Profile
from .utilities.aes_cipher import decrypt_data
import requests
import tempfile
from django.db import models


class UploadView(SuccessMessageMixin, CreateView):
    form_class = FileSenderForm
    success_message = "File uploaded successfully"
    model = FileSender
    template_name = 'upload.html'  
    success_url = None

    def form_valid(self, form):
        for field in self.request.FILES.keys():
            for formfile in self.request.FILES.getlist(field):
                file_ext = formfile.content_type.split('/')[-1]
                encrypted_name = FileSenderService.get_file_name()

                # ✅ Step 1: Save AES-encrypted file to media/
                FileSenderService.upload_to_media_root(formfile, encrypted_name, file_ext)
                file_path = f'{settings.MEDIA_ROOT}/{encrypted_name}.{file_ext}'

                # ✅ Step 2: Compute SHA-256 hash of encrypted file
                with open(file_path, 'rb') as f:
                    file_hash = FileSenderService.get_object_hash(f.read())

                if not FileSenderService.check_hash_exist(file_hash):
                    # ✅ Step 3: Upload encrypted file to IPFS
                    ipfs_result = FileSenderService.ipfs_pin_file(encrypted_name, file_path)

                    # ✅ Step 4: Save file metadata to DB
                    file_instance = FileSenderService.create_file_sender(
                        original_file_name=formfile.name,
                        file_path=file_path,
                        file_hash=file_hash,
                        ipfs_hash=ipfs_result['IpfsHash'],
                        pin_size=ipfs_result['PinSize'],
                        file_description=form.cleaned_data['file_description'],
                        time_stamp=ipfs_result['Timestamp'],
                        uploaded_by=self.request.user
                    )

                    # ✅ Step 5: Assign access permissions
                    file_instance.allowed_departments.set(form.cleaned_data['departments_allowed'])
                    file_instance.save()

        return HttpResponsePermanentRedirect(
            reverse('file_details', kwargs={'file_id': FileSenderService.get_file_id(file_hash)})
        )

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class FileDetails(DetailView):
    model = FileSender
    queryset = FileSender.objects.all()
    template_name = 'file-detail.html'
    context_object_name = 'file'
    pk_url_kwarg = 'file_id'

    def get_queryset(self):
        return FileSenderService.get_file_details(self.kwargs.get('file_id'))





@login_required
def download_file(request, file_id):
    file = get_object_or_404(FileSender, file_id=file_id)
    user_profile = getattr(request.user, 'profile', None)

    has_access = (
        request.user == file.uploaded_by or
        file.allowed_users.filter(id=request.user.id).exists() or
        (
            user_profile and
            file.allowed_departments.filter(id=user_profile.department_id).exists()
        )
    )

    if not has_access:
        return HttpResponseForbidden("You are not allowed to download this file.")

    ipfs_url = f"https://gateway.pinata.cloud/ipfs/{file.ipfs_hash}"
    response = requests.get(ipfs_url)

    if response.status_code != 200:
        return render(request, 'download.html', {
            'file': file,
            'ipfs_url': '',
            'error': 'Could not fetch the encrypted file from IPFS.'
        })

    try:
        # ✅ Decrypt the file
        encrypted_data = response.content
        decrypted_data = decrypt_data(encrypted_data)

        # ✅ Serve decrypted file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(decrypted_data)
        temp_file.seek(0)

        return FileResponse(
            temp_file,
            as_attachment=True,
            filename=file.original_file_name
        )

    except Exception as e:
        return render(request, 'download.html', {
            'file': file,
            'ipfs_url': '',
            'error': f'Decryption failed: {str(e)}'
        })


@login_required
def user_files(request):
    files = FileSender.objects.filter(uploaded_by=request.user)
    return render(request, 'user_files.html', {'files': files})
    

@login_required
def shared_files(request):
    user = request.user
    user_profile = getattr(user, 'profile', None)

    files = FileSender.objects.none()

    if user_profile:
        files = FileSender.objects.filter(
            models.Q(allowed_users=user) |
            models.Q(allowed_departments=user_profile.department)
        ).distinct()

    return render(request, 'shared_files.html', {'files': files})



# ✅ Public landing page
def landing_page(request):
    return render(request, 'landing.html')
