'''
Created on Dec 20, 2014

@author: alantai
'''
import random, rabinMiller, cryptomath

def generateKey(keySize):
    """ generate RSA keys and return a tuple of keys; first key is public key and second key is private key """
    
    # Creates a public/private key pair with keys that are keySize bits in
    # size. This function may take a while to run.

    # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
    # print('Generating p prime...')
    p = rabinMiller.generateLargePrime(keySize)
    # print('Generating q prime...')
    q = rabinMiller.generateLargePrime(keySize)
    n = p * q

    # Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
    # print('Generating e that is relatively prime to (p-1)*(q-1)...')
    while True:
        # Keep trying random numbers for e until one is valid.
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    # Step 3: Calculate d, the mod inverse of e.
    # print('Calculating d that is mod inverse of e...')
    d = cryptomath.findModInverse(e, (p - 1) * (q - 1))

    publicKey = (n, e)
    privateKey = (n, d)

    # print('Public key:', publicKey)
    # print('Private key:', privateKey)

    return (publicKey, privateKey)