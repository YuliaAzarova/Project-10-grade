def bubble_sort_steps(data):
    data = data.copy()
    steps = []
    n = len(data)
    for i in range(n - 1, 0, -1):
        for j in range(i):
            if data[j][1] > data[j + 1][1]:
                data[j], data[j + 1] = (data[j][0], data[j + 1][1]), (data[j+1][0], data[j][1])
            steps.append(data.copy())
    return steps


def insert_sort_steps(data):
    data = data.copy()
    steps = []
    n = len(data)
    for i in range(n):
        for j in range(i, 0, -1):
            if data[j][1] < data[j - 1][1]:
                data[j], data[j - 1] = (data[j][0], data[j - 1][1]), (data[j - 1][0], data[j][1])
            steps.append(data.copy())
    return steps

def merge_sort_steps(data):
    data = data.copy()
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left_half = data[:mid]
    right_half = data[mid:]

    left_half = merge_sort_steps(left_half)
    right_half = merge_sort_steps(right_half)

    return merge(left_half, right_half)

def merge(left, right):
    left = left.copy()
    right = right.copy()
    steps = []
    merged = []

    while left and right:
        if left[0] < right[0]:
            merged.append(left.pop(0))
        else:
            merged.append(right.pop(0))
        steps.append(merged +left + right)

    merged += left or right
    if len(steps) == 0 or steps[-1] != merged:
        steps.append(merged.copy())
    
    return steps