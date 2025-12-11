def bubble_sort_step(lst: list, i):
    if lst[i][1] > lst[i+1][1]:
            lst[i], lst[i+1] = (lst[i][0], lst[i+1][1]), (lst[i+1][0], lst[i][1])
    return lst

print(bubble_sort_step([(1, 2), (2, 1), (3, 3)], 0))