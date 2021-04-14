import random
import string


def generate_code():
    return ''.join(random.sample(string.digits, random.randint(4, 6)))

if __name__ == '__main__':
    print(generate_code())