# create a new process
from multiprocessing import Process, Queue
import time
def task(name):
    for i in range(3):
        print(f"{name}正在工作{i}")
        time.sleep(1) # use time to imitate process that make it vivid
if __name__ == "__main__":
    p = Process(target=task, args=("进程A",))
    p.start()
    p.join()
    print("全部结束")



# custom process
from multiprocessing import Process
class MyProcess(Process):
    def __init__(self, worker_name):
        # when inherit others' class, we must use transfer unless we know the class is none
        super().__init__()
        self.worker_name = worker_name
    def run(self):
        print(f"{self.worker_name} 开始干活")
if __name__ == "__main__":
    p = MyProcess("机器人1号")
    p.start()
    p.join()

# use multiprocessing to write or read files
from multiprocessing import Process
def write_file(file_name, content):
    with open(file_name, mode="w", encoding="utf-8") as f:
        f.write(content)
    print(f"{file_name} 写完了")

if __name__ == "__main__":
    tasks = [("a.txt", "内容A"), ("b.txt", "内容B"), ("c.txt", "内容c")]
    procs = []
    for fname, text in tasks:
        p = Process(target=write_file, args=(fname, text))
        p.start()
        procs.append(p)
    for p in procs:
        p.join()
    print("三个文件都写好了")

# all the process cannot share the global variable

from multiprocessing import Process
count = 0
def add():
    global count
    count += 100
    print("子进程里 count = ", count)

if __name__ == "__main__":
    p = Process(target=add)
    p.start()
    p.join()
    print("主进程里 count = ", count)

# when we want to use the global variable in the process we should use the "Queue"
from multiprocessing import Process, Queue
def producer(q):
    for i in range(3):
        q.put(f"数据{i}")
        print("input data", i)
def consumer(q):
    for _ in range(3):
        item = q.get()
        print("output data", item)

if __name__ == "__main__":
    q = Queue()
    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("transfer finished")










































