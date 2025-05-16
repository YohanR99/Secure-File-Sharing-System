from django.core.management.base import BaseCommand
from djfsender.utilities.blockchain import Blockchain

class Command(BaseCommand):
    help = 'Validates the blockchain for integrity'

    def handle(self, *args, **kwargs):
        blockchain = Blockchain()
        is_valid = blockchain.validate_chain()  

        if is_valid:
            self.stdout.write(self.style.SUCCESS('Blockchain is valid and untampered.'))
        else:
            self.stdout.write(self.style.ERROR('Blockchain integrity check failed.'))
