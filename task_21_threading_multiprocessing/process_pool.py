from multiprocessing import Pool
import time
def work(n):
    print(f"deal with {n}")
    time.sleep(1)
    return n * n

if __name__ == "__main__":
    with Pool(3) as p:
        results = p.map(work, [1,2,3,4,5])
        print(results)