
with open(r"C:\Users\BenQ\Desktop\testdata.txt") as fp:
    lists = fp.readlines()
cache = ["1",]

for x in lists:
    x=x.replace("\n", "")
    y = x.split("_")
    if y[0] != cache[0]:
        cache = y
    elif cache[0] == y[0]:
        if int(y[1]) > int(cache[1]) and int(y[2]) < int(cache[2]):
            print(" OK ")

        elif int(y[1]) <= int(cache[1]) and int(y[2]) >= int(cache[2]):
            print(" OK ")
        else:
            print(y[3])