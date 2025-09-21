def main():
    # print(calculate())
    # hello()
    # mewo()
    # wafwaf()
    # multipl()
    # arrIsListInPy()
    department()


def square(num):
    return num * num


def calculate():
    return 2 + 2 != 5 and (3 * 3 != 10 and 5 / 5 == 1)


def hello(name="john doe"):
    print(f"Hello {name}, my friend!")


def mewo():
    max_num = 6
    while max_num != 0:
        max_num = max_num - 1
        if max_num % 2 == 0:
            print("we are not going to print out odd shit numbers")
            continue
        else:
            break
        # print(f"{max_num}meow")


def wafwaf():
    for _ in range(4):
        print("waf waf")


def multipl():
    print("waf\n" * 3, end="")


def arrIsListInPy():
    blueMts = ["soso", "bela", "irodioni"]

    print(blueMts[1])

    for pers in range(len(blueMts)):
        print("perss: ", pers + 1)
        print(blueMts[pers])


def department():
    blueMts = ["soso", "bela", "irodioni"]
    deps = ["shabiamani", "gazetta", "ufrosi"]

    peopLeInDes = [
        {
            "soso": {"propes": "writer", "loves": "yava"},
            "bela": {"propes": "assistant", "loves": None},
            "irodioni": {"propes": "noone knows", "loves": "egg"},
        }
    ]

    for name in peopLeInDes[0]:
        print(
            name, 
            peopLeInDes[0][name]["loves"]
        )


main()
