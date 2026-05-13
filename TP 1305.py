def weak_before(a,b,k) :
    if k=="score":
        if a>b:
            return True
        else:
            return False
    elif k=="timestamp":
        if a<b:
            return True
        else:
            return False
