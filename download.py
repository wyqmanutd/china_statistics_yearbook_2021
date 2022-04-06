from api import Statistic_Yearbook_2021
import threading
from concurrent.futures import ThreadPoolExecutor,as_completed
from threading import Thread
import random
import time
import snoop

yearbook = Statistic_Yearbook_2021()
total = len(yearbook.files_urls)
# yearbook.unit_download(0)
# yearbook.unit_download(1)

@snoop
def func(i):
    time.sleep(random.choice([0.8,0.5,1,0.9,1.3,1.5,0.6]))
    yearbook.unit_download(i)
    return i+1
  
@snoop
def main():
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        threads_list = []
        for i in range(total):
            executor.submit(func,i)
            print(f"{i+1}/{total}: Threads Imported")
            threads_list.append(i)
        
        for future in as_completed(threads_list):
            data = future.result()
            print(f"第{data}个线程运行完毕")
        
    end = time.time()
    dauer = format(end-start,".2f")
    print(f"耗时：{dauer}s")    

@snoop
def main_1():
    start = time.time()
    for i in range(total):
        func(i)
        print(f"{i+1}/{total}: Threads Finished")
        
    end = time.time()
    dauer = format(end-start,".2f")
    print(f"耗时：{dauer}s")   





if __name__ == '__main__':
    # main()
    main_1()
    print("All Finished")