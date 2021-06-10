def convert(strT):
    hour = int(strT[-4:-2])
    min = int(strT[-2:])
    date = int(strT[-8:-4])
    return hour*60+min
    
def sub(str1, str2):
    t1 = convert(str1)
    t2 = convert(str2)
    return t2-t1

convert('202001010600')
ans = sub('202001010600','202001010840')
print(ans)