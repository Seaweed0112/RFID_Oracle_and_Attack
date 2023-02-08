from bitstring import BitArray
import random


# get the two's complement of the number
def neg(s):
    mask = '1' * len(s)
    one = '0' * (len(s) - 1) + '1'
    result = plus(XOR(mask, s), one)
    return result


# xor for two bit strings
def XOR(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Bitstrings must have the same length for xor.")

    res = ""
    for i in range(len(s1)):
        if s1[i] == '*' or s2[i] == '*':
            res += '*'
        elif s1[i] == s2[i]:
            res += '0'
        else:
            res += '1'
    return res


# or for two bit strings
def OR(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Bitstrings must have the same length for or.")

    res = ""
    for i in range(len(s1)):
        if s1[i] == '1' or s2[i] == '1':
            res += '1'
        else:
            res += '0'
    return res


# and for two bit string
def AND(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Bitstrings must have the same length for and.")

    res = ""
    for i in range(len(s1)):
        if s1[i] == '1' and s2[i] == '1':
            res += '1'
        else:
            res += '0'
    return res


# get random bit string with specific length
def get_rand(key_length):
    return BitArray(uint=random.randint(0, 1 << key_length - 1), length=key_length).bin


# add operation for two bit strings which may contain unknown bits
def plus(s1, s2) -> str:
    if len(s1) != len(s2):
        raise ValueError("Bitstrings must have the same length for add.")

    result = ''
    carry = 0

    have_unknown = False

    for i in range(len(s1) - 1, -1, -1):

        if s1[i] == '*' or s2[i] == '*':
            result = '*' + result
            have_unknown = True
            continue

        if not have_unknown:
            r = carry
            r += 1 if s1[i] == '1' else 0
            r += 1 if s2[i] == '1' else 0
            result = ('1' if r % 2 == 1 else '0') + result

            carry = 0 if r < 2 else 1
        else:
            if s1[i] == '1' and s2[i] == '1':
                carry = 1
                have_unknown = False
            elif s1[i] == '0' and s2[i] == '0':
                carry = 0
                have_unknown = False
            result = '*' + result

    return result


def fp(s1):
    res = ""
    for i in range(len(s1)//4):
        s = s1[i*4:i*4+4]
        if s.count('1') % 2 == 1:
            res += '1'
        else:
            res += '0'
    return res


if __name__ == "__main__":
    a = '1111'
    b = '0011'
    print(plus(a, neg(b)))
