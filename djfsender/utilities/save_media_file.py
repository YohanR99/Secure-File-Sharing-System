import os
from django.conf import settings

# Define media path once
media_folder = settings.MEDIA_ROOT


# Upload file to media root in chunks
def file_to_media_root(file, file_name, file_extension):
    # Ensure media directory exists
    os.makedirs(media_folder, exist_ok=True)

    # Define full file path
    full_path = os.path.join(media_folder, f'{file_name}.{file_extension}')

    # Write file in chunks
    try:
        with open(full_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    except Exception as e:
        raise IOError(f"Error writing file to {full_path}: {e}")
