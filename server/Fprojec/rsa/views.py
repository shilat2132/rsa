import sys
import os
from math import gcd

# Add the 'machines' directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'machines'))

from utils2 import binaryToDecimal, decimalToBinaryList, tapeToBinaryString, is_prime
from RSA import RSA

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import copy
import math

# In-memory queues to hold steps for chunked sending
queues = {
    "key": {},
    "encryption": {},
    "decryption": {}
}

chunk_size = 100

# Strip only the "steps" field from a single step (shallow)
def strip_step(step):
    step_copy = copy.deepcopy(step)
    if "steps" in step_copy:
        step_copy["steps"] = []
    return step_copy

# Build a flattened queue of steps while maintaining the path
def build_queue(step, path=None):
    if path is None:
        path = []

    queue = []

    # Append a stripped version of the current step (shallow strip)
    queue.append((path, strip_step(step)))

    # Continue recursively on the original step (which includes steps)
    if "steps" in step:
        for idx, substep in enumerate(step["steps"]):
            subpath = path + [idx]
            queue.extend(build_queue(substep, subpath))

    return queue



# Return a chunk of steps from the queue
# chunk_size defines how many steps are sent each time
def get_chunk(queue):
    if len(queue) < chunk_size:
        chunk = copy.deepcopy(queue)
        del queue[:len(queue)]
        return chunk
    chunk = queue[:chunk_size]
    del queue[:chunk_size]
    return chunk

@csrf_exempt
def key(request):
    """
    Generate the public and private keys using the RSA algorithm.
    First call returns the stripped main_step.
    Next calls return chunks of steps.
    """
    if request.method == 'POST':
        data = json.loads(request.body)

        if "fetch_chunk" in data:
            queue = queues["key"].get("queue")
            if queue is None:
                return JsonResponse({"error": "No key generation in progress."}, status=400)

            chunk = get_chunk(queue)
            return JsonResponse({"chunk": chunk, "finished": len(queue) == 0})

        # Regular request to start key generation
        try:
            p = int(data['p'])
            q = int(data['q'])
            b = int(data['b'])
        except (ValueError, KeyError):
            return JsonResponse({"error": "Inputs must be integers."}, status=400)

        # Check all numbers are greater than 0 and are integers
        if not (isinstance(p, int) and isinstance(q, int) and isinstance(b, int)):
            return JsonResponse({"error": "Inputs must be integers."}, status=400)
        if p <= 0 or q <= 0 or b <= 0:
            return JsonResponse({"error": "Inputs must be greater than 0."}, status=400)

        # Check if p and q are primes
        if not is_prime(p) or not is_prime(q):
            return JsonResponse({"error": "p and q must be prime numbers."}, status=400)

        # Check whether gcd(b, phi_n) == 0
        phi_n = (p - 1) * (q - 1)
        if gcd(b, phi_n) != 1:
            return JsonResponse({"error": "gcd(b, phi_n) must be 1."}, status=400)

        pList = decimalToBinaryList(p)
        qList = decimalToBinaryList(q)
        bList = decimalToBinaryList(b)

        rsa = RSA(pList, qList, bList)
        main_step, nList, aList = rsa.getKeyGeneration()
        n, a = binaryToDecimal(nList), binaryToDecimal(aList)

        # Build queue
        queue = build_queue(main_step, [0])
        queues["key"]["queue"] = queue

        # Return stripped main_step without internal steps
        
        return JsonResponse({
            "total_chunks": math.ceil(len(queue)/chunk_size),
            "results": {
                'p': p,
                'q': q,
                'b': b,
                'n': n,
                'a': a,
                "resLists": {
                    'p': tapeToBinaryString(pList), 
                    'q': tapeToBinaryString(qList), 
                    'b': tapeToBinaryString(bList), 
                    'n': tapeToBinaryString(nList), 
                    'a': tapeToBinaryString(aList) }

            },
            
            'main_step': copy.deepcopy(queue[0][1])
        })

@csrf_exempt
def encryption(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        if "fetch_chunk" in data:
            queue = queues["encryption"].get("queue")
            if queue is None:
                return JsonResponse({"error": "No encryption in progress."}, status=400)

            chunk = get_chunk(queue)
            return JsonResponse({"chunk": chunk, "finished": len(queue) == 0})

        x = int(data['x'])
        b = int(data['b'])
        n = int(data['n'])

        if not isinstance(x, int):
            return JsonResponse({"error": "x must be an integer."}, status=400)
        if x <= 0:
            return JsonResponse({"error": "x must be greater than 0."}, status=400)
        if x >= n:
            return JsonResponse({"error": "x must be less than n."}, status=400)

        xList = decimalToBinaryList(x)
        bList = decimalToBinaryList(b)
        nList = decimalToBinaryList(n)
       
        rsaEncrypt = RSA(b=bList, n=nList)
        main_step, y, yList = rsaEncrypt.encrypt(x, xList)

        queue = build_queue(main_step, [0])
        queues["encryption"]["queue"] = queue

        return JsonResponse({
            "total_chunks": math.ceil(len(queue)/chunk_size),
            "results": {
                'y': y,
                'x': x,
                "resLists": {
                    'y': tapeToBinaryString(yList),
                    'x': tapeToBinaryString(xList)
                }
            },
            "main_step": copy.deepcopy(queue[0][1])
        })


@csrf_exempt
def decryption(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        if "fetch_chunk" in data:
            queue = queues["decryption"].get("queue")
            if queue is None:
                return JsonResponse({"error": "No decryption in progress."}, status=400)

            chunk = get_chunk(queue)
            return JsonResponse({"chunk": chunk, "finished": len(queue) == 0})

        y = int(data['y'])
        a = int(data['a'])
        p = int(data['p'])
        q = int(data['q'])
        n = int(data['n'])

        if not isinstance(y, int):
            return JsonResponse({"error": "y must be an integer."}, status=400)
        if y <= 0:
            return JsonResponse({"error": "y must be greater than 0."}, status=400)
        if y >= n:
            return JsonResponse({"error": "y must be less than n."}, status=400)


        yList = decimalToBinaryList(y)
        aList = decimalToBinaryList(a)
        pList = decimalToBinaryList(p)
        qList = decimalToBinaryList(q)
        nList = decimalToBinaryList(n)

        rsaDecrypt = RSA(a=aList, p=pList, q=qList, n=nList)
        main_step, x, xList = rsaDecrypt.decrypt(y, yList)

        queue = build_queue(main_step, [0])
        queues["decryption"]["queue"] = queue

        return JsonResponse({
            "total_chunks": math.ceil(len(queue)/chunk_size),
            "results": {
                "y": y,
                "x": x,
                "resLists": {
                    'x': tapeToBinaryString(xList),
                    'y': tapeToBinaryString(yList)
                }
            },
            "main_step": copy.deepcopy(queue[0][1])
        })
