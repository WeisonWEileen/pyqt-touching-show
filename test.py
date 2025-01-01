import queue

q = queue.Queue()

q.put(1)
q.put(2)
q.put(3)

list = list(q.queue)
max =  max(list)
print(list)
print(max)

