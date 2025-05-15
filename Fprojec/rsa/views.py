import sys
import os

# Add the 'machines' directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'machines'))

from utils2 import binaryToDecimal, decimalToBinaryList
from RSA import RSA

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import copy

# In-memory queues to hold steps for chunked sending
queues = {
    "key": {},
    "encryption": {},
    "decryption": {}
}

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
def get_chunk(queue, chunk_size=100):
    if len(queue) < chunk_size:
        chunk = queue
        del queue[:len(queue)]
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
        p = int(data['p'])
        q = int(data['q'])
        b = int(data['b'])

        p = decimalToBinaryList(p)
        q = decimalToBinaryList(q)
        b = decimalToBinaryList(b)

        rsa = RSA(p, q, b)
        main_step, n, a = rsa.getKeyGeneration()

        # Build queue
        queue = build_queue(main_step)
        queues["key"]["queue"] = queue

        # Return stripped main_step without internal steps
        
        return JsonResponse({
            "results": {
                'a': a,
                'n': n,
                'b': b,
                'p': p,
                'q': q
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
        b = data['b']
        nList = data['n']

        rsaEncrypt = RSA(b=b, n=nList)
        main_step, y = rsaEncrypt.encrypt(x)

        queue = build_queue(main_step)
        queues["encryption"]["queue"] = queue

        return JsonResponse({
            "results": {'y': y},
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
        a = data['a']
        p = data['p']
        q = data['q']
        n = data['n']

        rsaDecrypt = RSA(a=a, p=p, q=q, n=n)
        main_step, x = rsaDecrypt.decrypt(y)

        queue = build_queue(main_step)
        queues["decryption"]["queue"] = queue

        return JsonResponse({
            "results": {"x": x},
            "main_step": copy.deepcopy(queue[0][1])
        })
