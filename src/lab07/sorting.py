def bubble_sort(nums) -> list:
    for i in range(len(nums)):
        for j in range(len(nums) - i - 1):
            if nums[j] > nums[j+1]:
                nums[j], nums[j+1] = nums[j+1], nums[j]
    return nums


def insertion_sort(nums) -> list:
    for insert_index in range(1, len(nums)):
        insert_element  = nums[insert_index]
        left_coast = insert_index - 1
        while left_coast >= 0 and nums[left_coast] > insert_element:
            nums[left_coast + 1] = nums[left_coast]
            left_coast -= 1
        nums[left_coast + 1] = insert_element
    return nums
    



#def selection_sort(nums) -> list:


print(bubble_sort([7,4,55,2,1,0,9,55,2]))
print(insertion_sort([7,4,55,2,1,0,9,55,2]))