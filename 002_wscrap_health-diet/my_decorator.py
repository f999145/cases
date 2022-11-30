import time
def my_decorator(func):
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        total = int(round(((end - start) * 1000), 0))
        print()
        if total < 1000:
            print(f'function "{func.__name__}" take: {total} ms')
        elif (total//1000) < 60:
            print(f'function "{func.__name__}" take: {total//1000:02d}:{total%1000:03d} sec')
        elif ((total//1000)//60) < 60:
            print(f'function "{func.__name__}" take: {(total//1000)//60:02d}:{(total//1000)%60:02d} min')
        else:
            print(f'function "{func.__name__}" take: {((total//1000)//60)//60}:{((total//1000)//60)%60:02d} h')
        print('-' * 20)
    return wrapper