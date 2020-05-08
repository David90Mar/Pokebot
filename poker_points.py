def scala_colore(values, colors)  :  
    k=list(map(lambda x:x,Counter(colors).most_common()))[0]
    if k[1]>=5:
        values=np.array(values)[list(np.where(np.array(colors[0:10]) == k[0])[0])]
        s=scala(values)
        if s[1]:
            return 'scala_colore', True, s[2]+1000
        else:
            return 'no', False,0
    else:
        return 'no', False,0

def colore(colors,values):
    somma=0
    k=list(map(lambda x:x,Counter(colors).most_common()))[0]
    if k[1]>=5:
        somma=sum(np.array(values)[list(np.where(np.array(colors) == k[0])[0][0:5])])
        return 'colore', True, somma+500
    else:
        return 'NO', False, 0



def scala(values):
    import numpy as np
    k = np.diff(np.sort(np.array(list(values)))[::-1])
    if len(k[0:len(k)-2][k[0:len(k)-2]==-1])==4:
        return 'scala', True, sum(values[0:(len(values)-2)])+200
    elif len(k[1:len(k)-1][k[1:len(k)-1]==-1])==4:
        return 'scala', True, sum(values[1:(len(values)-1)])+200
    elif len(k[2:len(k)][k[2:len(k)]==-1])==4:
        return 'scala', True, sum(values[2:len(values)])+200
    else: 
        return 'no', False


def poker_tris(values, val):
    t=list(map(lambda x:x,Counter(values).most_common()))[0]

    if t[1]>=val:
        if val==4:
            point =t[0]*4+750
            res ='poker'
        elif val ==3:
            point = t[0]*3+120
            res ='tris'
        return res, True, point
    else:
        return 'no', False,0

def full(values):
    t=list(map(lambda x:x,Counter(values).most_common()))[0:2]
    if t[0][1]>=3:
        try:
            if t[1][1]>=2:

                return 'full',True, t[0][0]*3+t[1][0]*2+300
            else:
                return 'no',False,0
        except:
            return 'no', False, 0
    else:
        return 'no',False, 0

def doppia_coppia(values):
    t=list(map(lambda x:x,Counter(values).most_common()))[0:2]
    if t[0][1]>=2:
        try:
            if t[1][1]>=2:
                return 'doppia_coppia',True,t[0][0]*2+t[1][0]*2+50
            else:
                return 'no',False,0
        except: return 'no', False,0
    else:
        return 'no',False,0

def coppia(values):
    t=list(map(lambda x:x,Counter(values).most_common()))[0]
    if t[1]>=2:
        return 'coppia',True, t[0]*2+20
    else:
        return 'no',False, 0

def high_card(values):
    cards=[]
    for card in values:
        cards.append(int(card[:-1]))

    k = np.array(list(set(cards)))
    k = np.sort(k)[::-1][0]
    return 'high_card',True,k


def point(values,colors,hand_cards):
    carta_alta =high_card(hand_cards)[2]
    A=scala_colore(values,colors)
    if A[1]:return A[0],A[2]
    A=poker_tris(values,4)
    if A[1]:return A[0],A[2]
    A=colore(colors,values)
    if A[1]:return A[0],A[2]
    A=full(values)
    if A[1]:return A[0],A[2]
    A=scala(values)
    if A[1]:return A[0],A[2]
    A=poker_tris(values,3)
    if A[1]:return A[0],A[2]
    A=doppia_coppia(values)
    if A[1]:return A[0],A[2]
    A=coppia(values)
    if A[1]:return A[0],A[2]
    A=high_card(hand_cards)
    return A[0],A[2]
