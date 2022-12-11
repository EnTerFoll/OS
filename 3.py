import threading
from collections import deque
import random
from time import sleep
import keyboard


def worker(exit, id, interval=0.5):
    global my_queue, b, _sleep
    while (not exit.wait(interval)) and (len(my_queue) <= _sleep):
        with lock:
            if (len(my_queue) <= _sleep) and (b):
                my_queue.append(random.randint(1, 100))
                if len(my_queue) == _sleep:
                    b = False
                print('-'*56)
                print(f'Производитель {id} добавил число {my_queue[-1]} | Всего элементов - {len(my_queue)}')


def consumer(done, id, interval=2):
    global my_queue, b, l, _sleep, wake_up
    while (not done.wait(interval)) and (len(my_queue) > 0):
        with lock:
            if len(my_queue) > 0:
                if len(my_queue) >= _sleep:
                    print("\nПроизводители спят")
                    l = True
                if (l) and (len(my_queue) <= wake_up):
                    l = False
                    b = True
                    print("\nПроизводители работают")
                print(f'\nПотребитель {id} забрал число {my_queue[0]} | Всего элементов - {len(my_queue) - 1}')
                my_queue.popleft()


if __name__ == '__main__':
    q = ''
    b = True
    l = False
    _sleep = 100
    wake_up = 80
    my_queue = deque([], 200)
    my_queue.clear()
    lock = threading.Lock()
    cons = threading.Event()
    exit = threading.Event()

    work1 = threading.Thread(target=worker, args=[exit, 1], daemon=True)
    work2 = threading.Thread(target=worker, args=[exit, 2], daemon=True)
    work3 = threading.Thread(target=worker, args=[exit, 3], daemon=True)

    cons1 = threading.Thread(target=consumer, args=[cons, 1], daemon=True)
    cons2 = threading.Thread(target=consumer, args=[cons, 2], daemon=True)

    work1.start()
    work2.start()
    work3.start()

    cons1.start()
    cons2.start()

    while True:
        if keyboard.read_key() == "q" or keyboard.read_key() == "й":
            exit.set()
            sleep(3)
            break

    while len(my_queue) > 0:
        sleep(0.1)
