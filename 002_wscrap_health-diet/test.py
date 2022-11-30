total = 62084
# print(f'{total:03d}')


if total < 1000:
    print(f'function " " take: {total} ms')
elif (total//1000) < 60:
    print(f'function " " take: {total//1000:02d}:{total%1000:03d} sec')
elif ((total//1000)//60) < 60:
    print(f'function " " take: {(total//1000)//60:02d}:{(total//1000)%60:02d} min')
else:
    print(f'function " " take: {((total//1000)//60)//60}:{((total//1000)//60)%60:02d} h')
print('-' * 20)