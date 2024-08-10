import random as rd
ch = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890@#$&"
password = ""
user = int(input("enter the length of the password: "))

r1 = ch[rd.randint(52,62)]
r2 = ch[rd.randint(62,65)]
r3 = rd.randint(0,user)
r4 = rd.randint(0,user)

for i in range (0,user):
    if i == r3:
        password = password + r1
        continue
    if i == r4:
        password = password + r2
        continue
    random = rd.randint(0,len(ch))
    password = password + ch[random]

print("your password is: ", password)
#but we require at least 1 number and alleast 1 Special character

