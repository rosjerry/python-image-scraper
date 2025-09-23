# import tensorflow as tf
from random import choice, randint, shuffle
from statistics import mean
import sys
from cowsay import cow, trex
    
def main():
    # random()
    # stats()
    try:
        cow("hello")
        trex("world")
    except:
        print("error happ")


def random():
    nums = ["1", "2", "6", "5"]
    shuffle(nums)
    for c in nums:
        print(c)

def stats():
    mnn = mean([100, 80, 56, 12])
    print(mnn)


main()
