play = game()
play.start()

def salva_df(play,turn,phase,giro):    
    n_player=[play.players]*10 
    piatto=[play.piatto]*10  
    max_bet=[play.max_bet]*10    
    punti_numerici=[]
    cosa=[]
    index=[range(1,11)]
    carta1=[]
    carta2=[]
    for k in range(1,11):
        # salva in "punti_numerici" i punti ottenuti da ogni giocatore
        # salvia in "cosa", la miglior combinazione ottenuta  
        punti_numerici.append(play.punti[k][1])
        cosa.append(play.punti[k][0])
        try:
            a=play.deck.player_cards[k][0]
            if a[:-1]=='14':
                a=a.replace('14','1')   # converte 14 con il 1 (asso)
            carta1.append(a)
        except:
            carta1.append(np.nan)
        try:
            a=play.deck.player_cards[k][1] #se il player non sta giocando cadrà sull'except e mettterà nan
            if a[:-1]=='14':
                a=a.replace('14','1')
            carta2.append(a)
        except:
            carta2.append(np.nan)

    giocatore=[1,2,3,4,5,6,7,8,9,10]
    fase=[phase]*10
    turno=[str(turn)]*10

    table_card=[]
    for k in range(0,5): # creiamo le colonne contenenti le carte 
                         # sul tavolo
        try: table_card.append(play.deck.table_cards[k])
        except: table_card.append('NULL')
            
    table_card1=[table_card[0]]*10
    table_card2=[table_card[1]]*10
    table_card3=[table_card[2]]*10
    table_card4=[table_card[3]]*10
    table_card5=[table_card[4]]*10


    cap=[]  # salviamo il capitale
    for k in range(1,11):
        cap.append(play.capitale[k])
    act=[] #salvialo l'azione
    for k in range(1,11):
        act.append(play.action[k][:-6])
    val_act=[] # salviamo il valore numerico dell'azione
    for k in range(1,11):
        val_act.append(play.action[k][-5:])

    inv=[] #salviamo investimento
    for k in range(1,11):
        inv.append(play.investimento[k])

    tu=1 #salviamo l'ordine di chi inizia prima
    ju=[0,0,0,0,0,0,0,0,0,0,0]
    for k in range(0,len(giro)):
        ju[giro[k]]=tu
        tu+=1
    ju=ju[1:]
    
    tur_max=[0,0,0,0,0,0,0,0,0,0] #mettiamo tutto nel dataset
    df=pd.DataFrame(list(zip(fase,turno,giocatore,n_player,carta1,carta2,table_card1,table_card2,table_card3,table_card4,table_card5,cap,inv,max_bet,piatto,act,val_act,ju,tur_max)), index=range(1,11), columns=['Fase','phase','giocatore','#_giocatori','Carta1','Carta2','Banco1','Banco2','Banco3','Banco4','Banco5','capitale','inv','max_bet','piatto','azione','val_act','turno','max_turno']).dropna()
    return df

def fold_check() : # vede se tutti i giocatori meno 1 hanno foldato
    h=0
    for ply2 in play.turni:
        if play.action[ply2][0:4]=='FOLD':
            h+=1
    if len(play.turni) - h<=1:
        return True
    else:
        return False

def check_finish(): # vede se fermare la partita   
    h=0
    for ply2 in play.turni:
        if (play.action[ply2][0:4]=='FOLD') or (play.action[ply2][0:6]=='ALL_IN') or (round(play.investimento[ply2],3)==round(play.max_bet,3)):
            h+=1
    if len(play.turni) - h==0:
        return True
    else:
        return False

df=pd.DataFrame(list(zip([],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[])), index=range(1,11), columns=['Fase','phase','giocatore','#_giocatori','Carta1','Carta2','Banco1','Banco2','Banco3','Banco4','Banco5','capitale','inv','max_bet','piatto','azione','val_act','turno','max_turno']).dropna()
# dai le carte ai giocatori
for ply in play.turni:
    play.deck.take(2, player=ply)

# metti il bind
play.capitale[play.turni[0]]=play.capitale[play.turni[0]]-play.blind
play.investimento[play.turni[0]]=play.investimento[play.turni[0]]+play.blind
play.action[play.turni[0]]='CALL: 0.005'
play.capitale[play.turni[1]]=play.capitale[play.turni[1]]-play.blind*2
play.investimento[play.turni[1]]=play.investimento[play.turni[1]]+play.blind*2
play.action[play.turni[1]]='CALL: 0.01'
# valorizza il piatto e la piu grande scommessa del momento
play.piatto=0.015
play.max_bet=play.blind*2

fasi =['1-PREFLOP', '2-FLOP', '3-TURN', '4-RIVER']
#fasi =['PREFLOP']
for fase in fasi:
    all_fold=0
    ki=0
    play.scommesse=1
    if fase != '1-PREFLOP':
        play.bet=True
        giro = play.turni
    else:
        play.bet=False
        giro= play.inizio
        moltiplicatore=1
    if fase =='2-FLOP':
        ti=3
        play.deck.take(4,0)
        play.deck.table_cards = play.deck.table_cards[1:4]
        moltiplicatore=1
    elif fase=='3-TURN':
        play.deck.take(2,0)
        play.deck.table_cards.pop(3)
        moltiplicatore=2
    elif fase=='4-RIVER':
        play.deck.take(2,0)
        play.deck.table_cards.pop(4)
        moltiplicatore=2

    while True: # gira infinito finchè o tutti foldano salvo uno o se hanno effettuato call
        ki+=1
        if (all_fold==1) or (check_finish()==True and ki>1) :
            df['max_turno'] = int(df['phase'].max())
            break

        for ply in giro: # giriamo per ogni giocatore, da quelli che non hanno blindato
            if (fold_check())==True and play.action[ply][0:4] != 'FOLD':
                play.action[ply] = 'LAST: '+str(play.action[ply])
                all_fold=1
            # se il giocatore è l'unico che non ha foldato, finisce la partita

            elif (play.action[ply][0:4] != 'FOLD') and (play.action[ply][0:6] != 'ALL_IN') : # se non ha foldato o ha fatto all_in
                if play.bet==False: # se non hanno ancora fatto una scommessa
                    choice=['check','bet']
                    random=int(np.random.uniform(low=0, high=1.99999999999999, size=None))
                    if (choice[random]=='bet') & (play.capitale[ply]>= play.max_bet+0.01*moltiplicatore) :
                        # se scommette, si vede se il capitale e piu alto almeno della scommessa minima

                        play.max_bet = round(play.max_bet+0.01*moltiplicatore,3)
                        play.scommesse+=1
                        play.piatto=play.piatto+play.max_bet-float(play.action[ply][-4:])
                        play.capitale[ply]=play.capitale[ply]-play.max_bet
                        play.investimento[ply]=play.investimento[ply]+play.max_bet-float(play.action[ply][-4:])
                        play.action[ply] = 'RAISE: '+str(round(play.max_bet,3))
                        play.bet=True
                    elif (choice[random]=='bet') & (play.capitale[ply]< play.max_bet+0.01*moltiplicatore) & (play.capitale[ply]> play.max_bet+0.001) :
                        # se scommette, si vede se il capitale e piu alto almeno della scommessa minima

                        play.piatto=play.piatto+play.capitale[ply]-float(play.action[ply][-4:])
                        play.max_bet= round(play.max_bet+ play.capitale[ply],3)
                        play.investimento[ply]=play.investimento[ply]+play.capitale[ply]-round(float(play.action[ply][-4:]),3)
                        play.scommesse+=1
                        play.action[ply] = 'ALL_IN: '+str(float(round(play.capitale[ply],3)))
                        play.capitale[ply]=0
                        play.bet=True

                    else: # check
                        play.action[ply] = 'CHECK: 0.00'

                elif (play.bet==True)  & (float(play.action[ply][-4:])<=play.max_bet): # se hanno già fatto una scommessa e scommesso meno del massimo
                    choice=['call','fold','raise']   #se hanno fatto meno di 4 raise, possono scegliere anche raise
                    if play.scommesse<4:
                        random=int(np.random.uniform(low=0, high=3, size=None))
                    else:
                        random=int(np.random.uniform(low=0, high=2, size=None))
                    if (choice[random]=='call') :   # risponde alla scommessa
                        if (play.capitale[ply]>= play.max_bet) : # se il capitale può coprire la massima scommessa
                            play.piatto=play.piatto+play.max_bet-float(play.action[ply][-4:])
                            play.capitale[ply]=play.capitale[ply]- play.max_bet+float(play.action[ply][-4:])
                            play.investimento[ply]=play.investimento[ply]+play.max_bet-float(play.action[ply][-4:])
                            play.action[ply] = 'CALL: '+str(round(play.max_bet,3))
                        else:   # se non può, mette tutto quello che ha
                            play.piatto=play.piatto+play.capitale[ply]-float(play.action[ply][-4:])
                            play.investimento[ply]=play.investimento[ply]+play.capitale[ply]-round(float(play.action[ply][-4:]),3)
                            play.action[ply] = 'ALL_IN: '+str(round(float(play.capitale[ply]),3))
                            play.capitale[ply]=0
                    elif choice[random]=='raise':  # fa un raise
                        if (play.capitale[ply]>= play.max_bet+0.01*moltiplicatore): # se può scommettere piu del minimo, lo fa                   
                            play.max_bet = round(play.max_bet+0.01*moltiplicatore,3)
                            play.scommesse+=1
                            play.piatto=play.piatto+play.max_bet-float(play.action[ply][-4:])
                            play.capitale[ply]=play.capitale[ply]-play.max_bet+float(play.action[ply][-4:])
                            play.investimento[ply]=play.investimento[ply]+play.max_bet-float(play.action[ply][-4:])
                            play.action[ply] = 'RAISE: '+str(round(play.max_bet,3))
                        elif (play.capitale[ply]> play.max_bet+0.001) & (play.capitale[ply]< play.max_bet+0.01*moltiplicatore):
                             #altrimenti scommette quello che gli è rimasto
                            play.piatto=play.piatto+play.capitale[ply]-float(play.action[ply][-4:])
                            play.max_bet= round(play.max_bet+ play.capitale[ply],3)
                            play.investimento[ply]=play.investimento[ply]+play.capitale[ply]-round(float(play.action[ply][-4:]),3)
                            play.scommesse+=1
                            play.action[ply] = 'ALL_IN: '+str(float(round(play.capitale[ply],3)))
                            play.capitale[ply]=0
                    else: #fold
                        play.action[ply] = 'FOLD: 0.00' # altrimenti folda
                        pass
                elif (float(play.action[ply][-4:])>=play.max_bet): # se già ja coperto il max_bet, passa il turno
                        play.action[ply] = 'PASS: '+str(play.action[ply])




        #salviamo
        df=df.append(salva_df(play,ki,fase,giro))




punti_numerici=[]
cosa=[]
for i in range(1,play.players+1):
        
        play.deck.player_cards[i].extend(play.deck.table_cards)
        hand_cards=play.deck.player_cards[i][0:2]
        values=[]
        colors=[]
        for gi in np.array(play.deck.player_cards[i]):
            for color in ['p','f','q','c']:
                if color in gi:
                    values.append(int(gi.replace(color,'')))
                    colors.append(color)

        a=list(zip(values,colors))

        def getKey(item):
             return item[0]

        s=sorted(a, key=getKey, reverse= True)

        values =[]
        colors=[]
        for si in s:
            values.append(si[0])
            colors.append(si[1])

        play.punti[i]=point(values, colors,hand_cards)
        punti_numerici.append(play.punti[i][1])
        cosa.append(play.punti[i][0])
        
df['Carta3']=df['Carta1'].astype(str).str[:-1].astype(np.int64)
df['Carta4']=df['Carta2'].astype(str).str[:-1].astype(np.int64)
df['Carta_max']=df[["Carta3", "Carta4"]].max(axis=1)
df['Carta_min']=df[["Carta3", "Carta4"]].min(axis=1)

ind=range(1,play.players+1)
tg=pd.DataFrame(zip(ind, cosa,punti_numerici), columns=['giocatore','best_comb','point'])
df=pd.merge(df, tg, on='giocatore')
dfk=df.sort_values(['point','Carta_max','Carta_min'],ascending=False)
juy=list(dfk[['giocatore','point','Carta_max','Carta_min']]['giocatore'].unique())
df2=pd.DataFrame(list(zip(juy,list(range(1,len(juy)+1)))), columns=['giocatore','classifica'])
                 
df=pd.merge(df, df2, on='giocatore').sort_values(['Fase','phase']).drop(['Carta3','Carta4'],axis=1)

k_fin=df[(df['Fase']=='4-RIVER') & (df['azione']!='FOLD') ].sort_values('classifica').append(df[(df['Fase']=='4-RIVER') & (df['azione']=='FOLD') ].sort_values('classifica'))
k_fin['classifica_reale']=list(range(k_fin.shape[0]+1))[1:]

df=pd.merge(df, k_fin[['giocatore','classifica_reale']], on='giocatore')
df[(df['Fase']=='4-RIVER') & (df['azione']=='FOLD') ].sort_values('classifica')

df.sort_values(['Fase','phase'])