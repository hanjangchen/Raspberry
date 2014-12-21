# -*- coding: utf-8 -*-
'''
Created on Dec 21, 2014

@author: alantai
'''
import string, random
def generate_random_id(self, size=50, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size)) 