from collections import deque


def countdown(n):
    while n > 0:
        yield  n
        n -= 1


tasks = deque()
tasks.extend([countdown(10),
              countdown(5),
              countdown(20)])


def run():
    while tasks:
        try:
            task = tasks.popleft()
            x = next(task)
            print(x)
            tasks.append(task)
        except StopIteration:
            print("Task")


run()
