def findPalindrome(input):
# 	“”
# 	“babdfjkecalilac”
# 	[d,r,b,a,c] ab”
# “drbacab”
# ””
    input = input.lower()
	# iterate through string, checking for the first duplicate

    pot_substrs = []
    seen_dict = {}
    for c_idx in range(len(input)):
        if input[c_idx] not in seen_dict:
			# original idx
            seen_dict[input[c_idx]] = c_idx
        else:
            pot_substrs.append(input[seen_dict[input[c_idx]] : c_idx+1])
    print(pot_substrs)
 
    pot_palindromes = []
    for substr in pot_substrs:
        hash_dict = {}
        for c in substr:
            if c not in hash_dict:
                hash_dict [c] = 1
            else:
                hash_dict[c] += 1
			
        mid = len(substr) // 2
        values = list(hash_dict.values())
        palindrome = True
        for c, v in zip(substr[:mid], values):
            if v < 2:
                palindrome = False
                break
        if palindrome:
            pot_palindromes.append(substr)
            
    print(pot_palindromes)
    greater_len_palind = [float('-inf'), ""] 
    for palind in pot_palindromes:
        if len(palind) > greater_len_palind[0]:
            greater_len_palind = [len(palind), palind]

    return greater_len_palind[1]

def removeDuplicates(nums):
    current_num = None
    num_duplicates = 0
    num_idx = 0
    # k = 0
    while nums[num_idx] <= nums[num_idx+1]:
        if nums[num_idx] is not current_num:
            current_num = nums[num_idx]
            num_idx += 1 
        else:
            print(nums)
            print(nums[num_idx])
            num_duplicates += 1
            to_append = nums.pop(num_idx)
            nums.append(to_append)
            
    # O(1) edge case check
    print(num_idx)
    if nums[num_idx] == nums[num_idx - 1]:
        num_duplicates += 1
    k = len(nums) - num_duplicates
    return k, nums

def jumpGame(nums, num_jumps=0):
    """
    My Solution
    """
    # [2,3,1,1,4]
    distance = len(nums) - 1
    if len(nums) ==  0 or len(nums) == 1:
        return 0
    num_jumps += 1
    # base case
    if distance - (nums[0]) <= 0:
        return num_jumps
    # recursive case
    num_jumps_list = []
    for num in range(1, nums[0]+1):
        # print(jumpGame(nums[num:], num_jumps))
        num_jumps_list.append(jumpGame(nums[num:], num_jumps))
    return min(num_jumps_list)

# ALTERNATE SOLUTION TO JUMP GAME
def jumpGameAlt(nums, i=0):
    """
    Solution from TA
    """
    if i >= len(nums):
        return 0
    jump_options = nums[i]
    min_jump_num = float('inf')
    for j in range(1, jump_options + 1):
        min_jump_num = min(min_jump_num, 1 + jumpGameAlt(nums, i + j))
        
    # solution off by 1, need to create the recursive function on the inside, then substract 1 after calling 
    # that recursive function
    return min_jump_num


def mixtape(songs, target_duration):
    # base cases
    if target_duration == 0:
        return set()
    
    if target_duration < 0 or not songs:
        return None
    
    song = list(songs.keys())[0]
    # first / rest recursive breakdown
    songs_rest = {k: v for k,v in songs.items() if k != song}
    duration = songs[song]
    
    # assume first is part of solution, if returns None, backtrack
    recursive_result1 = mixtape(songs_rest, target_duration - duration)
    if recursive_result1 is not None:
        return {song} | recursive_result1
    
    # checking if solution exists without first one
    recursive_result2 = mixtape(songs_rest, target_duration)
    if recursive_result2 is not None:
        return recursive_result2
    
    # if not, no solution exists
    return None
    
    



if __name__ == '__main__':
    # print(findPalindrome("dcbabjkfblgaflfag"))
    nums = [0,0,1,1,1,2,2,3,3,4]
    nums2 = [1,1,2]
    nums3 = [1,1,4,4,4,4,8,9,10,10,223,313,313,313,5000,5000]
    # print(removeDuplicates(nums3))
    nums4 = [2,1,2,1,4]
    nums5 = [1,1,1,1,1,1]
    # print(jumpGame(nums4))
    # print(jumpGameAlt(nums4))
    songs = {'A': 5, 'B': 10, 'C': 6, 'D': 2}
    print(mixtape(songs, 1000))