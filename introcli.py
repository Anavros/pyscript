
"""
Easy CLI creation using function introspection.
"""

# BUG: Arguments don't stay in order.

import inspect
import argparse
from sys import argv


class Registry:
    def __init__(self):
        self.functions = { }
        self.default = None

    def register(self, f):
        self.functions[f.__name__] = Function(f)

    def call(self, command, args):
        try:
            f = self.functions[command]
        except KeyError:
            raise SystemExit("Unknown command: {}.".format(command))
        p = generate_parser(f.parameters)
        a = p.parse_args(args)
        print(f.name, vars(a))
        f(**vars(a))

    def run(self):
        # requires that argv > 1
        if len(argv) <= 1:
            raise SystemExit("Missing command.")
        command, args = argv[1], argv[2:]
        self.call(command, args)

    def offer(self, to_decorate):
        self.register(to_decorate)

    def default(to_decorate):
        pass


class Function:
    def __init__(self, f):
        self.f = f
        self.name = f.__name__
        self.parameters = { }
        for n, p in inspect.signature(f).parameters.items():
            self.parameters[n] = p.annotation

    def __call__(self, *args, **kwargs):
        self.f(*args, **kwargs)


def generate_parser(parameters):
    p = argparse.ArgumentParser()
    for n, a in parameters.items():
        if a is inspect._empty:
            p.add_argument(n)
        else:
            p.add_argument(n, type=a)
    return p
