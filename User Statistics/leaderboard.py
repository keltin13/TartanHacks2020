#get a list of tuples of userids and total money and order them

def leaderboard(vals):
    ids = lst[]
    money = lst[]
    result = lst[]
    for i in range(len(vals)):
        ids.append(vals[0])
        money.append(vals[1])
    mergeSort(money, ids)
    for j in range(len(vals)):
        result.append((ids[j], money[j]))
    return result
    
    
# from https://www.cs.cmu.edu/~112/notes/notes-efficiency.html

def merge(a, b, start1, start2, end):
    index1 = start1
    index2 = start2
    length = end - start1
    aux = [None] * length
    aux2 = [None] * length
    for i in range(length):
        if ((index1 == start2) or
            ((index2 != end) and (a[index1] > a[index2]))):
            aux[i] = a[index2]
            aux2[i] = b[index2]
            index2 += 1
        else:
            aux[i] = a[index1]
            aux2[i]= b[index1]
            index1 += 1
    for i in range(start1, end):
        a[i] = aux[i - start1]
        b[i] = aux2[i - start1]

def mergeSort(a, b):
    n = len(a)
    step = 1
    while (step < n):
        for start1 in range(0, n, 2*step):
            start2 = min(start1 + step, n)
            end = min(start1 + 2*step, n)
            merge(a, b, start1, start2, end)
        step *= 2
