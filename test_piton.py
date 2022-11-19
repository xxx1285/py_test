name = "str_"
for n in range (5):
    exec(name + "%s = %d" % (n,n))
    print(name)
