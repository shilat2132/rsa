from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def key(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        P = int(data['P'])
        Q = int(data['Q'])
        B = int(data['B'])

        N = P * Q
        phi = (P - 1) * (Q - 1)

        def modinv(a, m):
            for x in range(1, m):
                if (a * x) % m == 1:
                    return x
            return None

        A = modinv(B, phi)
        return JsonResponse({'A': A, 'N': N})

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
