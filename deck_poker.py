class deck_poker:
    def __init__(self, name='poker', player_cards=[]):
        self.name = name
        self.deck_cards = []
        
        a={}
        for k in range(1,11):a[k]=[]
        self.player_cards = a
        
        self.table_cards = []
        
        
        
    def create_deck(self, range_cards=list(range(2,15)), colors=['p','f','q','c']):
        def list_word(l, word):
            l2=[]
            for li in l:
                l2.append(str(li)+word)
            return l2 
        t = []
        for color in colors:
            k = list_word(range_cards, color)
            t =t + k
        self.deck_cards = t
        return self
    
    def shuffle(self):
        import random
        self.deck_cards = random.sample(self.deck_cards, len(self.deck_cards))
        return self
    
    def take(self, n, player=1):
        k= self.deck_cards[:n]
        self.deck_cards= self.deck_cards[n:]
        if player ==0:
            self.table_cards.extend(k)
        if player >=1:
            self.player_cards [player] = k

        return self
    
