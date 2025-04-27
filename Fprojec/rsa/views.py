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

# Build a queue of all steps in a flattened structure while maintaining the path
# Each element is (path, step)
def build_queue(step, path=None):
    if path is None:
        path = []

    queue = []
    # Add the current step
    queue.append((path, step))

    # If the step has substeps, recursively add them
    if "steps" in step:
        for idx, substep in enumerate(step["steps"]):
            subpath = path + ["steps", idx]
            queue.extend(build_queue(substep, subpath))

    return queue

# Remove all internal steps to send a lightweight main_step
# Keeps only empty "steps": [] fields to preserve structure
def strip_steps(step):
    step = copy.deepcopy(step)
    if "steps" in step:
        step["steps"] = []
    return step

# Insert a chunk into the main_step structure according to the path
def insert_steps(main_step, chunk):
    for path, step in chunk:
        target = main_step
        for key in path[:-1]:
            target = target[key]
        if isinstance(path[-1], int):
            # Insert at list index
            while len(target) <= path[-1]:
                target.append(None)
            target[path[-1]] = step
        else:
            # Insert as a dictionary field
            target[path[-1]] = step

# Return a chunk of steps from the queue
# chunk_size defines how many steps are sent each time
def get_chunk(queue, chunk_size=10):
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
            # Client asks for next chunk
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
        return JsonResponse({'a': a, 'n': n, 'b': b, 'p': p, 'q': q, 'main_step': strip_steps(main_step)})

@csrf_exempt
def encryption(request):
    """
    Encrypt a number using RSA public key.
    First call returns the stripped main_step.
    Next calls return chunks of steps.
    """
    if request.method == 'POST':
        data = json.loads(request.body)

        if "fetch_chunk" in data:
            # Client asks for next chunk
            queue = queues["encryption"].get("queue")
            if queue is None:
                return JsonResponse({"error": "No encryption in progress."}, status=400)

            chunk = get_chunk(queue)
            return JsonResponse({"chunk": chunk, "finished": len(queue) == 0})

        # Regular request to start encryption
        x = int(data['x'])
        b = data['b']
        nList = data['n']

        rsaEncrypt = RSA(b=b, n=nList)
        main_step, y = rsaEncrypt.encrypt(x)

        # Build queue
        queue = build_queue(main_step)
        queues["encryption"]["queue"] = queue

        # Return stripped main_step without internal steps
        return JsonResponse({'y': y, "main_step": strip_steps(main_step)})

@csrf_exempt
def decryption(request):
    """
    Decrypt a number using RSA private key.
    First call returns the stripped main_step.
    Next calls return chunks of steps.
    """
    if request.method == 'POST':
        data = json.loads(request.body)

        if "fetch_chunk" in data:
            # Client asks for next chunk
            queue = queues["decryption"].get("queue")
            if queue is None:
                return JsonResponse({"error": "No decryption in progress."}, status=400)

            chunk = get_chunk(queue)
            return JsonResponse({"chunk": chunk, "finished": len(queue) == 0})

        # Regular request to start decryption
        y = int(data['y'])
        a = data['a']
        p = data['p']
        q = data['q']
        n = data['n']

        rsaDecrypt = RSA(a=a, p=p, q=q, n=n)
        main_step, x = rsaDecrypt.decrypt(y)

        # Build queue
        queue = build_queue(main_step)
        queues["decryption"]["queue"] = queue

        # Return stripped main_step without internal steps
        return JsonResponse({"x": x, "main_step": strip_steps(main_step)})
