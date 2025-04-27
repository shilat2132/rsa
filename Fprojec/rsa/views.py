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
        steps, a, n = rsa.getKeyGeneration()
        print(a)
        return JsonResponse({'a': a, 'n': n})

@csrf_exempt
def encription(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        X = int(data['X'])
        B = int(data['B'])
        N = int(data['N'])

        Y = pow(X, B, N)  # הצפנה: X^B mod N
        return JsonResponse({'Y': Y})

@csrf_exempt
def decription(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Y = int(data['Y'])
        A = int(data['A'])
        N = int(data['N'])

        X = pow(Y, A, N)  # פענוח: Y^A mod N
        return JsonResponse({'X': X})
