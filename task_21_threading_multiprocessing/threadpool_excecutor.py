from concurrent.futures import ThreadPoolExecutor
def work(n):
    return n*n
with ThreadPoolExecutor(max_workers=3) as pool:
    results = pool.map(work, range(5))
    print(list(results))

# there are some insecurity questions:
# for example, which can lose the accurate digit, because they adjust digits each other
import threading
count = 0
def add():
    global count
    for _ in range(1000000):
        count += 1
if __name__ == '__main__':
    threads = [threading.Thread(target=add) for _ in range(2)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(count)

# however, there is a solution to solve this problem
import threading
count = 0
lock = threading.Lock()
def add():
    global count
    for _ in range(1000000):
        with lock:
            count += 1
if __name__ == '__main__':
    threads = [threading.Thread(target=add) for _ in range(2)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(count)