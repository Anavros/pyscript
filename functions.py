
import introcli

r = introcli.Registry()

#@r.default # nyi
@r.offer
def a():
    print('a')


@r.offer
def b(x):
    print('b')


@r.offer
def c(x, y:int):
    print('c')


@r.offer
def repeat(string, n:int):
    print(string*n)


if __name__ == '__main__':
    r.run()
