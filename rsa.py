import random
def mod_inverse(a, m):
    # Extended Euclidean Algorithm
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keypair(bits):
    # Step 1: Choose two large prime numbers
    p = generate_prime(bits)
    q = generate_prime(bits)

    # Step 2: Compute n = p * q
    n = p * q

    # Step 3: Compute the totient (Euler's totient function) φ(n)
    phi = (p - 1) * (q - 1)

    # Step 4: Choose a public key e, where 1 < e < φ(n) and e is coprime with φ(n)
    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    # Step 5: Compute the private key d, such that (d * e) % φ(n) = 1
    d = mod_inverse(e, phi)

    # Return public and private key pairs
    return ((e, n), (d, n))

def generate_prime(bits):
    # Helper function to generate a prime number of specified bits
    prime_candidate = random.getrandbits(bits)
    while not is_prime(prime_candidate):
        prime_candidate += 1
    return prime_candidate

def is_prime(n, k=5):
    # Miller-Rabin primality test
    if n <= 1 or n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

def gcd(a, b):
    # Euclidean algorithm for finding the greatest common divisor
    while b:
        a, b = b, a % b
    return a

def encrypt(message, public_key):
    e, n = public_key
    cipher_text = [pow(ord(char), e, n) for char in message]
    return cipher_text

def decrypt(cipher_text, private_key):
    d, n = private_key
    plain_text = ''.join([chr(pow(char, d, n)) for char in cipher_text])
    return plain_text

# Example usage:
bits = 1024
public_key, private_key = generate_keypair(bits)

message = "Hello, RSA encryption!"
print(f"Original message: {message}")

# Encryption
cipher_text = encrypt(message, public_key)
print(f"Cipher text: {cipher_text}")

# Decryption
decrypted_text = decrypt(cipher_text, private_key)
print(f"Decrypted message: {decrypted_text}")
