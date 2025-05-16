import requests
from django.conf import settings

# Pinata API URL
url = 'https://api.pinata.cloud/pinning/pinFileToIPFS'
headers = {'Authorization': f'Bearer {settings.PINETA_JWT}'}

def pin_file(file_name, file_location):
    # Prepare metadata and payload
    payload = {
        'pinataOptions': '{"cidVersion": 1}',
        'pinataMetadata': '{"name": "%s", "keyvalues": {"company": "DJIPFS"}}' % file_name,
    }

    # Open the file and prepare the multipart form-data
    with open(file_location, 'rb') as f:
        files = [('file', (file_name, f, 'application/octet-stream'))]

        response = requests.post(url, headers=headers, data=payload, files=files)

        # 🔍 Check response status
        if response.status_code != 200:
            raise Exception(f"[Pinata Error] {response.status_code}: {response.text}")

        # ✅ Success: Parse and return JSON response
        print("[Pinata Response]", response.json())  # Optional for testing
        return response.json()
