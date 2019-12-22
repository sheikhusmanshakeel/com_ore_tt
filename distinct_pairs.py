from typing import List


class Solution:
    def twoSum_bf(self, nums: List[int], target: int) -> int:
        size_of_nums = len(nums)
        ans_set = set()
        for i, n in enumerate(nums):
            res = target - n
            for j in range(i + 1, size_of_nums):
                if nums[j] == res:
                    min_val = min(n, nums[j])
                    ans_set.add((min_val, target - min_val))
                    break

        return len(ans_set)

    def twoSum_hash(self, nums: List[int], target: int) -> int:
        ans_set = set()
        res_hash = {}
        for n in nums:
            res_hash[target - n] = n
        first_half_seen = False

        for num in nums:
            if num in res_hash:
                if num == (target - num):
                    if first_half_seen:
                        # second half seen as well
                        ans_set.add((num, num))
                        first_half_seen = False
                    else:
                        first_half_seen = True
                        continue
                min_val = min(target - num, num)
                ans_set.add((min_val, target - min_val))
        return len(ans_set)


data1 = [1, 3, 46, 1, 3, 9, 40, 7, 7]
target1 = 47
data2 = [1, 9, 8, 25, 15, 19, 45, 12, 16, 18, 2, 3, 5]
target2 = 10
data3 = [7, 6, 12, 3, 9, 3, 5, 1]
target3 = 24

assert (Solution().twoSum_hash(data2, target2)) == 2  # 9,1 and 8,2
assert (Solution().twoSum_hash(data1, target1)) == 2  # 46,1 and 40,7
assert (Solution().twoSum_hash(data3, target3)) == 0
