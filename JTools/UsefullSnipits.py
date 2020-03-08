def average(data):
    try:
        if (type(data[0]) == list) or (type(data[0]) == tuple):
            out = []
            for d in data:
                out.append(average(d))
            return(out)
        else:
            return(sum(data)/len(data))
    except:
        return(None)