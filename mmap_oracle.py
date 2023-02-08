import random
from utils import plus, get_rand, neg, XOR, AND, OR

# fix the random number generator for testing purposes
# random.seed(42)


class MMAPoracle:
    def __init__(self, k1: str, k2: str, k3: str, k4: str, idp: str, id: str):
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
        self.k4 = k4
        self.idp = idp
        self.id = id
        self.key_length = len(k1)

    def hello(self):
        return self.idp

    def protocolRun(self):
        n1 = get_rand(self.key_length)
        n2 = get_rand(self.key_length)

        a = XOR(self.idp, XOR(self.k1, n1))
        b = OR(AND(self.idp, self.k2), n1)
        c = plus(plus(self.idp, self.k3), n2)
        d = AND(OR(self.idp, self.k4), n2)
        e = XOR(plus(self.id, self.idp), n1)

        new_idp = XOR(plus(self.idp, XOR(n1, n2)), self.id)
        new_k1 = XOR(XOR(self.k1, n2), plus(self.k3, self.id))
        new_k2 = XOR(XOR(self.k2, n2), plus(self.k4, self.id))
        new_k3 = plus(XOR(self.k3, n1), plus(self.k1, self.id))
        new_k4 = plus(XOR(self.k4, n1), plus(self.k2, self.id))

        self.idp, self.k1, self.k2, self.k3, self.k4 = new_idp, new_k1, new_k2, new_k3, new_k4

        return (a, b, c, d, e)


if __name__ == '__main__':
    # key length
    K = 96

    k1, k2, k3, k4, idp, id = get_rand(K), get_rand(K), get_rand(K), get_rand(K), get_rand(K), get_rand(K)
    print("original:")
    print(f"k1:  {k1}")
    print(f"k2:  {k2}")
    print(f"k3:  {k3}")
    print(f"k4:  {k4}")
    print(f"idp: {idp}")
    print(f"id:  {id}")

    oracle = MMAPoracle(k1, k2, k3, k4, idp, id)
    for i in range(10):

        print(f"protocolRun... {i}")
        a, b, c, d, e = oracle.protocolRun()
        print("result:")
        print(f"a:   {a}")
        print(f"b:   {b}")
        print(f"c:   {c}")
        print(f"d:   {d}")
        print(f"e:   {e}")

        print("after:")
        print(f"k1:  {oracle.k1}")
        print(f"k2:  {oracle.k2}")
        print(f"k3:  {oracle.k3}")
        print(f"k4:  {oracle.k4}")
        print(f"idp: {oracle.idp}")
        print(f"id:  {oracle.id}")
