class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        if x < 0:
            return False
        digits = [int(d) for d in str(x)]
        return digits == digits[::-1]