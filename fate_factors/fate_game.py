class Board():
    def __init__(self):
        self.all_cards = [i for i in range(1, 24)]
        self.chosen_cards = set()
        self.taken_cards = set()
        self.available_cards = set(self.all_cards)
        self.fated_cards = {2, 6, 10}
        self.factor_dict = dict([(i,self.other_factors(i)) for i in self.all_cards])
    
    def __str__(self):
        bstring = f"Taken: {self.taken_cards}\n"+'\n'.join([' '.join([' '*(2-len(str(j)))+str(j) if j in self.available_cards else "  " for j in range(i*6+1, i*6+7)]) for i in range(len(self.all_cards)//6+1)])

        return bstring
    
    def begin_game(self):
        print("Game is starting")
        move_set = self.available_moves()
        while (move_set):
            user_num = ""
            print(self)
            while (True):
                user_num = input("Input a valid move >> ")
                if (not user_num.isdigit() or int(user_num) not in move_set):
                    print(self)
                    print(f"Invalid move '{user_num}'")
                else:
                    break     
            chosen_num = int(user_num)
            self.available_cards.remove(chosen_num)
            self.chosen_cards.add(chosen_num)
            self.taken_cards |= (self.factor_dict[chosen_num]&self.available_cards)
            for card in self.factor_dict[chosen_num]:
                self.available_cards.discard(card)
            move_set = self.available_moves()
        print("The game is over...")
        opp_sum = sum(self.taken_cards)+sum(self.available_cards)
        user_sum = sum(self.chosen_cards)
        print(self.taken_cards)
        print(self.available_cards)
        print(self.chosen_cards)
        assert opp_sum + user_sum == 23*(23+1)/2
        print(f"Opp: {opp_sum}")
        print(f"You: {user_sum}")
        if opp_sum >= user_sum:
            print("YOU LOSE")
        else:
            print("YOU WIN")
            chosen_fated_cards = self.fated_cards&self.chosen_cards
            if (chosen_fated_cards):
                print(f"Fated Cards: {chosen_fated_cards}")
            else:
                print(f"Fated Cards: None")



    def available_moves(self):
        ans = set()
        for card in self.available_cards:
            if self.factor_dict[card]&self.available_cards:
                ans.add(card)
        return ans
        

    def other_factors(self, n):
        i = 2
        factors = {1}
        while i * i <= n:
            if n % i == 0:
                factors.add(i)
                factors.add(n // i)
            i += 1
        factors.discard(n)
        assert n not in factors
        return factors    

if __name__ == "__main__":
    print("Welcome")
    my_board = Board()
    print("_____________________")
    # print(my_board.factor_dict[1])
    # print(my_board.available_moves)
    my_board.begin_game()