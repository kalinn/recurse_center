# Write a recursive function that adds elements in a list

def mysum(mylist):
    if len(mylist)==0:
        return 0
    elif len(mylist)==1:
        return mylist[0]
    else:
        addtwo = [mylist[0] + mylist[1]]
        newlist = addtwo + mylist[2:]
        return mysum(newlist)

