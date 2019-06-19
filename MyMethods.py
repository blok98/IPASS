import numpy
import json

#print
def printm(matrix):     #print matrixes in numpy format
    try:
        if type(matrix[0]) == list:
            for row in matrix:
                print(numpy.array(row))
        elif type(matrix) == list:
            print(numpy.array(matrix))
    except Exception:
        if type(matrix) == list:
            print(numpy.array(matrix))
        else:
            print(matrix)
    print("")

def printv(a="", b="", c="", d="", e="", f="", g="", h="", i="", j="", k="", l="", m="", n=""):     #kan meer dan 2 dingen printen
    print(a, b, end=" ")
    print(c, d, end=" ")
    print(e, f, end=" ")
    print(g, h, end=" ")
    print(i, j, end=" ")
    print(k, l, end=" ")
    print(m, n, end="\n")



def printr(data,layers=1,index=None,limiter=25,):            #print elk element uit een for loop
    if layers <= 0:
        return True
    if limiter <=0:
        return True
    for i in data:
        if index != None:
            try:
                print(i[index])
            except Exception as e:
                print(e)
        else:
            print(i)
        printr(i, layers - 1, index, limiter-1)

def printt(value):
    print("type("+str(value)+")="+str(type(value)))

#open
def openjs(filename,mode="r"):
    with open(filename,mode) as json_file:
        data = json.load(json_file)
    return data

def openf(filename,mode="r"):
    with open(filename,mode) as file:
        data = file.read()
    return data

#list
def listType(list,type):

    for i in range(len(list)):
        list[i]=type(list[i])
    return list

def listWhere(list,where="element!=None"):
    aantalRemoved=0
    list2=[]
    for element in list:
        if eval(where):
            list2.append(element)
        else:
            aantalRemoved+=1
    print("aantal removed: ",aantalRemoved)
    return list2

#dict
def dictWhere(dict,where="element!=None"):
    dict2=dict
    aantalRemoved=0
    for element in list(dict):
        if not eval(where):
            dict2.pop(element)
            aantalRemoved+=1
    print("aantal removed: ", aantalRemoved)
    return dict2























