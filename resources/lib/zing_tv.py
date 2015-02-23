# -*- coding: utf-8 -*-
import random
import base64
from Crypto.Cipher import AES

a = "0IWOUZ6789ABCDEF"
b = "0123456789abcdef"
c = "GHmn|LZk|DFbv|BVd|ASlz|QWp|ghXC|Nas|Jcx|ERui|Tty|rIU|POwq|efK|Mjo".split('|')

def encrypt_aes(text, key='f_pk_ZingTV_1_@z', iv='f_iv_ZingTV_1_@z'):
    obj = AES.new(key, AES.MODE_CBC, iv)
    return obj.encrypt(text)

def decrypt_aes(cipher, key='f_pk_ZingTV_1_@z', iv='f_iv_ZingTV_1_@z'):
    obj = AES.new(key, AES.MODE_CBC, iv)
    return obj.decrypt(cipher)

def decrypt_video_url(plain):
    #decoded = base64.b64decode(plain) # your ecrypted and encoded text goes here
    return decrypt_aes(plain.decode('hex'))

def replace_encrypt(v):
    return a[b.find(v)]

def replace_decrypt(v):
    return b[a.find(v)]

def encrypt(_id):
    """Encrypt encodes an integer ID into a key."""
    return ''.join([replace_encrypt(i) for i in hex(_id)[2:]])

def decrypt(key):
    """Decrypt decodes a key into an integer ID."""
    return int(''.join([replace_decrypt(i) for i in key]), 16)

def replace_c(v):
    return c[v][random.randrange(len(c[v]))]

def get_cipher(tv_id, tail_array=None):
    if tail_array is None:
        tail_array = [10, 2, 0, 1, 0]
    random.seed()
    l = [1, 0, 8, 0, 10] + [int(i) for i in str(tv_id - 307843200)] + tail_array
    return ''.join([replace_c(i) for i in l])

def replace_enum(v):
    for index, s in enumerate(c):
        if v in s:
            return index
    return -1

def encoded_key(key):
    """Gets an encoded key of a video."""
    return get_cipher(decrypt(key))

def decode_key(encoded_key):
    y = [replace_enum(v) for v in encoded_key[5:15]]
    vid = int(''.join([str(i) for i in y])) + 307843200
    return encrypt(vid)

if __name__ == '__main__':
    # http://api.tv.zing.vn/2.0/media/info?api_key=d04210a70026ad9323076716781c223f&media_id=18515&session_key=91618dfec493ed7dc9d61ac088dff36b&
    #http://api.tv.zing.vn/2.0/program/info?api_key=d04210a70026ad9323076716781c223f&program_id=47&session_key=91618dfec493ed7dc9d61ac088dff36b&
    print(encoded_key('IWZ998C8'))
    print(decrypt('IWZ9Z0DC') -307843200 )
    plain = 'ec5ce1cbb40b6125b960545405e7ffd7e759ebc9c317ac71f20facc61fb3e0a5e70182b653dd4257354ab753f4702aaafaa1647e3410b3f37e99700f9a957c0b56767f336ebe6c8332859cd76097e1fae0d1c0e87514782848f03c9aff90c1c07971be90d8d827f4033f239833936bdf361a5e35291b5911c97f98d5ec84f45a91541a58f423f5084cb05a5b0d321b5308e642b247d8443be00be91302f07d8a31ac20c84a0276ba39c40d9d500bd9c4'
    print(decrypt_video_url(plain))