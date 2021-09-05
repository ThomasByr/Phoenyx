__all__ = ["prime_factors"]


def prime_factors(x: int) -> list[str]:
    """
    a list of positive primes integers

    Parameters
    ----------
        x : int
            number to check

    Returns
    -------
        list[str] : primes
    """
    a, res = 0, []
    while x % 2 == 0:
        x //= 2
        a += 1
    if a >= 2:
        res.append('2^' + str(a))
    if a == 1:
        res.append('2')
    b = 3
    while b * b <= x:
        a = 0
        while x % b == 0:
            x //= b
            a += 1
        if a >= 2:
            res.append(str(b) + '^' + str(a))
        if a == 1:
            res.append(str(b))
        b += 2
    if x != 1:
        res.append(str(x))
    return res


# if __name__ == '__main__':
#     number = int(eval(input("n = ")))
#     print(prime_factors(number))
