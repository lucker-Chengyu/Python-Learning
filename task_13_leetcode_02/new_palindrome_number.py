class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        if x < 0:
            return False
        reversed_num = 0
        original = x
        while x > 0:
            yushu = x % 10
            reversed_num = reversed_num * 10 + yushu
            x = x // 10
        return reversed_num == original
