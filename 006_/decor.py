import time

def spent_time(func):
    """ Декорирующая функция
        Считает время затрачиваемое функцией на выполнение
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
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

def return_delta_time(start: float, name: str):
    end = time.time()
    total = int(round(((end - start) * 1000), 0))
    print()
    if total < 1000:
        print(f'function "{name}" take: {total} ms')
    elif (total//1000) < 60:
        print(f'function "{name}" take: {total//1000:02d}:{total%1000:03d} sec')
    elif ((total//1000)//60) < 60:
        print(f'function "{name}" take: {(total//1000)//60:02d}:{(total//1000)%60:02d} min')
    else:
        print(f'function "{name}" take: {((total//1000)//60)//60}:{((total//1000)//60)%60:02d} h')
    print('-' * 20)