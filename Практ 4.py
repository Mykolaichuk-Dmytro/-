def remove_duplicates(input_list):
    return list(set(input_list))

def sort_list(unique_list):

    numbers = [x for x in unique_list if isinstance(x, (int, float))]
    strings = [x for x in unique_list if isinstance(x, str)]

    numbers.sort()

    strings.sort()

    return numbers + strings

input_list = [1, 2, 3, 4, 5, 6, 3, 4, 5, 7, 6, 5, 4, 3, 4, 5, 4, 3, 'Привіт', 'анаконда']

unique_list = remove_duplicates(input_list)

sorted_list = sort_list(unique_list)

print(sorted_list)
