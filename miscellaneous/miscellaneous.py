from collections import deque


class Miscellaneous:
    @staticmethod
    def list_rotate(array, n):
        dequed_array = deque(array)
        dequed_array.rotate(n)
        return list(dequed_array)

    @staticmethod
    def foldr(f, acc, xs):
        for x in xs:
            acc = f(x, acc)
        return acc
