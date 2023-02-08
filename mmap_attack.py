from mmap_oracle import MMAPoracle
from utils import get_rand, plus, XOR, neg
import random
import time
import matplotlib.pyplot as plt
import numpy as np

# fix the random number generator for testing purposes
# random.seed(42)


def MMAP_attack(oracle: MMAPoracle):
    start = time.time()

    # get the key length
    K = len(oracle.hello())
    target_id = ['*'] * K  # '*' means we haven't solved the bit yet
    unknowns = K  # number of unknown bits so far
    records = []  # to record the time elapse when we solve the ith bit
    records.append((unknowns, start, 0))

    run = 0
    # keep running the loop while there are unknown bits
    while unknowns > 0:
        run += 1

        # send hello to get the IDP
        idp = oracle.hello()

        # extract B and E
        _, b, _, _, e = oracle.protocolRun()

        # solving random number n1
        n1 = ["*"] * K
        for i in range(K):
            if idp[i] == '0':
                n1[i] = b[i]

        # get the result of this run
        curr_id = plus(XOR(e, n1), neg(idp))
        for i in range(K):
            if target_id[i] == '*' and curr_id[i] != '*':
                unknowns -= 1
                target_id[i] = curr_id[i]
                records.append((unknowns, time.time(), run))

                # print(f"run: {run}")
                # print("n1: ", "".join(n1))
                # print("curr_id: ", curr_id)
                # print("target: ", "".join(target_id))
                # print()

        # break when running for too long
        if run > 100000:
            return "".join(target_id)

    end = time.time()

    print(f"key length: {K}")
    print(f"run: {run}")
    print(f"total time: {end - start} sec")
    return "".join(target_id), records


if __name__ == '__main__':

    all_records = {}
    # repeat the experiment 100 times for different key lengths
    for key_length in [16, 48, 72, 96, 120]:
        for _ in range(100):

            k1, k2, k3, k4, idp, id = get_rand(key_length), get_rand(key_length), get_rand(
                key_length), get_rand(key_length), get_rand(key_length), get_rand(key_length)
            # print("original:")
            # print(f"k1:  {k1}")
            # print(f"k2:  {k2}")
            # print(f"k3:  {k3}")
            # print(f"k4:  {k4}")
            # print(f"idp: {idp}")
            # print(f"id:  {id}")

            # initialize MMAP oracle
            oracle = MMAPoracle(k1, k2, k3, k4, idp, id)

            # start the attack
            attack_id, records = MMAP_attack(oracle)
            # print(f"ID: {id}\nattack_id: {attack_id}")

            # check if we get the id right
            if (attack_id != id):
                raise Exception("Attack ID mismatch")

            # scatter plot of the time elapse and bits solved
            unknown_bit, timestamp, run = list(zip(*records))
            unknown_fraction = [0] * len(unknown_bit)
            time_elapse = [0] * len(unknown_bit)

            for i in range(len(unknown_bit)):
                time_elapse[i] = timestamp[i] - timestamp[0]
                unknown_fraction[i] = unknown_bit[i] / key_length

            run = np.array(run)
            time_elapse = np.array(time_elapse)

            if key_length not in all_records:
                all_records[key_length] = [unknown_fraction, time_elapse, run]
            else:
                all_records[key_length][1] = np.add(all_records[key_length][1], time_elapse)
                all_records[key_length][2] = np.add(all_records[key_length][2], run)

    # average the result
    for key_length, record in sorted(all_records.items()):
        print(key_length)
        print("average runs:", record[2][-1]/100)
        plt.plot(record[2]/100, record[0], label=key_length)

    # plot average result of each key length
    plt.legend(['16', '48', '72', '96', '120'])
    plt.xlabel('protocol runs')
    plt.ylabel('unknown fraction')
    plt.axhline(y=0.1, color='r', linestyle='-')
    plt.title('MMAP attack')
    plt.show()
