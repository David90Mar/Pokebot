class game:
    def __init__(self, name='partita_poker', blind=0.005):
        self.name = name
        self.deck = deck_poker()
        self.players=0
        self.turni=[]
        self.inizio=[]
        self.bet = True
        self.piatto=0
        self.max_bet=0
        self.scommesse=1
        self.blind=blind
        
        a={}
        for k in range(1,11):a[k]=('no', 0)
        self.punti = a
        
        a={}
        for k in range(1,11):a[k]='0.000'
        self.action = a
        
        a={}
        for k in range(1,11):a[k]=0
        self.capitale = a
        
        a={}
        for k in range(1,11):a[k]=0
        self.investimento = a
        
        
    
    def start(self):
        dt = datetime.now()
        rand=int(dt.microsecond**2/(dt.year+dt.month*dt.second+dt.day*dt.minute+dt.hour+1))
        np.random.seed(rand)
        
        self.players = int(round(np.random.uniform(low=2, high=10, size=None),0))
        inizio =  int(round(np.random.uniform(low=1, high=self.players, size=None),0))
        k=[]
        k2=[]
        for i in range(1,self.players+1):
            if i>=inizio: k.append(i)
            else: k2.append(i)
        k.extend(k2)
        self.turni = k
        
        
        self.inizio=k[2:]
        k2=k[0:2]
        self.inizio.extend(k2)
        
        
        # mescolo mazzo
        self.deck =deck_poker()
        self.deck=self.deck.create_deck().shuffle()
        
        # creo casualmente il capitale
        for k in range(1,self.players+1):
            self.capitale[k]=round(np.random.uniform(low=0, high=1, size=None),3)
        
        
        #resetto carte
        self.deck.table_cards = []
        a={}
        for k in range(1,11):a[k]=[]
        self.deck.player_cards = a
        
        
        #resetto action
        
        self.bet=False
        a={}
        for k in range(1,11):a[k]= '0.000'
        self.action = a
        
        a={}
        for k in range(1,11):a[k]= 0
        self.investimento = a
        
        self.scommesse=1
        
        self.bet==True
        
        return self
    
    def simulate(self):
        # distribuisco le carte
        for i in self.turni:
            self.deck.take(n=2, player=i)
        # prendo le carte dal deck
        self.deck.take(n=5, player=0)
        for i in self.turni:
            
            self.deck.player_cards[i].extend(self.deck.table_cards)
            hand_cards=self.deck.player_cards[i][0:2]
            values=[]
            colors=[]
            for gi in np.array(self.deck.player_cards[i]):
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
            
            self.punti[i]=point(values, colors,hand_cards)
        
        
        return self
        
    