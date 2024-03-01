from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import jwt
import uuid

app = Flask(__name__)

# dictionary to store key pairs with their associated data
keys = {}


def generate_rsa_keypair(kid, expiry_days):
    # generates RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # serializes private key to PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # generates corresponding public key
    public_key = private_key.public_key()

    # serializes public key to PEM format
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # gets expiry timestamp
    expiry = datetime.utcnow() + timedelta(days=expiry_days)

    # stores key pair and associated data
    keys[kid] = {
        'kid': kid,
        'expiry': expiry,
        'private_key': private_key_pem,
        'public_key': public_key_pem
    }


def get_jwks():
    # filters out expired keys
    valid_keys = [keys[kid] for kid in keys if keys[kid]['expiry'] > datetime.utcnow()]

    # prepares JWKS format
    jwks = {
        'keys': [{
            'kid': key['kid'],
            'alg': 'RS256',
            'kty': 'RSA',
            'use': 'sig',
            'n': serialization.load_pem_public_key(key['public_key'], backend=default_backend()).public_numbers().n,
            'e': serialization.load_pem_public_key(key['public_key'], backend=default_backend()).public_numbers().e
        } for key in valid_keys]
    }
    return jwks


@app.route('/jwks', methods=['GET'])
def jwks():
    return jsonify(get_jwks())


@app.route('/auth', methods=['POST'])
def auth():
    kid = request.args.get('kid')  # key ID parameter
    expired = request.args.get('expired')  # expired parameter

    # if no key ID is specified it uses the first available key
    if not kid:
        kid = next(iter(keys))

    # if key ID is specified but not found or expired it will return 404
    if kid not in keys or keys[kid]['expiry'] <= datetime.utcnow():
        return 'Key not found or expired', 404

    # sign JWT token using the selected key
    payload = {'user': 'example_user'}
    private_key = serialization.load_pem_private_key(keys[kid]['private_key'], password=None, backend=default_backend())
    token = jwt.encode(payload, private_key, algorithm='RS256')

    return token


if __name__ == '__main__':
    # generates RSA key pairs with associated data
    generate_rsa_keypair(str(uuid.uuid4()), expiry_days=30)
    generate_rsa_keypair(str(uuid.uuid4()), expiry_days=60)

    app.run(port=8080)
