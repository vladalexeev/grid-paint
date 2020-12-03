import base64
import hashlib
import json


HEADER = {
    'version': '1.0'
}


def make_signature(text, salt):
    s = hashlib.sha256()
    s.update((text + salt).encode())
    return s.digest()


def encode_token(data, salt):
    data_str = json.dumps(data)

    signature = make_signature(data_str, salt)

    return '.'.join([
        base64.b64encode(json.dumps(HEADER).encode()).decode(),
        base64.b64encode(data_str.encode()).decode(),
        base64.b64encode(signature).decode()
    ])


def generate_token(salt, artwork_id, user_id, nickname, avatar_url):
    return encode_token(
        {
            'artwork_id': artwork_id,
            'user': {
                'user_id': user_id,
                'nickname': nickname,
                'avatar_url': avatar_url
            }
        },
        salt
    )
