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
    data = data.copy()
    steps = []

    def quick_sort(low, high):
        if low >= high:
            return

        pi_ind = high
        pivot = data[pi_ind]
        i = low - 1

        for j in range(low, high):
            if data[j] <= pivot:
                i += 1
                if i != j:
                    for k in range(j, i, -1):
                        steps.append((k - 1, k, pi_ind))
                        data[k - 1],data[k] = data[k], data[k - 1]

                        if k == pi_ind:
                            pi_ind = k - 1
                        elif k - 1 == pi_ind:
                            pi_ind = k

        pi = i+1
        if pi_ind > pi:
            for k in range(high, i + 1, -1):
                steps.append((k - 1, k, pi_ind))
                data[k - 1], data[k] = data[k], data[k - 1]
                if k == pi_ind:
                    pi_ind = k - 1
                elif k - 1 == pi_ind:
                    pi_ind = k

        quick_sort(low, i)
        quick_sort(i + 2, high)

    quick_sort(0, len(data) - 1)
    return steps


def select_sort_steps(data):
    data = data.copy()
    steps = []
    for i in range(len(data)):
        minim = (data[i], i)
        for j in range(i + 1, len(data)):
            if data[j] < minim[0]:
                minim = (data[j], j)
        for k in range(minim[1], i, -1):
            steps.append((k, k-1, i))
            data[k], data[k - 1] = data[k - 1], data[k]

    return steps


def comb_sort_steps(data):
    n = len(data)
    steps = []
    gap = n
    factor = 1.247
    sorting = True

    while sorting:
        gap = int(gap / factor)
        if gap <= 1:
            gap = 1
            sorting = False

        for i in range(0, n - gap):
            if data[i] > data[i + gap]:
                data[i], data[i + gap] = data[i + gap], data[i]
                steps.append((i, i + gap, gap))
                sorting = True
    return steps


def shell_sort_steps(data):
    data = data.copy()
    steps = []
    n = len(data)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = data[i]
            j = i
            while j >= gap and data[j - gap] > temp:
                data[j] = data[j - gap]
                steps.append((j, j - gap, gap))
                j -= gap
            data[j] = temp
        gap //= 2
    return steps


def shaker_sort_steps(data):
    data = data.copy()
    steps = []
    n = len(data)

    for i in range(n//2):
        for j in range(n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                steps.append((j, j + 1, 0))

        for j in range(n - i - 2, i, -1):
            if data[j] < data[j - 1]:
                data[j], data[j - 1] = data[j - 1], data[j]
                steps.append((j, j - 1, 1))
    return steps


def gnome_sort_steps(data):
    data = data.copy()
    steps = []
    n = len(data)
    i = 0
    while i < n - 1:
        if data[i] <= data[i + 1]:
            i += 1
        else:
            data[i], data[i + 1] = data[i + 1], data[i]
            steps.append((i, i + 1))
            if i != 0:
                i -= 1
    return steps