from .blockchain import Blockchain

def log_file_to_blockchain(file_instance):
    data = {
        "file_id": file_instance.file_id,
        "original_file_name": file_instance.original_file_name,
        "file_hash": file_instance.file_hash,
        "ipfs_hash": file_instance.ipfs_hash,
        "uploader": file_instance.uploaded_by.username if file_instance.uploaded_by else "anonymous",
        "timestamp": file_instance.pin_time_stamp,
    }

    bc = Blockchain()
    bc.add_block(data)
