import threading as th
import time
def task(name):
    for i in range(3):
        print(f"{name} {i}")
        time.sleep(0.5)
if __name__ == '__main__':
    t = th.Thread(target=task, args=("taskA",))
    t.start()
    t.join()
    print("END")
