import hashlib
from multiprocessing import Pool
import time


start = time.time()

hash = ['1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad',
         '3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b',
         '74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f']


def check(words):
    for word in words:
        hashed_passwd = hashlib.sha256(word.encode('utf-8')).hexdigest()
        if hashed_passwd in hash:
            print(word, hashed_passwd)


def divide(data, count):
    output = []
    for i in range(0, len(data), count):
        output.append(data[i: i+count])
    return output


if __name__ == "__main__":
    count_threads = 0
    while count_threads < 1 or count_threads > 16:
        count_threads = int(input('Введите количество потоков от 1 до 16 -> '))

    with open('1.bin', 'r') as f:
        print('Читаем словарь')
        words = [line.strip() for line in f]

    words: list = divide(words, 100)

    with Pool(count_threads) as pool:
        print('Ищем слова')
        pool.map(check, words)

    end = time.time()
    time = end - start
    print("Время выполнения:", round(time, 2), "с")
