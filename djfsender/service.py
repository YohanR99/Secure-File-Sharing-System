from .utilities.file_name_gen import get_random_file_name
from .utilities.ipfs import pin_file
from .utilities.save_media_file import file_to_media_root
from .utilities.get_hash import object_hash
from .utilities.aes_cipher import encrypt_data
from .utilities.blockchain import Blockchain  # ✅ Blockchain logging
from .models import FileSender
from django.conf import settings


class FileSenderService:

    @staticmethod
    def get_file_name():
        return get_random_file_name(16)

    @staticmethod
    def upload_to_media_root(file, file_name, file_extension):
        """
        Encrypt the uploaded file and save it to the media directory.
        """
        raw_data = file.read()
        encrypted_data = encrypt_data(raw_data)
        media_path = f'{settings.MEDIA_ROOT}/{file_name}.{file_extension}'
        with open(media_path, 'wb') as out_file:
            out_file.write(encrypted_data)

    @staticmethod
    def get_object_hash(object_string):
        return object_hash(object_string)

    @staticmethod
    def ipfs_pin_file(file_name, file_path):
        return pin_file(file_name, file_path)

    @staticmethod
    def check_hash_exist(upload_file_hash):
        return FileSender.objects.filter(file_hash=upload_file_hash).exists()

    @staticmethod
    def create_file_sender(
        original_file_name,
        file_path,
        file_hash,
        ipfs_hash,
        pin_size,
        file_description,
        time_stamp,
        uploaded_by=None
    ):
        """
        Create a FileSender record and log the metadata to the blockchain.
        """
        # ✅ Step 1: Save file metadata to DB
        file_instance = FileSender.objects.create(
            original_file_name=original_file_name,
            file=file_path,
            file_hash=file_hash,
            ipfs_hash=ipfs_hash,
            pin_size=pin_size,
            pin_time_stamp=time_stamp,
            file_description=file_description,
            uploaded_by=uploaded_by,
        )

        # ✅ Step 2: Log metadata to local blockchain
        Blockchain().add_block({
            "file_id": file_instance.file_id,
            "file_name": original_file_name,
            "file_hash": file_hash,
            "ipfs_hash": ipfs_hash,
            "timestamp": time_stamp,
            "uploaded_by": uploaded_by.username if uploaded_by else "Anonymous"
        })

        return file_instance

    @staticmethod
    def get_file_id(file_hash):
        return FileSender.objects.get(file_hash=file_hash).file_id

    @staticmethod
    def get_file_details(file_id):
        return FileSender.objects.filter(file_id=file_id)
