from SocketServer import TCPServer, BaseRequestHandler, ForkingMixIn
from random import randint, choice, seed
from struct import unpack
from math import floor, trunc, ceil
import operator
import socket
import os
import inflect

# some initialization
ie = inflect.engine()
socket.setdefaulttimeout(5)

# globals
FLAG = "RC3-2017{i-am-the-0ne-wh0-kn0ckz}"

ops = { "+":  operator.add,
        "-":  operator.sub,
        "**": operator.pow,
        "&":  operator.and_,
        "/":  operator.truediv,
        "*":  operator.mul,
        "^":  operator.xor,
        "|":  operator.or_,
        "%":  operator.mod,
        ">>": operator.rshift,
        "<<": operator.lshift }

rounds = [ floor, ceil, trunc, round ]

# makes up a random equation to generate a port number
# the hope is that they'll just eval it...
def randomMaths():
    prob = ""
    for i in range(randint(2, 6)):
        if not prob:
            lhs = randint(-255, 255)
            prob = str(lhs)
        rhs = randint(-255, 255)
        op = choice(list(ops.keys()))
        try:
            lhs = ops.get(op)(lhs, rhs)
        except:
            continue
        else:
            prob += " {} {})".format(op, rhs)
            prob = "(" + prob
    r = choice(rounds)
    prob = "{}{} % 65535".format(r.__name__, prob)
    lhs = r(lhs) % 65535
    return prob, lhs


# returns words for the port number. cool!
def randomWords():
    ret = randint(1024, 65535)
    return ie.number_to_words(ret), ret


# just returns a number for the port
def randomPort():
    ret = randint(1024, 65535)
    return ret, ret


funcs = [ randomMaths, randomWords, randomPort ]


# binds to the specified port and makes up a new one
# also sends each letter of the flag
def bindAndSend(req, l, port, trick=False):
    while 1:
        try:
            p, a = choice(funcs)()
            if a < 1023:
                continue
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', int(port)))
            s.listen(1)
            break
        except:
            pass
    try:
        c, _ = s.accept()
        c.send(l + '\n')
        if not trick:
            c.send(str(p) + '\n')
        else:
            # troll city
            c.send("{}(__import__('os').system('echo probably dont eval arbitrary code from the internet k? -wumb0 > SPECIAL_WARNING_MESSAGE.txt'))\n".format(choice(rounds).__name__))
        c.close()
        return True, a
    except socket.timeout:
        pass
    finally:
        s.close()
    return False, 0


# sends the whole flag each to different ports
class KnockerHandler(BaseRequestHandler):
    def handle(self):
        seed(unpack(">L", os.urandom(4))[0])
        self.request.settimeout(60)
        self.request.send("Welcome to the third annual short python challenge.\n")
        self.request.send("You'll get one letter at a time and a new problem to solve each time. Left vague on purpose. You'll figure it out. Hit enter when you're ready...")
        try:
            self.request.recv(1024)
        except socket.timeout:
            self.request.send("Bye.")
        self.request.settimeout(5)

        # make up the first port and send the first letter & challenge
        while 1:
            try:
                p, a = choice(funcs)()
                if a < 1023:
                    continue
                break
            except:
                pass
        self.request.send(FLAG[0] + '\n')
        self.request.send(str(p) + '\n')

        # send the rest of the flag, creating a new challenge every time
        for i in FLAG[1:-1]:
            res, a = bindAndSend(self.request, i, a)
            if not res:
                break

        # if not res then don't send the last letter, something failed in loop
        if res:
            # send final char with troll
            res, _ = bindAndSend(self.request, FLAG[-1], a, True)

        # if still res then you win!
        if res:
            self.request.send("You got it ;)\n")
        else:
            self.request.send("Better luck next time\n")


class KnockerServer(ForkingMixIn, TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)


if __name__ == '__main__':
    s = KnockerServer(('', 7747), KnockerHandler)
    s.serve_forever()
