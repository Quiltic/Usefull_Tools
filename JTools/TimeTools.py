import time
times = {}
def functionTimer(name='a',prnt = True):
    '''
    Name is the name of the process, its literaly just there for orginization and being able to use it for more than one case
    prnt is if you want it to print something or not
    '''
    global times 
    if name in times:
        t = time.time() - times[name]
        if prnt:
            print('{} finished in {} seconds'.format(name,t))
        del times[name]
        return(t)
    else:
        times[name] = time.time()
