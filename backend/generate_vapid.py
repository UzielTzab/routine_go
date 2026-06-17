import json
import base64
import os

try:
    from pywebpush import generate_vapid_keypair
except ImportError:
    os.system("pip install pywebpush==2.0.0")
    from pywebpush import generate_vapid_keypair

k = generate_vapid_keypair()
print("VAPID_PRIVATE_KEY=", k['private_key'])
print("VAPID_PUBLIC_KEY=", k['public_key'])
