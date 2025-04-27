import sys
import os

# הוסף את התיקיה של machines לsys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'machines'))
from utils2 import binaryToDecimal, decimalToBinaryList
from RSA import RSA


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json




@csrf_exempt
def key(request):
    """
    Generate the public and private keys using the RSA algorithm.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        p = int(data['p'])
        q = int(data['q'])
        b = int(data['b'])

        p = decimalToBinaryList(p)
        q = decimalToBinaryList(q)
        b = decimalToBinaryList(b)

        rsa = RSA(p, q, b)
        steps, n, a = rsa.getKeyGeneration()
        return JsonResponse({'a': a, 'n': n, 'b': b, 'p': p, 'q': q})

@csrf_exempt
def encryption(request):
    """
    gets the public key (b, n) - both should be tapes. and a number x to encrypt.
    returns the main_step object and the encrypted tape y.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        x = int(data['x'])
        b = data['b']
        nList = data['n']

        

        rsaEncrypt = RSA(b=b, n=nList)
        main_step, y = rsaEncrypt.encrypt(x)
        return JsonResponse({'y': y, "main_step": main_step})

@csrf_exempt
def decryption(request):
    """
    expects the private key (a, p, q) - all should be tapes and n as a tape. and a number y to decrypt.
    returns the main_step object and the decrypted tape x.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        
        y = int(data['y'])
        a = data['a'] #list
        p = data['p']
        q = data['q']
        n = data['n']

        rsaDecrypt = RSA(a=a, p=p, q=q, n=n)
        main_step, x = rsaDecrypt.decrypt(y)

        return JsonResponse({"x": x, "main_step": main_step})
