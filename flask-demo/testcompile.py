
def printa(i):
    print("lala" + str(i))


a = 5
code = '''
for i in range(0, a):
    printa(i)
a = 100
'''

cmpcode = compile(code, '', 'exec')

exec(cmpcode)

print(a)

