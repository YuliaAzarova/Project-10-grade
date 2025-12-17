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