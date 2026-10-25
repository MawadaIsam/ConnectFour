from src.services.game import Game

class UI:

    def run(self):
        print('='*60)
        print('Welcome to CONNECT FOUR Game!')
        print('='*60)

        while True:
            print('\n1. Play Game vs Basic AI')
            print('2. Play Game vs Advanced AI(Minimax)')
            print('3. Quit')
            choice = input(" Enter your choice: ").strip()

            if choice == '1':
                self._play_game(use_minimax=False)
            elif choice == '2':
                self._play_game(use_minimax=True)
            elif choice == '3':
                print('Goodbye!!')
                break


    def _play_game(self,use_minimax=False):
        ai_type= "Advanced" if use_minimax else "Basic"
        print('='*60)
        print(f"playing vs {ai_type} AI")
        print('='*60)

        game = Game(use_minimax=use_minimax, minimax_depth=5)

        print('You are X, Computer is O')


        while not game.game_over:
            print(game.board)
            print()

            if game.current_player == 1:
                self._human_turn(game)
            else:
                self._computer_turn(game)

        print(game.board)
        print()

        if game.winner==1:
            print('You Win!')
        elif game.winner==2:
            print('You Lose, Computer Wins!')
        else:
            print('DRAW!')


    def _human_turn(self, game):
        while True:
            try:
                col_input = input('Enter Column (1-7): ').strip()
                col=int(col_input)-1
                result=game.make_move(col)

                if result['success']:
                    break
                else:
                    print(f'Error: {result["message"]}')
            except ValueError:
                print("Please enter a number 1-7")

    def _computer_turn(self, game):
        col=game.get_computer_move()
        game.make_move(col)
        print(f' Computer move: {col+1}\n')


if __name__ == '__main__':
    UI().run()


