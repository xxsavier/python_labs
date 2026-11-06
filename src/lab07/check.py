import random
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort
from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast


def check_sorting(func, trials=100) -> int:
    """Проверка работы сортировок

    Args:
        func (function): функция - выбранный способ сортировки
        trials (int): количество проверок. Значение по умолчанию - 100.

    Returns:
        int: количество пройденных тестов
    """
    for _ in range(trials):
        len_list = random.randint(0,50)
        try_list = [random.randint(-100, 100) for _ in range(len_list)]
        not_srt_lst = list(try_list)
        srt_lst = func(try_list)
        assert srt_lst == sorted(not_srt_lst), f"{func.__name__} ошиблась на {try_list}: {srt_lst}"
        assert try_list == not_srt_lst, f"{func.__name__} изменила исходный список"
    return trials


def check_search() -> int:
    """Проверка работы поиска

    Returns:
        int: количество пройденных тестов
    """
    trials = 100
    for _ in range(trials):
        nums = [random.randint(-50, 50) for _ in range(random.randint(0, 42))]
        target = random.randint(-60, 60)
        func_result = linear_search(nums, target)
        try:
            index_result = nums.index(target)
        except ValueError:
            index_result = -1
        assert func_result == index_result, f"linear_search ошибся при поиске {target} в {nums}"
        
        srt_nums = sorted(nums)
        bin_result = binary_search(srt_nums, target)
        try:
            index_result = srt_nums.index(target)
        except ValueError:
            index_result = -1
        assert bin_result == index_result, f"binary_search ошибся при поиске {target} в {srt_nums}"
    return trials


def check_two_sum(trials=100) -> int:
    """Проверка работы поиска пары по сумме

    Args:
        trials (int): количество проверок. Значение по умолчанию - 100.

    Returns:
        int: количество пройденных тестов
    """
    for _ in range(trials):
        nums = [random.randint(-50, 50) for _ in range(random.randint(2, 42))]
        target = random.randint(-101, 101)
        brute_result = two_sum_brute(nums, target)
        fast_result = two_sum_fast(nums, target)
        if brute_result is None:
            assert fast_result is None, f"Результат two_sum_fast и two_sum_brute не совпадают. two_sum_fast нашел пару, two_sum_brute - нет"
        else:
            bi, bj = brute_result
            assert nums[bi] + nums[bj] == target, f"two_sum_brute нашел неверную пару"
            assert fast_result is not None, f"Результат two_sum_fast и two_sum_brute не совпадают. two_sum_brute нашел пару, two_sum_fast - нет"
            fi, fj = fast_result
            assert nums[fi] + nums[fj] == target, f"two_sum_brute верно нашел пару, two_sum_fast - нет"
    return trials
        
if __name__ == "__main__":
    random.seed(42)
    attempts = 0
    for func in (bubble_sort, insertion_sort, selection_sort):
        attempts += check_sorting(func)
    attempts += check_search()
    attempts += check_two_sum()
    print(f"OK: {attempts} проверок")
        
            