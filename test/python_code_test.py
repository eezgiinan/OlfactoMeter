import enum
import threading

print([s for s in range(1, 10+1)])

odors = ['mint', 'almond']

for i, odor in enumerate(odors, 1):
    print(i, '. ' + odor, sep='', end='\n')


print([i+2 for i, x in enumerate(odors)])

odors.index(odor)


for odor in odors:
    print(odor)


class Odors(enum.Enum):
    """
    Different odors that the user can use
    """
    Odor_1 = 'Mint'
    Odor_2 = 'Almond'


print(Odors.Odor_1)



FLAG = 'False'


def hello():
    print("hello, world")


t = threading.Timer(1, hello)
t.start()  # after 30 seconds, "hello, world" will be printed

print(FLAG)


a = 1


def changing_a(a):
    a = 2
    return a

