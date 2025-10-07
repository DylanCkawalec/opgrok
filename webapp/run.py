import random
import math

def is_prime_miller_rabin(n, k=40):
    """
    Probabilistic primality test using Miller-Rabin algorithm.
    Returns True if n is probably prime, False if composite.
    k is the number of rounds for accuracy (higher k means more certainty).
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as 2^s * d
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1
    
    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_large_prime(bits=1024):
    """
    Generates a random prime number with the specified number of bits.
    Uses Miller-Rabin primality test for efficiency.
    """
    while True:
        # Generate a random odd number with 'bits' bits
        num = random.getrandbits(bits)
        num |= (1 << (bits - 1)) | 1  # Ensure it's odd and has the high bit set
        if is_prime_miller_rabin(num):
            return num

# Example usage:
if __name__ == "__main__":
    prime = generate_large_prime(bits=1024)  # Generate a 1024-bit prime
    print(f"Generated prime: {prime}")
    print(f"Number of bits: {prime.bit_length()}")