# made posable by https://pymotw.com/2/xml/etree/ElementTree/create.html

#import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree, tostring, parse
from xml.dom import minidom


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


if __name__ == "__main__":
    d = {"&": '&','Name': "Bob", "age": 35, "height": 6.3, "home": False, "mysc": [True,2,3.1,"four",[5,6,7.3,'nine'],'t',['sup'],{'a':'B'}],"D": {'oh':'no','two': 2, "THREE": 3.3, "Working?": True, "mysc":[1,False,5.5,'6']}}
    l = [[1,2,3],{"a":'A','b':'B','c':'C'}]
    Save('d',d)
    Save('l',l)
    v = Load('d')
    b = Load('l')

    print(d == v)
    print(l == b)
    #print(v)
