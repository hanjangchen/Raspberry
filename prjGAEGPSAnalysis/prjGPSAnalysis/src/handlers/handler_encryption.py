'''
Created on Dec 19, 2014

@author: alantai
'''
import base64
# encryption key


class EncryptionTools(object):
    def __init__(self):
        self._my_key = "csadcavrev43t24t45y54y356y65u56(*&*(UHY*T7_+_+O)O0-9i90i(I)(IU09u09u)U*(YR$&ER^%7EDRD~!E@@#R@#Rr2>:LPKBERBvdf756~BBFGBfgb"
        
    def encode(self, key, clear):
        enc = []
        if key is None:
            key = self._my_key
            
        for ith in range(len(clear)):
            key_c = key[ith % len(key)]
            enc_c = chr((ord(clear[ith]) + ord(key_c)) % 256)
            enc.append(enc_c)
        
        return base64.urlsafe_b64encode("".join(enc))


    def decode(self, key, enc):
        dec = []
        enc = base64.urlsafe_b64decode(enc)
        if key is None:
            key = self._my_key
            
        for ith in range(len(enc)):
            key_c = key[ith % len(key)]
            dec_c = chr((256 + ord(enc[ith]) - ord(key_c)) % 256)
            dec.append(dec_c)
            
        return "".join(dec)