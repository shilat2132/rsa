# RSA Turing Machine Simulator

This project implements the **RSA cryptosystem** using **Turing machines**, offering a unique perspective on cryptographic computation.  
It simulates **three main machines**:

- **Key Generation Machine** – Generates RSA keys (`n`, `a`, `b`) step by step.
- **Encryption Machine** – Encrypts a given message using the public key.
- **Decryption Machine** – Decrypts the ciphertext using the private key.

All numbers are represented in **binary** on the tapes, and the machines run using low-level state transitions.

---

## 🎯 Motivation

This project demonstrates that a complete RSA encryption/decryption pipeline can be expressed and executed entirely with Turing machines.  
It is both a **theoretical exploration** and a **practical educational tool** to better understand the fundamentals of computation and cryptography.

---

## ✨ Features

- **Three core Turing machines** for RSA: key generation, encryption, decryption  
- **Nested submachines** – complex operations (like modular exponentiation) are broken down into smaller machines  
- **Interactive Web Interface** – built with **React** to visualize the step-by-step execution  
- **Backend with Django** – sends execution steps in chunks for smooth playback  
- **Controls** – Play, Pause, Step Forward, adjustable speed  
---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** React
- **Simulation:** Custom Turing machine engine with step-by-step execution
- **Communication:** Chunk-based API for efficient streaming

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/shilat2132/rsa.git

# make sure you are on the rsa directory

# Backend setup
cd server
pip install -r requirements.txt

#activate the virtual environment and the server
venv\Scripts\activate
cd Fprojec
python manage.py runserver
#keep this terminal window open


# Frontend setup
cd client
npm install
npm run start

#click the following: ➜  Local:   http://localhost:8080/
#this will open the browser to show the website itself

## License
This project is licensed under the MIT License.
