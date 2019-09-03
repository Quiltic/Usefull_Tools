"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Save a Dictionary to a easy to read .txt file
    please note this is not for increadibly complex dictionarys, NO Dictionary INSIDE!
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def Load_Dic(Name):
    if ('.' not in Name):
        Name = Name + '.txt' 
    #Loads a card from a file
    file = open(Name,'r')
    Dic = {}
    for a in file:
        #get the segments name, type, and inner stuffs
        tipe = a[a.index(' ')+1:]
        inner = a[a.index('> ')+2:]
        name = a[:a.index(' ')]
        
        #remove the new line
        inner = inner.replace('\n','')

        #correct for being a string
        if ("int" in tipe):
            Dic[name] = int(inner)
        elif ("float" in tipe):
            Dic[name] = float(inner)
        elif ("list" in tipe):
            #lists are dumb when turned into a string
            inner = inner.replace('[','')
            inner = inner.replace(']','')
            #make it back into a list
            inner = inner.split(",")
            #make the inside what it is suposed to be
            for thing in range(len(inner)):
                try:
                    #floats are basicly complex ints right?
                    inner[thing] = float(inner[thing])
                except:
                    #basicly it adds "" to the outside of the thing if its not removed hence the [] stuff
                    inner[thing] = (inner[thing])[2:len(inner[thing])-1]
            Dic[name] = inner
        else:
            #string or unidentified
            Dic[name] = str(inner)
    
    return(Dic)

def Save_Dic(Name, Dictionary):
    if ('.' not in Name):
        Name = Name + '.txt'
    #save the files to here
    file = open(Name, 'w')
    for part in Dictionary:
        #name type inner
        line = str(part +' '+ str(type(Dictionary[part])) + ' '+ str(Dictionary[part])+'\n')
        #write the stats
        file.write(line)
    #save
    file.close()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Save a Dictionary to a easy to read .txt file
    please note this is not for increadibly complex lists like [1,[1,[1,1]]]
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def Load_List(Name): 
    if ('.' not in Name):
        Name = Name + '.txt' 
    #Loads a card from a file
    file = open(Name,'r')
    lst = []
    for a in file:
        #get the segments name, type, and inner stuffs
        tipe = a[a.index(' ')+1:]
        inner = a[a.index('> ')+2:]
        
        #remove the new line
        inner = inner.replace('\n','')

        #correct for being a string
        if ("int" in tipe):
            lst.append(int(inner))
        elif ("float" in tipe):
            lst.append(float(inner))
        elif ("list" in tipe):
            #lists are dumb when turned into a string
            inner = inner.replace('[','')
            inner = inner.replace(']','')
            #make it back into a list
            inner = inner.split(",")
            #make the inside what it is suposed to be
            for thing in range(len(inner)):
                try:
                    #floats are basicly complex ints right?
                    inner[thing] = float(inner[thing])
                except:
                    #basicly it adds "" to the outside of the thing if its not removed hence the [] stuff
                    inner[thing] = (inner[thing])[2:len(inner[thing])-1]
            lst.append(inner)
        else:
            #string or unidentified
            lst.append(str(inner))

    return(lst)

def Save_List(Name,List):
    if ('.' not in Name):
        Name = Name + '.txt'
    #save the files to here
    file = open(Name, 'w')
    for part in List:
        #write the stats
        file.write(str(type(part)) +' ' + str(part) + '\n')
    #save
    file.close()


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Save/load eather a list or a dic
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def Load_file():
    pass

def Save_file(Name, stuff_to_save):
    if ('.' not in Name):
        Name = Name + '.txt'      
    
    if type(stuff_to_save) == list:  
        Save_List(Name,stuff_to_save)
    elif type(stuff_to_save) == dict:  
        Save_Dic(Name,stuff_to_save)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Test the entire file
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if (__name__ == "__main__"):
    #this is used to test Dictionary stuff
    temp = {"words": "hi","numbers": 12, "floats": 35.89, "array": [1,2,3,4, "five"]}
    Save_file("Test",temp)
    print(Load_Dic("Test"))
    temp = ["one", 2, 3, "four", 5.5, 6.6, [1,2,3,4,5,6,'seven']]
    Save_file("Test",temp)
    print(Load_List('Test'))
