#!/usr/bin/env python3

import itertools


def split_iter(iterable, condition):
    """
    Split an iterable in two, based on callable condition.

    condition must be a callable that accepts an element
    of the sequence, and returns a boolean. The `split_iter`
    function returns two iterables: First one is for the items
    that are avaluated by `condition` as `True`, second one is
    an iterable for the rest.

    Example:

        >>> pares, impares = split_iter(range(10), lambda x: x % 2 == 0)
        >>> assert list(pares) == [0, 2, 4, 6, 8]
        >>> assert list(impares) == [1, 3, 5, 7, 9]
        >>> lt4, gte4 = split_iter(range(10), lambda x: x < 4)
        >>> assert list(lt4) == [0, 1, 2, 3]
        >>> assert list(gte4) == [4, 5, 6, 7, 8, 9]
    """
    a, b = itertools.tee(iterable, 2)
    positive_iter = (_ for _ in a if condition(_))
    negative_iter = (_ for _ in b if not condition(_))
    return positive_iter, negative_iter
