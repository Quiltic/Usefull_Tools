# made posable by https://pymotw.com/2/xml/etree/ElementTree/create.html

#import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree, tostring, parse
from xml.dom import minidom
import os


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Save eather a list or a dic
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# Makes it look goood
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")


# Makes lists
def CompressList(lst):
    child = Element('list')
    liststuff = []
    for a in lst:
        if type(a) == dict:
            liststuff.append(CompressDict(a))
        elif type(a) != list:
            liststuff.append(Element(str(type(a)).replace("<class '",'').replace("'>",''), val=str(a)))
        else:
            liststuff.append(CompressList(a))
    child.extend(liststuff)

    return(child)


# turns it into usable xml stuffs
def CompressDict(dic):
    top = Element('dict')
    #comment = Comment('Generated for PyMOTW')
    #top.append(comment)

    for part in dic:
        #print(part)
        if type(dic[part]) == list:
            child = SubElement(top, 'list', name = part)
            child.extend(CompressList(dic[part]))
        elif type(dic[part]) != dict:
            child = SubElement(top, str(type(dic[part])).replace("<class '",'').replace("'>",''), name = part,  val = str(dic[part]))
        else:
            child = SubElement(top, 'dict', name = part)
            child.extend(CompressDict(dic[part]))

    return(top)


# main for saving
def Save(name,data):
    F = open('{}.xml'.format(name),'w+')
    if type(data) == dict:
        F.write(prettify(CompressDict(data)))
    if type(data) == list:
        F.write(prettify(CompressList(data)))
    F.close()
#'''


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Load eather a list or a dic
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



# gives xml files
def LoadXML(NAME):
    """
    >>> f = openXMLFiles(".\\Testfiles\\patch.xml")
    >>> type(f)
    <class 'xml.etree.ElementTree.Element'>
    """
    # Basics snaged from https://docs.python.org/2/library/xml.etree.elementtree.html
    Tree = parse(NAME) # opens and turns the xml file into a tree
    Root = Tree.getroot()
    return(Root)


def typer(tipe,data):
    if tipe == 'int':
        return(int(data.attrib['val']))
    elif tipe == 'float':
        return(float(data.attrib['val']))
    elif tipe == 'bool':
        if (data.attrib['val'] == 'False') or (data.attrib['val'] == '0'):
            return(False)
        else:
            return(True) 
    #elif a.tag == 'char':
    #    returnDict[a.attrib['name']] = char(a.attrib['val'])
    elif tipe == 'list':
        return(DecompressList(data))
    elif tipe == 'dict':
        return(DecompressDict(data))
    else:
        return(data.attrib['val'])

#
def DecompressList(tree):
    returnList = []
    for a in tree:
        returnList.append(typer(a.tag,a))

    return(returnList)


#
def DecompressDict(tree):
    returnDict = {}
    for a in tree:
        returnDict[a.attrib['name']] = typer(a.tag,a)
        

    return(returnDict)


def Load(fileName):
    fileName = fileName+'.xml'
    xml = LoadXML(fileName)
    if xml.tag == 'list':
        return(DecompressList(xml))
    else:
        return(DecompressDict(xml))


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Get a listing of files/subfolders
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



class File:
    '''
    Basicly this gives info about folders and files.
    Both - Path(given to it), name, type (FOLDER if its a folder)
    Folders - dirs (folders), files, filepaths (for files), allfilepaths (all filepaths for all files inside of this folder & subfolders), 
            - subdir (all folders inside of this one), contents (strings with paths of surface files/folders), data (class File versions of contents) 
    Files - data (raw data from open(path, 'r')), contents (data.read())
    '''

    """
    Based on:
    for subdir, dirs, files in os.walk(path):
        for file in files:
            print(os.path.join(subdir, file))
    """
    def __init__(self,path = '.\\', quick=False):

        #print(path)
        self.path = path # the given path
        self.name = path.split('\\')[-1]

        tp = (path.split('.'))
        if len(tp) == 1: # split will make a len 1 list if theres no .
            self.type = 'FOLDER'
        elif ((len(tp) == 2) and (tp[0] == '')) or ('\\' in tp[-1]): # because if you do ".\\Mysc" it makes ['',"\Mysc"]
            self.type = 'FOLDER'
            #self.rootpath = os.getcwd()+path # core path?
        else:
            self.type = path.split('.')[-1]

        # iteration files
        try:
            if int(tp[-1]) != '0':
                self.type = 'FOLDER'
        except:
            pass

        if self.type == 'FOLDER':

            if not quick:
                tmp = [(subdir, dirs, files) for subdir, dirs, files in os.walk(path)] # for speed
                if tmp == []:
                    print("Not a valid FOLDER.")
                    tmp = [([],[],[])]
                #print(tmp)
                self.dirs = tmp[0][1]
                self.files = tmp[0][2]
                self.subdir = [sub[0] for sub in tmp]

                '''
                self.subdir = [subdir for subdir, dirs, files in os.walk(path)] # folderpaths inside this folder
                self.dirs = [dirs for subdir, dirs, files in os.walk(path)][0] # folders inside this folder
                self.files = [files for subdir, dirs, files in os.walk(path)][0] # files inside this folder
                #self.allfilepaths = [os.path.join(subdir, file) for subdir, dirs, files in os.walk(path) for file in files] 
                #self.data = [File(self.subdir[0]+'\\'+sub) for sub in self.dirs] # not a file
                '''
                self.filepaths = [os.path.join(path, file) for file in self.files] # filepaths inside this folder if it is a folder otherwise its empty
                self.allfilepaths = [os.path.join(b[0], file) for b in tmp for file in b[2]] # filepaths inside this folder if it is a folder otherwise its empty

                self.contents = self.filepaths + [os.path.join(path, folder) for folder in self.dirs] # all the filepaths/names for the contens
                self.data = [File(p) for p in self.contents]
            else:
                # gets only the first layer which speeds things up drimaticly
                try:
                    tmp = next(os.walk(path)) # for speed
                except:
                    print("Not a valid FOLDER.")
                    tmp = [[],[],[]]

                self.dirs = tmp[1]
                self.files = tmp[2]
                self.subdir = tmp[0]

                self.filepaths = [os.path.join(path, file) for file in self.files] # filepaths inside this folder if it is a folder otherwise its empty
                self.allfilepaths = self.filepaths # filepaths inside this folder if it is a folder otherwise its empty

                self.contents = self.filepaths + [os.path.join(path, folder) for folder in self.dirs] # all the filepaths/names for the contens
                self.data = None
                
        else:
            # if its a file
            self.subdir = None
            self.dirs = None   
            self.files = None
            self.filepaths = None
            self.allfilepaths = None
            # if its not able to get the info, mostly a problem with .lnk files (link files)
            try:
                self.data = open(path,'r') # a file
                self.contents = self.data.read()
            except:
                self.data = None
                self.contents = None


    def isDirectory(self):
        if self.name == 'FOLDER':
            return(True)
        return(False)

    def help(self):
        print("Contains path, name, type, subdir, dirs, files, filepaths, allfilepaths, data, and contents.")
        print("Has a faster verson if you do File(path,True). This version misses subdir and data")
    

"""
if __name__ == "__main__":
    pass

    path = ".\\Mysc"
    #path = "Maze.py"
    print(File(path).subdir) 
    File()
    #""
    d = {"&": '&','Name': "Bob", "age": 35, "height": 6.3, "home": False, "mysc": [True,2,3.1,"four",[5,6,7.3,'nine'],'t',['sup'],{'a':'B'}],"D": {'oh':'no','two': 2, "THREE": 3.3, "Working?": True, "mysc":[1,False,5.5,'6']}}
    l = [[1,2,3],{"a":'A','b':'B','c':'C'}]
    Save('d',d)
    Save('l',l)
    v = Load('d')
    b = Load('l')

    print(d == v)
    print(l == b)
    #print(v)
    """