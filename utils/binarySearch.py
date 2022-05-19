def modified_binary_search(arr: [], n: int):
    """
    a simple algorithm which return the next smalled number given an integer and an array
    :param arr: array of integer
    :param n: the target integer
    :return: next smallest integer in given array
    """
    try:
        m = len(arr) // 2
        if arr[m] <= n and arr[m + 1] > n:
            return arr[m]
        elif arr[m] > n and arr[m - 1] > n:
            return modified_binary_search(arr[:m], n)
        else:
            return modified_binary_search(arr[m:], n)
    except Exception:
        return -1


array = [3, 4, 6, 9, 10, 12, 14, 15, 17, 19, 21]
number = 13
print(modified_binary_search(array, number))
