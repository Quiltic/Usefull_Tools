from FileTools import *
#https://realpython.com/absolute-vs-relative-python-imports/
path = __file__[:-11]

'''
imports all of its freinds into this file hopefully
'''
p = File(path) # gets the files

for file in p.files:
    #print(file)
    if '__init__.py' in file: # ignores self
        continue
    else:
        file = file.replace('.py','') # file we want to import
        #print('from .{} import *'.format(file))
        exec('from .{} import *'.format(file)) # file that gets imported


  