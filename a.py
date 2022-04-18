import random
import string

print(''.join(map(lambda x: x.replace('X', random.choice(string.ascii_letters)), 'X1X1X1')))
