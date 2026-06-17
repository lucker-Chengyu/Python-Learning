def count_character(s, char):
    if s == "":
        return 0
    if s[0] == char:
        return 1 + count_character(s[1:], char)
    return count_character(s[1:], char)
a = count_character("banana", "a")
print(a)
