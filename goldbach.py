"""
Implementation of Goldbach Conjecture logic.

This module provides the core functionality for testing and analyzing the Goldbach Conjecture,
which states that every even integer greater than 2 can be expressed as the sum of two prime numbers.

The implementation focuses on efficient algorithms for finding all prime pairs that sum to a given
even number, as well as analyzing patterns across ranges of even numbers.

Author: https://github.com/686f6c6
"""

from prime_utils import generate_primes, is_prime

def find_goldbach_pairs(even_number):
    """
    Find all pairs of prime numbers that sum to the given even number.
    
    This function implements an optimized algorithm for finding Goldbach pairs:
    1. It only searches for primes up to even_number - 1
    2. It only checks prime candidates up to even_number/2 (since pairs are symmetric)
    3. For each prime p, it checks if (even_number - p) is also prime
    
    Args:
        even_number (int): An even number greater than 2
        
    Returns:
        list: List of tuples containing pairs of primes (p1, p2) where p1 + p2 = even_number
              and p1 <= p2 (to avoid duplicate pairs)
    
    Time Complexity: O(π(n) * log(n)) where π(n) is the prime-counting function
    Space Complexity: O(π(n))
    """
    if even_number <= 2 or even_number % 2 != 0:
        return []
    
    pairs = []
    # We only need to check primes up to even_number
    primes = generate_primes(even_number - 1)
    
    # Optimization: we only need to check up to even_number/2
    for prime in primes:
        if prime > even_number // 2:
            break
        
        # If even_number - prime is also prime, we found a pair
        complement = even_number - prime
        if is_prime(complement):
            pairs.append((prime, complement))
    
    return pairs

def count_goldbach_pairs(even_number):
    """
    Count the number of prime pairs that sum to the given even number.
    
    This is a convenience function that leverages find_goldbach_pairs() and returns
    just the count. For performance-critical applications where only the count is needed,
    a more optimized implementation could be created that doesn't store the actual pairs.
    
    Args:
        even_number (int): An even number greater than 2
        
    Returns:
        int: Number of prime pairs that sum to even_number
    
    Time Complexity: Same as find_goldbach_pairs()
    Space Complexity: Same as find_goldbach_pairs()
    """
    return len(find_goldbach_pairs(even_number))

def analyze_goldbach_range(start, end):
    """
    Analyze Goldbach conjecture for a range of even numbers.
    
    This function processes a range of even numbers and computes all Goldbach pairs
    for each number in the range. It returns two data structures:
    1. A dictionary mapping each even number to its list of prime pairs
    2. A dictionary mapping each even number to the count of prime pairs
    
    The function automatically handles odd start values by incrementing to the next even number.
    
    Args:
        start (int): Start of range (must be > 2, will be adjusted to even if odd)
        end (int): End of range (inclusive)
        
    Returns:
        tuple: Contains two dictionaries:
               - pairs_dict: {even_number: [(p1, p2), ...], ...}
               - counts_dict: {even_number: count, ...}
    
    Time Complexity: O(n * π(n) * log(n)) where n is the range size
    Space Complexity: O(n * π(n))
    """
    if start % 2 != 0:
        start += 1  # Ensure start is even
    
    pairs_dict = {}
    counts_dict = {}
    
    for num in range(max(4, start), end + 1, 2):  # Step by 2 to get only even numbers
        pairs = find_goldbach_pairs(num)
        pairs_dict[num] = pairs
        counts_dict[num] = len(pairs)
    
    return pairs_dict, counts_dict
