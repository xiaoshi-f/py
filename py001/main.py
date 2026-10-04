def count_aeiou(s):
    num=0
    for i in s:
        if i in "aeiouAEIOU":
            num += 1
    return num
print(count_aeiou("nihaowoshishijianing"))