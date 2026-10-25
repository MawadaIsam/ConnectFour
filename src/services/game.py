import random as rnd

from src.domain import board
from src.domain.board import Board
from src.exceptions.exceptions import OutOfBoundsException, ColumnFilledException


class MinimaxAI:

    def __init__(self,depth=5):
        self.max_depth = depth

    def get_best_move(self,board):
        """
        get the best move using minimax algorithm
        This method explores the game tree up to a specified depth, evaluating all
        possible moves and their consequences. It assumes both players play optimally
        and selects the move that maximizes the computer's advantage.

        :param board: current board instance

        :return: best_column: int: the best column for the computer to play(0-6)
        defaults to col 3 (center) if no move are evaluated

        :algorithm:
        1. Initialize best_score to negative infinity
        2. Try dropping a piece in each non-full column
        3. Recursively evaluate each position using minimax
        4. Undo each simulated move to restore board state
        5. Track the move with the highest score
        6. Apply alpha-beta pruning to optimize search
        """
        best_score = float('-inf')
        best_column = 3
        alpha = float('-inf')
        beta = float('inf')

        #trying each column
        for col in range (board.cols):
            if board.is_column_full(col):
                continue

            #move simulation
            row = board.drop_piece(col,2)
            #evaluate the move
            score= self._minimax(board, self.max_depth - 1, False, alpha, beta)

            #undo the move
            board.grid[row][col]=0
            #updating the best move
            if score > best_score:
                best_score = score
                best_column = col
            alpha=max(alpha, best_score)

        return best_column


    def _minimax(self,board,depth,is_maximizing,alpha, beta):
        """
        recursive minimax with alpha-beta pruning for game tree evaluation

        This is the core recursive function that explores the game tree, alternating
        between maximizing (computer) and minimizing (human) players. It uses
        alpha-beta pruning to eliminate branches that cannot influence the final decision

        :param board: current board state
        :param depth: remaining depth to search
        :param is_maximizing: True if computer's turn (maximizing score), false if player's turn
        :param alpha: best score maximizer can guarantee
        :param beta: best score minimizer can guarantee
        :return: score of this position
        int or float: Numerical score representing the position's value:
                     - Positive: Favors computer (player 2)
                     - Negative: Favors human (player 1)
                     - Zero: Neutral or draw position
                     - Terminal wins: ±10000 ± depth (prefer faster wins/slower losses)

        Terminal Conditions:
            - Computer wins (player 2): Returns 10000 + depth
            - Human wins (player 1): Returns -10000 - depth
            - Board full (draw): Returns 0
            - Depth limit reached: Returns heuristic evaluation score

        Pruning:
            - Beta cutoff: If beta ≤ alpha in maximizing phase, stop searching
            - Alpha cutoff: If beta ≤ alpha in minimizing phase, stop searching
            - Rationale: The opponent won't allow this branch in optimal play

        Algorithm:
            Maximizing (Computer's turn):
                1. Start with max_score = -infinity
                2. Try each valid move
                3. Recursively evaluate as minimizing player
                4. Update max_score and alpha
                5. Prune if beta ≤ alpha

            Minimizing (Human's turn):
                1. Start with min_score = +infinity
                2. Try each valid move
                3. Recursively evaluate as maximizing player
                4. Update min_score and beta
                5. Prune if beta ≤ alpha
        """
        winner= board.check_winner()

        # Terminal states
        if winner == 2:  # Computer wins
            return 10000 + depth  # Prefer faster wins
        elif winner == 1:  # Human wins
            return -10000 - depth  # Prefer slower losses
        elif board.is_full():  # Draw
            return 0
        elif depth == 0:  # Depth limit reached
            return self._evaluate_position(board)

        if is_maximizing:

            max_score = float('-inf')
            for col in range (board.cols):
                if board.is_column_full(col):
                    continue

                row= board.drop_piece(col,2)
                score = self._minimax(board, depth - 1, False, alpha, beta)
                board.grid[row][col]=0

                max_score = max(max_score, score)
                alpha=max(alpha, score)

                if beta <= alpha:
                    break # beta cutoff - opponent wont allow this path

            return max_score
        else:
            # human's turn: minimize the score
            min_score = float('inf')
            for col in range (board.cols):
                if board.is_column_full(col):
                    continue

                row= board.drop_piece(col,1)
                score = self._minimax(board, depth - 1, True, alpha, beta)
                board.grid[row][col]=0

                min_score = min(min_score, score)
                beta= min(beta,score)

                if beta <= alpha:
                    break # alpha cutoff, computer won't allow this path

            return min_score

    def _evaluate_position(self,board):
        """
        Heuristically evaluate a non-terminal board position.

        Called when the search depth limit is reached and no winner is determined.
        Estimates the position's value by analyzing strategic features like center
        control and potential winning patterns (windows).
        :param board: the board position to evaluate
        :return: int: numerical score representing the position's strength:
            - +: computer has advantage
            - -: human has advantage
            zero : roughly equal position
        """
        score = 0

        center_col = board.cols//2
        center_count= sum(1 for row in range(board.rows)
                          if board.grid[row][center_col] == 2) #counts how many computer pieces are in the center
        score+= center_count * 3 # adds 3 points to the score for each piece

        score+= self._score_all_windows(board,2)
        score-= self._score_all_windows(board,1)

        return score

    def _score_all_windows(self,board,player):
        """
        Calculate total score from all possible 4-cell windows for a given player.

        A "window" is any sequence of 4 adjacent cells that could potentially form
        a Connect Four win. This method systematically checks all possible windows
        in all directions and sums their individual scores.

        :param board: current board state to analyze
        :param player:player to evaluate(1,2)
        :return:int: Total score from all windows for the specified player:
             - Higher scores indicate more/stronger winning opportunities
             - Blocked windows (containing opponent pieces) score 0
        """
        score = 0
        #horizontal windows
        for row in range(board.rows):
            for col in range(board.cols-3):
                window = [board.grid[row][col+i] for i in range(4)]
                score+= self._score_window(window,player)

        # vertical windows
        for row in range(board.rows - 3):
            for col in range(board.cols):
                window = [board.grid[row + i][col] for i in range(4)]
                score += self._score_window(window, player)

            # Diagonal (down-right) windows
        for row in range(board.rows - 3):
            for col in range(board.cols - 3):
                window = [board.grid[row + i][col + i] for i in range(4)]
                score += self._score_window(window, player)

            # Diagonal (down-left) windows
        for row in range(board.rows - 3):
            for col in range(3, board.cols):
                window = [board.grid[row + i][col - i] for i in range(4)]
                score += self._score_window(window, player)

        return score

    def _score_window(self,window,player):
        """
        Evaluate a single 4-cell window's strategic value for a player.

        Assigns points based on how close the window is to forming a Connect Four
        win. Windows containing opponent pieces are considered blocked and score 0

        Scoring:
        - 4 in a row: 100 points (win)
        - 3 in a row with 1 empty: 5 points (threat)
        - 2 in a row with 2 empty: 2 points (potential)
        - Blocked by opponent: 0 points
        :param window:list: list of exactly four 4-cell values(each is 1 or 2 or 0)
        :param player: the player to score for (1 or 2)
        :return:int: score for this window based on the scoring above
        """
        opponent= 3 - player
        player_count= window.count(player)
        empty_count= window.count(0)
        opponent_count= window.count(opponent)

        # if opponent has pieces in this window, it is blocked

        if opponent_count > 0:
            return 0
        #score based on how many pieces we have
        if player_count == 4:
            return 100
        elif player_count == 3 and empty_count == 1:
            return 5
        elif player_count == 2 and empty_count == 2:
            return 2

        return 0

class Game:
    def __init__(self,use_minimax=False, minimax_depth=5):
        self.board = Board()
        self.current_player = 1  # 1: human  2: computer
        self.game_over = False
        self.winner = None
        self.use_minimax = use_minimax

        if use_minimax:
            self.minimax_ai = MinimaxAI(depth=minimax_depth)
        else:
            self.minimax_ai = None

    def make_move(self,col):
        """
        execute a move for the current player in the specified column


        :param col:int: column number where the player wants to play
        :return:dict: - 'success' (bool): True if move was valid and executed, False otherwise
                     - 'message' (str): Human-readable description of the result
        """
        if self.game_over:
            return {'success': False, 'message': 'Game Over'}

        try :
            row= self.board.drop_piece(col,self.current_player)
        except OutOfBoundsException as e:
            return {'success': False, 'message': str(e)}
        except ColumnFilledException as e:
            return {'success': False, 'message': str(e)}

        #check win
        winner=self.board.check_winner()
        if winner != 0:
            self.game_over = True
            self.winner=winner
            return {'success': True, 'message': f'Player {winner} won!'}

        #check draw
        if self.board.is_full():
            self.game_over = True
            return {'success': True, 'message': 'Draw!'}

        #switch player
        self.current_player = 3-self.current_player # 1->2,  2->1
        return {'success': True, 'message': f'Move Successful'}

    def get_computer_move(self):
        """
        function that checks which computer mode is playing and then call
        the corresponding functions
        :return: int : number of the column to play
        """
        if self.use_minimax and self.minimax_ai:
            return self.minimax_ai.get_best_move(self.board)
        else:
            return self._get_basic_ai_move()

    def _get_basic_ai_move(self):
        """
        a function for the basic ai computer moves that place the discs
        in a systematic way and provide us with the basic moves
        win when possible and block if you cant win and always play center columns

        :return:int: number of the col for the best move and a random one if
        could not choose the best move
        """
        #try to win
        for col in range(self.board.cols):
            if self._is_winning_move(col,2):
                return col

        # try to block
        for col in range(self.board.cols):
            if self._is_winning_move(col,1):
                return col

        #prefer center columns
        available =[c for c in range(self.board.cols) if not self.board.is_column_full(c)]
        center_order=[3,2,4,1,5,0,6]
        for col in center_order:
            if col in available:
                return col

        return rnd.choice(available)

    def _is_winning_move(self,col,player):
        """
        a function that checks if a column wins by move simulation

        :param col: int: number of the column that we want to check for
        :param player: int: number of the player that we want to check for
        :return: boolean:True if placing a piece in col would win for player, False otherwise
        """
        if self.board.is_column_full(col):
            return False

        # simulate move
        try:
            row= self.board.drop_piece(col,player)
        except OutOfBoundsException as e:
            return f'Error: {e}'
        except ColumnFilledException as e:
            return f'Error: {e}'

        winner=self.board.check_winner()

        #undo the move
        self.board.grid[row][col]=0

        return winner==player

