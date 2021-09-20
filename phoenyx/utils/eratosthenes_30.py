from __future__ import absolute_import, division, print_function

# from numba import jit

__all__ = ["primes"]


# @jit  # <-- ``@jit`` is a decorator that tells Numba to compile this function
# please whatever you do, don't compile this function with Numba
def primes(lim: int) -> list[int]:
    """
    Generate prime numbers up to ``lim``.\\
    P.S. this is a modified version of the Sieve of Eratosthenes

    Example
    -------
    >>> primes(10)
    ... # for example
    <<< [2, 3, 5, 7]
    """
    # assertion
    lim = abs(int(lim))
    # special cases
    if lim < 7:
        if lim < 2:
            return []
        if lim < 3:
            return [2]
        if lim < 5:
            return [2, 3]
        return [2, 3, 5]
    # sieve
    n = (lim-1) // 30
    m = n + 1
    ba = bytearray
    prime1 = ba([1]) * m
    prime7 = ba([1]) * m
    prime11 = ba([1]) * m
    prime13 = ba([1]) * m
    prime17 = ba([1]) * m
    prime19 = ba([1]) * m
    prime23 = ba([1]) * m
    prime29 = ba([1]) * m
    prime1[0] = 0
    i = 0
    try:
        while True:
            if prime1[i]:
                p = 30*i + 1
                li = i * (p+1)
                prime1[li::p] = ba(1 + (n-li) // p)
                li += i * 6
                prime7[li::p] = ba(1 + (n-li) // p)
                li += i * 4
                prime11[li::p] = ba(1 + (n-li) // p)
                li += i * 2
                prime13[li::p] = ba(1 + (n-li) // p)
                li += i * 4
                prime17[li::p] = ba(1 + (n-li) // p)
                li += i * 2
                prime19[li::p] = ba(1 + (n-li) // p)
                li += i * 4
                prime23[li::p] = ba(1 + (n-li) // p)
                li += i * 6
                prime29[li::p] = ba(1 + (n-li) // p)
            if prime7[i]:
                p = 30*i + 7
                li = i * (p+7) + 1
                prime19[li::p] = ba(1 + (n-li) // p)
                li += i*4 + 1
                prime17[li::p] = ba(1 + (n-li) // p)
                li += i*2 + 1
                prime1[li::p] = ba(1 + (n-li) // p)
                li += i * 4
                prime29[li::p] = ba(1 + (n-li) // p)
                li += i*2 + 1
                prime13[li::p] = ba(1 + (n-li) // p)
                li += i*4 + 1
                prime11[li::p] = ba(1 + (n-li) // p)
                li += i*6 + 1
                prime23[li::p] = ba(1 + (n-li) // p)
                li += i*2 + 1
                prime7[li::p] = ba(1 + (n-li) // p)
            if prime11[i]:
                p = 30*i + 11
                li = i * (p+11) + 4
                prime1[li::p] = ba(1 + (n-li) // p)
                li += i * 2
                prime23[li::p] = ba(1 + (n-li) // p)
                li += i*4 + 2
                prime7[li::p] = ba(1 + (n-li) // p)
                li += i * 2
                prime29[li::p] = ba(1 + (n-li) // p)
                li += i*4 + 2
                prime13[li::p] = ba(1 + (n-li) // p)
                li += i*6 + 2
                prime19[li::p] = ba(1 + (n-li) // p)
                li += i*2 + 1
                prime11[li::p] = ba(1 + (n-li) // p)
                li += i*6 + 2
                prime17[li::p] = ba(1 + (n-li) // p)
            if prime13[i]:
                p = 30*i + 13
                li = i * (p+13) + 5
                prime19[li::p] = ba(1 + (n-li) // p)
                li += i*4 + 2
                prime11[li::p] = ba(1 + (n-li) // p)
                li += i*2 + 1
                prime7[li::p] = ba(1 + (n-li) // p)
                li += i*4 + 1
                prime29[li::p] = ba(1 + (n-li) // p)
                li += i*6 + 3
                prime17[li::p] = ba(1 + (n-li) // p)
                li += i*2 + 1
                prime13[li::p] = ba(1 + (n-li) // p)
                li += i*6 + 3
                prime1[li::p] = ba(1 + (n-li) // p)
                li += i*4 + 1
                prime23[li::p] = ba(1 + (n-li) // p)
            if prime17[i]:
                p = 30*i + 17
                li = i * (p+17) + 9
                prime19[li::p] = ba(1 + (n-li) // p)
                li += i*2 + 1
                prime23[li::p] = ba(1 + (n-li) // p)
                li += i*4 + 3
                prime1[li::p] = ba(1 + (n-li) // p)
                li += i*6 + 3
                prime13[li::p] = ba(1 + (n-li) // p)
                li += i*2 + 1
                prime17[li::p] = ba(1 + (n-li) // p)
                li += i*6 + 3
                prime29[li::p] = ba(1 + (n-li) // p)
                li += i*4 + 3
                prime7[li::p] = ba(1 + (n-li) // p)
                li += i*2 + 1
                prime11[li::p] = ba(1 + (n-li) // p)
            if prime19[i]:
                p = 30*i + 19
                li = i * (p+19) + 12
                prime1[li::p] = ba(1 + (n-li) // p)
                li += i*4 + 2
                prime17[li::p] = ba(1 + (n-li) // p)
                li += i*6 + 4
                prime11[li::p] = ba(1 + (n-li) // p)
                li += i*2 + 1
                prime19[li::p] = ba(1 + (n-li) // p)
                li += i*6 + 4
                prime13[li::p] = ba(1 + (n-li) // p)
                li += i*4 + 2
                prime29[li::p] = ba(1 + (n-li) // p)
                li += i*2 + 2
                prime7[li::p] = ba(1 + (n-li) // p)
                li += i*4 + 2
                prime23[li::p] = ba(1 + (n-li) // p)
            if prime23[i]:
                p = 30*i + 23
                li = i * (p+23) + 17
                prime19[li::p] = ba(1 + (n-li) // p)
                li += i*6 + 5
                prime7[li::p] = ba(1 + (n-li) // p)
                li += i*2 + 1
                prime23[li::p] = ba(1 + (n-li) // p)
                li += i*6 + 5
                prime11[li::p] = ba(1 + (n-li) // p)
                li += i*4 + 3
                prime13[li::p] = ba(1 + (n-li) // p)
                li += i*2 + 1
                prime29[li::p] = ba(1 + (n-li) // p)
                li += i*4 + 4
                prime1[li::p] = ba(1 + (n-li) // p)
                li += i*2 + 1
                prime17[li::p] = ba(1 + (n-li) // p)
            if prime29[i]:
                p = 30*i + 29
                li = i * (p+29) + 28
                prime1[li::p] = ba(1 + (n-li) // p)
                li += i*2 + 1
                prime29[li::p] = ba(1 + (n-li) // p)
                li += i*6 + 6
                prime23[li::p] = ba(1 + (n-li) // p)
                li += i*4 + 4
                prime19[li::p] = ba(1 + (n-li) // p)
                li += i*2 + 2
                prime17[li::p] = ba(1 + (n-li) // p)
                li += i*4 + 4
                prime13[li::p] = ba(1 + (n-li) // p)
                li += i*2 + 2
                prime11[li::p] = ba(1 + (n-li) // p)
                li += i*4 + 4
                prime7[li::p] = ba(1 + (n-li) // p)
            i += 1
    except ValueError:
        pass
    #  generation
    res = [2, 3, 5]
    ar = res.append
    ti = 0
    try:
        for i in range(n):
            if prime1[i]:
                ar(ti + 1)
            if prime7[i]:
                ar(ti + 7)
            if prime11[i]:
                ar(ti + 11)
            if prime13[i]:
                ar(ti + 13)
            if prime17[i]:
                ar(ti + 17)
            if prime19[i]:
                ar(ti + 19)
            if prime23[i]:
                ar(ti + 23)
            if prime29[i]:
                ar(ti + 29)
            ti += 30
    except IndexError:
        pass
    if prime1[n] and (30*n + 1) <= lim:
        ar(30*n + 1)
    if prime7[n] and (30*n + 7) <= lim:
        ar(30*n + 7)
    if prime11[n] and (30*n + 11) <= lim:
        ar(30*n + 11)
    if prime13[n] and (30*n + 13) <= lim:
        ar(30*n + 13)
    if prime17[n] and (30*n + 17) <= lim:
        ar(30*n + 17)
    if prime19[n] and (30*n + 19) <= lim:
        ar(30*n + 19)
    if prime23[n] and (30*n + 23) <= lim:
        ar(30*n + 23)
    if prime29[n] and (30*n + 29) <= lim:
        ar(30*n + 29)
    return res


# test : should take eta 1.1s

# if __name__ == "__main__":
#     import time
#     start = time.time()
#     print(len(primes(100_000_000)))
#     print(time.time() - start)
