def bubble_sort_steps(data):
    data = data.copy()
    steps = []
    n = len(data)

    for i in range(n):
        for j in range(n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                steps.append((j, j + 1))

    return steps


def insert_sort_steps(data):
    data = data.copy()
    steps = []
    n = len(data)
    for i in range(n):
        for j in range(i, 0, -1):
            if data[j] < data[j - 1]:
                data[j], data[j - 1] = data[j - 1], data[j]
                steps.append((j - 1, j))

    return steps


def merge_sort_steps(data):
    data = data.copy()
    steps = []

    def merge(left, mid, right):
        i = left
        j = mid

        while i < j and j < right:
            if data[i] <= data[j]:
                i += 1
            else:
                k = j
                while k > i:
                    data[k], data[k - 1] = data[k - 1], data[k]
                    steps.append((k - 1, k, left, right))
                    k -= 1
                i += 1
                j += 1
                mid += 1

    def div(left, right):
        if right - left <= 1:
            return
        mid = (left + right) // 2
        div(left, mid)
        div(mid, right)
        merge(left, mid, right)

    div(0, len(data))
    return steps


def quick_sort_steps(data):
    arr = data.copy()
    steps = []

    def quick_sort(low, high):
        if low >= high:
            return

        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                if i != j:

                    for k in range(j, i, -1):
                        steps.append((k - 1, k))
                        arr[k - 1], arr[k] = arr[k], arr[k - 1]

        if i + 1 != high:
            for k in range(high, i + 1, -1):
                steps.append((k - 1, k))
                arr[k - 1], arr[k] = arr[k], arr[k - 1]

        pi = i + 1
        quick_sort(low, pi - 1)
        quick_sort(pi + 1, high)

    quick_sort(0, len(arr) - 1)
    return steps