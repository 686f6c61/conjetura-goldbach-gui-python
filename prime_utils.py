"""
Utility functions for working with prime numbers.

This module provides efficient implementations of common prime number operations
used throughout the application, particularly for testing the Goldbach Conjecture.

Author: https://github.com/686f6c6
"""

def is_prime(n):
    """
    Check if a number is prime using trial division with optimization.
    
    Implementation uses the 6k±1 optimization, checking only for divisibility by 2 and 3
    initially, then checking only numbers of the form 6k±1 up to the square root of n.
    This provides significant performance improvements for large numbers.
    
    Args:
        n (int): The number to check for primality
        
    Returns:
        bool: True if the number is prime, False otherwise
    
    Time Complexity: O(sqrt(n))
    Space Complexity: O(1)
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    
    return True

def generate_primes(limit):
    """
    Generate a list of prime numbers up to a given limit using trial division.
    
    This function uses the is_prime() helper to test each number up to the limit.
    For very large limits, a more efficient implementation like the Sieve of Eratosthenes
    would be preferable, but for the scale of numbers typically used in this application,
    this implementation provides a good balance of simplicity and performance.
    
    Args:
        limit (int): Upper limit for prime generation (inclusive)
        
    Returns:
        list: Ordered list of all prime numbers up to the limit
    
    Time Complexity: O(n * sqrt(n)) where n is the limit
    Space Complexity: O(π(n)) where π(n) is the prime-counting function
    """
    primes = []
    for num in range(2, limit + 1):
        if is_prime(num):
            primes.append(num)
    return primes
