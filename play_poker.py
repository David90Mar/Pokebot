class play_poker:
        def __init__(self, name='partita_poker'):
            self.name = name
            self.play= game()
            self.play.deck = deck_poker()
            
        def calculate_probability(self,n_sim=0, salva=20000, name_output='poker_dataset.csv'):
            
            df2=pd.DataFrame(list(zip([],[],[],[])), index=range(1,11), columns=['CardA','CardB','players','classifica','punti'])

            num=0
            num_comp=0
            while True:
                if (num_comp >= n_sim) and (n_sim!=0):
                    return df2
                    break

                else:
                    self.play.deck = deck_poker()
                    self.play.deck.create_deck().shuffle()
                    self.play = game()
                    self.play.start()
                    self.play.simulate()
                    num+=1


                    n_players=[self.play.players]*10
                    t2=pd.DataFrame(n_players,columns=['giocatori'])

                    punti_numerici=[]
                    cosa=[]
                    index=[range(1,11)]
                    carta1=[]
                    carta2=[]
                    carta3=[]
                    carta4=[]
                    for k in range(1,11):
                        punti_numerici.append(self.play.punti[k][1])
                        cosa.append(self.play.punti[k][0])
                        j=self.play.deck.player_cards[k][0:2]
                        t=[]
                        for ji in j:
                            t.append(int(ji[:-1]))    
                        t.sort(reverse=True)

                        try:
                            a=t[0]
                            if a==14:
                                a=1
                            carta1.append(a)
                            carta3.append(t[0])
                        except:
                            carta1.append(np.nan)
                            carta3.append(np.nan)
                        try:
                            a=t[1]
                            if a==14:
                                a=1
                            carta2.append(a)
                            carta4.append(t[1])
                        except:
                            carta2.append(np.nan)
                            carta4.append(np.nan)


                    df=pd.DataFrame(list(zip(punti_numerici,cosa,carta1,carta2,carta3,carta4)), index=range(1,11), columns=['punti', 'comb_migliore','CardA','CardB','c','d'])

                    df=df.sort_values(by=['punti','c','d'],ascending=False)
                    df=pd.concat([df.reset_index(drop=True),g,t2], axis=1).dropna().drop(['c','d'],axis=1)

                    df2=pd.concat([df2,df],axis=0).dropna().reset_index(drop=True)
                    if (num % salva) == 0:
                        print('saved')
                        num_comp=num_comp+num
                        num=0

                        df2.to_csv(name_output, index=False)


