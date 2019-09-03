import math

def fraction_finder(num, aprox = 20):
    top = 1
    bottom = 1
    for a in range(10000):
        result = float(top/bottom)
        if str(result)[:aprox] == str(num)[:aprox]:
            return(top,bottom)
        if (result < num):
            top += 1
        else:
            bottom += 1
    return(top,bottom)


if __name__ == "__main__":
    ipt = float(2.365)
    outa, outb = fraction_finder(ipt)
    print("%s/%s" % (outa, outb))