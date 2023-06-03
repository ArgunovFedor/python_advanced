from typing import Union, List

Number = Union[int, float, complex]


def find_insert_position(array: List[Number], number: Number) -> int:
    # пустой массив
    if len(array) == 0:
        return 1
    # X нужно вставить первым элементом.
    if array[0] > number:
        return 1
    # X нужно вставить последним элементом.
    if array[-1] < number:
        return len(array)
    index = 0
    for i in array:
        if i <= number:
            index += 1
        else:
            break
    return index


if __name__ == '__main__':
    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    insert_position: int = find_insert_position(A, x)
    A.insert(insert_position, x)
    assert insert_position == 5
    assert A == sorted(A)
