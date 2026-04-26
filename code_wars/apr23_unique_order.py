def unique_in_order(sequence):
   result=[]
   if len(sequence)>0:
       result.append(sequence[0])
       prev = sequence[0]
       for word in sequence:
           if word != prev:
               result.append(word)
               prev = word
   return list(result)

def findMaxConsecutiveOnes(nums) -> int:
     n = int("".join(map(str, nums)), 2)
     count = 0
     while n > 0 :
         n = n & (n << 1)
         count += 1
     return count

def findMaxConsecutiveOnes1(nums) -> int:
    max_count = 0
    curr = 0

    for x in nums:
        if x == 1:
            curr += 1
            max_count = max(max_count, curr)
        else:
            curr = 0

    return max_count

def high1(x):
    sum = 0
    for letter in x:
        code = ord(letter)
        if code >= 97 and code <= 122:
            sum +=ord(letter)-96
        if code >= 65 and code <= 90:
            sum +=ord(letter)-64
    return sum
def high(x):
    words = x.split()

    return max(words,key = high1)

#print(unique_in_order('aabaaccdddddeddde'))
#print(findMaxConsecutiveOnes([1,1,0,1,1,1,0,1,0,11]))
print(high("aa b"))