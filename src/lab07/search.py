def linear_search(nums, x) -> int:
    """Линейный поиск

    Args:
        nums (list): список чисел
        x (int): искомый элемент

    Returns:
        int: индекс искомого элемента
    """
    for number, element in enumerate(nums):
        if element == x:
            return number
    return -1


def binary_search(sorted_nums, x) -> int:
    """Бинарный поиск

    Args:
        sorted_nums (list): отсортированный список чисел
        x (int): искомый элемент

    Returns:
        int: индекс искомого элемента
    """
    
    lo, hi = 0, len(sorted_nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_nums[mid] == x:
            return mid
        elif x > sorted_nums[mid]:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def two_sum_brute(nums, target) -> tuple[int, int] | None:
    """Two sum методом грубой силы

    Args:
        nums (list): список чисел
        target (int): необходимая сумма

    Returns:
        tuple[int, int]: индексы i и j подходящих чисел (i < j)
        None: в списке нет подходящей пары чисел
    """
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


def two_sum_fast(nums, target) -> tuple[int, int] | None:
    """Two sum через словари

    Args:
        nums (list): список чисел
        target (int): необходимая сумма

    Returns:
        tuple[int, int]: индексы i и j подходящих чисел (i < j)
        None: в списке нет подходящей пары чисел
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None