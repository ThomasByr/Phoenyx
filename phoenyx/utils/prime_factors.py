__all__ = ["prime_factors"]

from typing import Union


def prime_factors(
    x: int,
    dtype: type[Union[list, dict]] = dict,
) -> Union[list[int], dict[int, int]]:
    """
    a list of positive primes integers

    Parameters
    ----------
        x : int
            number to check
        dtype : type
            type of returned data

    Returns
    -------
        list[int] | dict[int, int] : either a list of counted primes factors or a dict of primes factors and their counts
    """
    a = 0
    d: dict[int, int] = {}
    while x % 2 == 0:
        x //= 2
        a += 1
    if a >= 1:
        d[2] = a
    b = 3
    while b * b <= x:
        a = 0
        while x % b == 0:
            x //= b
            a += 1
        if a >= 1:
            d[b] = a
        b += 2
    if x != 1:
        d[x] = 1

    if dtype == dict:
        return d
    else:
        return sorted([k for k, v in d.items() for _ in range(v)])


# if __name__ == '__main__':
#     number = int(eval(input("n = ")))
#     print(prime_factors(number, dtype=dict))
