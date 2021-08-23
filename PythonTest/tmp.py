import os,sys
# import listNode

class ListNode():
    def __init__(self, val,lst):
        if isinstance(val,int):
            self.val = val
            self.next = None

        elif isinstance(val,list):
            self.val = val[0]
            self.next = None
            cur = self
            for i in val[1:]:
                cur.next = ListNode(i)
                cur = cur.next

    def gatherAttrs(self):
        return ", ".join("{}: {}".format(k, getattr(self, k)) for k in self.__dict__.keys())

    def __str__(self):
        return self.__class__.__name__+" {"+"{}".format(self.gatherAttrs())+"}"

# 给你一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？请你找出所有和为 0 且不重复的三元组。
# 链接：https://leetcode-cn.com/problems/3sum
class Solution0:
    def threeSum(self, lst):
        res = []
        resl = []
        tmplst = lst.copy()
        print ("list: ",tmplst)
        for i in range(len(tmplst)-1):
            for j in range(len(tmplst)-1,i+1,-1):
                count = 0 - ( tmplst[i] + tmplst[j])
                if count in tmplst[i+1:j]:
                    res.append(list(sorted([tmplst[i],tmplst[j],count])))
        for ele in res:
            if ele in resl:
                continue
            else:
                resl.append(ele)
        print (resl)


# 给定一个包括 n 个整数的数组 nums 和 一个目标值 target。找出 nums 中的三个整数，使得它们的和与 target 最接近。返回这三个数的和。假定每组输入只存在唯一答案。
# 输入：nums = [-1,2,1,-4], target = 1
# 输出：2
# 解释：与target最接近的和是 2 (-1 + 2 + 1 = 2)
# 链接：https://leetcode-cn.com/problems/3sum-closest
class Solution1:
    def threeSumClosest(self, lst,target):
        print (lst)
        res = {}
        sumres = 0
        for i in range(len(lst)-1):
            for j in range(len(lst)-1,i+1,-1):
                sum0 = lst[i] + lst[j]
                for ele in lst[i+1:j]:
                    sum = sum0 + ele
                    res[abs(sum-target)] = sum
        print(res)
        t = 0
        m = sorted(res.keys())
        print (m)
        print (sorted(res.values()))
        print (res[m[0]])

# 给定一个仅包含数字 2-9 的字符串，返回所有它能表示的字母组合。答案可以按 任意顺序 返回。
# 给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。
# 输入：digits = "23"
# 输出：["ad","ae","af","bd","be","bf","cd","ce","cf"]
# 链接：https://leetcode-cn.com/problems/letter-combinations-of-a-phone-number
class Solution2:
    def __init__(self):
        self.checkDict = {"2":["a","b","c"],"3":["d","e","f"],"4":["g","h","i"],"5":["j","k","l"],"6":["m","n","o"],
                 "7":["p","q","r","s"],"8":["t","u","v"],"9":["w","x","y","z"]}

    def parse(self,lsta ,lstb):
        res = []
        if lsta == [] :
            res = lstb
        if lstb == [] :
            res = lsta
        for ea in lsta:
            for eb in lstb:
                res.append(ea+eb)
        return res

    def letterCombinations(self, digits):
        res = []
        tmp = []
        if len(digits) == 0:
            return res
        elif len(digits) == 1:
            res = self.checkDict.get(digits,[])
            return res
        for d in digits:
            tmp = self.parse(tmp,self.checkDict.get(d,[]))
        return (tmp)

# 给定一个包含 n 个整数的数组 nums 和一个目标值 target，判断 nums 中是否存在四个元素 a，b，c 和 d ，使得 a + b + c + d 的值与 target 相等？找出所有满足条件且不重复的四元组。
# 链接：https://leetcode-cn.com/problems/4sum
class Solution:

    # def parse(self,lst,target,i,j):
    #     for i in lst[i:j]:
    #         for j in range(len(nums)-1,i+1,-1):
    #             sum = nums[i] + nums[j]

    def fourSum(self, nums, target):
        if len(nums) < 4 :
            return "error!"
        for i in range(len(nums)-2):
            for j in range(len(nums)-1,i+1,-1):
                sum = nums[i] + nums[j]
                aim = target - sum

class Solution4():
    def sumtwo(self,a,b):
        if a == 0: return b
        if b == 0: return a
        m = len(a) if len(a) > len(b) else len(b)
        print (m)
        jw = 0
        ls = []
        for ele in range(m-len(a)):
            a = "0" + a
        for ele in range(m-len(b)):
            b = "0" + b
        print (a,b)
        for i in range(m,0,-1):
            if i >= len(a):
                x = 0
            else:
                x = a[i]
            if i >= len(b):
                y = 0
            else:
                y = b[i]
            # print (x,y,jw)
            z = int(x) + int(y) + jw
            sum = z%10
            jw = z//10
            print (x,y,sum,jw)
            ls.append(str(sum))
        print (jw)
        ls.append(jw)
        print(ls)
        print ("".join(ls.reverse()),int(a)+ int(b))


class Solution5():
    def threeDigit(self):
        a = []
        for i in range(1,10):
            for j in range(10):
                for z in range(10):
                   a.append(i*100+j*10+z)
        print (a,len(a))

    def repeat(self):
        a=[1,1,1,3,3,4,3,2,4,2]
        b = len(a)
        a.sort()
        print(list(set(a)),b)
        if ( len(list(set(a))) == b ):
            print ("false")
        else:
            print("true")

    def longer(self):
        list = ["asddddsd","asdwwww","asdp"]
        s = list[0]
        sam = ""
        i=1
        while i < len(list):
            for j in range(len(s)):
                print(s[j])
                if j in list[i][j]:
                    sam += s[j]
                else:
                    continue
            i+=1
        print(sam)


if __name__=="__main__":
    he = Solution5()
    he.longer()
    # List = [-1,0,1,2,4,-4,-1,-2,3,7,6,-3]
    # print(he.sumtwo("1234","1234567"))
