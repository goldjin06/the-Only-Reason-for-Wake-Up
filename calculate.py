import random

num1 = random.randint(1, 20) # 정수 하나 랜덤
num2 = random.randint(1, 20) # 정수 하나 랜덤
c = random.randint(1, 3) # 연산자 랜덤

def random_exclude(range_start, range_end, excludes):
    r = random.randint(range_start, range_end)
    if r in excludes:
        return random_exclude(range_start, range_end, excludes)
    return r

def operator(number):
    if number == 1:
        return('+')
    elif number == 2:
        return('*')
    elif number == 3:
        return('-')

if c == 1:
    cal = num1 + num2 # cal -> 계산결과
elif c == 2:
    cal = num1 * num2
elif c == 3:
    cal = num1 - num2

answer1 = random_exclude(cal-30, cal+30, [cal])
answer2 = random_exclude(cal-30, cal+30, [cal, answer1])
answerlist = [answer1, answer2, cal]
random.shuffle(answerlist)

answer = input('''{0} {1} {2} = ?
(1){3} (2){4} (3){5}'''.format(num1, operator(c), num2, answerlist[0], answerlist[1], answerlist[2]))

if answerlist[int(answer)-1] == cal:
    print('정답')
    quit()
else:
    print('오답')