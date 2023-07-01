from threading import Lock, Thread, RLock

# list_lock = Lock() # will halt forever
list_lock = RLock()  # let reacquire lock with the same thread

"""
If you are developing a thread-safe class with a method A,
which acquires a lock, 
and a method B that also needs to acquire a lock and call method A,
you likely need to use a reentrant lock.
"""


def sum_list(int_list: list[int]) -> int:
    print("Waiting to acquire lock...")
    with list_lock:
        print("Acquired lock.")
        if len(int_list) == 0:
            print("Finished summing.")
            return 0
        else:
            head, *tail = int_list
            print("Summing rest of list.")
            return head + sum_list(tail)


thread = Thread(target=sum_list, args=([1, 2, 3, 4],))
thread.start()
thread.join()
