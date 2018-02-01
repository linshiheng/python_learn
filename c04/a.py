from multiprocessing import Process, Queue

queue1 = Queue()
queue2 = Queue()

def f1():
    for i in range(0,20):
        queue1.put(i)

def f2():
    
    while True:
        try:
            data = queue1.get(timeout=1)
            newdata = data*10
            queue2.put(newdata)
        except:
            print('f2 done')
            break

def f3():
    while True:
        try:
            newdata = queue2.get(timeout=1)
            print('f3 ',newdata)
        except:
            print('f3 done')
            break

Process(target=f1).start()
Process(target=f2).start()
Process(target=f3).start()
