def f(x):
    return x < 5

def find_boundary(N):
    low, high = 1, N

    while low < high:
        mid = (low + high) // 2
        if f(mid):
            low = mid + 1
        else:
            high = mid

    return low