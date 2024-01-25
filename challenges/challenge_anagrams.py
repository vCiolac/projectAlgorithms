def is_anagram(first_string, second_string):
    f_sorted = merge_sort(first_string.lower())
    s_sorted = merge_sort(second_string.lower())

    f_join = ''.join(f_sorted)
    s_join = ''.join(s_sorted)

    if not first_string or not second_string:
        if not first_string:
            return ('', s_join, False)
        else:
            return (f_join, '', False)

    return (f_join, s_join, f_sorted == s_sorted)


def merge_sort(value):
    if len(value) <= 1:
        return value
    mid = len(value) // 2
    left = merge_sort(value[:mid])
    right = merge_sort(value[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
