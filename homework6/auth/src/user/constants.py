from authlib.jose import JsonWebKey, RSAKey

private_key = RSAKey.generate_key(is_private=True)
public_key = RSAKey.import_key(private_key.get_public_key())