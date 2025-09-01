from typing import Union
class Encryptor:
    def __init__(self, key: Union[str, int]):
        if isinstance(key, str):
            self.key_bytes = key.encode('utf-8')
        elif isinstance(key, int):
            self.key_bytes = bytes([key])
        else:
            raise ValueError("Key must be a string or an integer.")
        self.key_length = len(self.key_bytes)

    def _xor(self, data_bytes: bytes) -> bytes:
        return bytes(
            data_bytes[i] ^ self.key_bytes[i % self.key_length]
            for i in range(len(data_bytes))
        )

    def encrypt(self, data: str) -> bytes:
        data_bytes = data.encode('utf-8')
        return self._xor(data_bytes)

    def decrypt(self, encrypted: bytes) -> str:
        decrypted_bytes = self._xor(encrypted)
        return decrypted_bytes