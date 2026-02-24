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
