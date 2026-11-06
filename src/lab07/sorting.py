def bubble_sort(nums: list[int]) -> list[int]:
    """Сортировка пузырьком

    Args:
        nums (list): неотсортированный список чисел

    Returns:
        list: отсортированный список nums
    """    
    nums = list(nums)
    for i in range(len(nums)):
        thats_all = True
        for j in range(len(nums) - i - 1):
            if nums[j] > nums[j+1]:
                nums[j], nums[j+1] = nums[j+1], nums[j]
                thats_all = False
        if thats_all:
            return nums
    return nums


def insertion_sort(nums: list[int]) -> list[int]:
    """Сортировка вставками

    Args:
        nums (list): неотсортированный список чисел

    Returns:
        list: отсортированный список nums
    """
    nums = list(nums)
    for insert_index in range(1, len(nums)):
        insert_element  = nums[insert_index]
        left_border = insert_index - 1
        while left_border >= 0 and nums[left_border] > insert_element:
            nums[left_border + 1] = nums[left_border]
            left_border -= 1
        nums[left_border + 1] = insert_element
    return nums
    
def selection_sort(nums: list[int]) -> list[int]:
    """Сортировка выбором

    Args:
        nums (list): неотсортированный список чисел

    Returns:
        list: отсортированный список nums
    """
    nums = list(nums)
    for index in range(len(nums)):
        min_el = index
        for el in range(index + 1, len(nums)):
            if nums[el] < nums[min_el]:
                min_el = el
        nums[index], nums[min_el] = nums[min_el], nums[index]
    return nums
