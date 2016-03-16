import collections
import random

class Domino:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def inverted(self):
        return Domino(self.second, self.first)

    def point_sum(self):
        return self.first + self.second

    def is_double(self):
        return self.first == self.second

    def __str__(self):
        return '[{0}|{1}]'.format(self.first, self.second)

    def __eq__(self, other):
        return (self.first, self.second) == (other.first, other.second) \
            or (self.first, self.second) == (other.second, other.first)

    def __ge__(self, other):
        return self.point_sum() >= other.point_sum()

    def __le__(self, other):
        return self.point_sum() <= other.point_sum()

    def __ne__(self, other):
        return not self == other

    def __contains__(self, key):
        return key == self.first or key == self.second

class Board:
    def __init__(self):
        self.board = collections.deque()

    def left_end(self):
        if not self.board:
            return None
        return self.board[0].first

    def right_end(self):
        if not self.board:
            return None
        return self.board[-1].second

    def ends(self):
        return self.left_end(), self.right_end()

    def add_left(self, domino):
        if not self.board or domino.second == self.left_end():
            self.board.appendleft(domino)
        elif domino.first == self.left_end():
            self.board.appendleft(domino.inverted())
        else:
            raise Exception('{0} cannot be added to the left of'
                            ' the board- numbers do not match!'.format(domino))

    def add_right(self, domino):
        if not self.board or domino.first == self.right_end():
            self.board.append(domino)
        elif domino.second == self.right_end():
            self.board.append(domino.inverted())
        else:
            raise Exception('{0} cannot be added to the right of'
                            ' the board- numbers do not match!'.format(domino))

    def __len__(self):
        return len(self.board)

    def __str__(self):
        return ''.join([str(domino) for domino in self.board])

class Player:
    # hand is an array of dominos
    def __init__(self, strategy):
        self.hand = []
        self.strategy = strategy

        #for certain strategies, we record teammate and opponent moves
        self.tm_has_played = []
        self.opp_has_played = []

    def has_empty_hand(self):
        return not self.hand

    def remaining_pts(self):
        return sum([domino.point_sum() for domino in self.hand])

    def select_move(self, board):
        moves = self.valid_moves(board)
        if not moves:
            return None
        else:
            return behaviors[self.strategy](self, moves)

    def valid_moves(self, board):
        #return all if all are valid
        if not board:
            return self.hand

        moves = []
        left_end, right_end = board.ends()

        for domino in self.hand:
            if left_end in domino or right_end in domino:
                moves.append(domino)

        return moves

############# Below are the Player Strategies available #############

    def greedy(self, moves):
        return max(moves)

    def defensive(self, moves):
        best = moves[0]
        for domino in moves:
            if domino.is_double():
                return domino

        return self.greedy(moves)

    def reverse_greedy(self, moves):
        return min(moves)

    def random(self, moves):
        return random.choice(moves)

    def cooperative(self, moves):
        best = moves[0]
        updated = False

        for domino in moves:
            for team_domino in self.tm_has_played:
                if team_domino.first in domino or team_domino.second in domino:
                    if domino.is_double():
                        return domino
                    elif domino >= best:
                        best = domino
                        updated = True
        if updated is True:
            return best
        else:
            return self.random(moves)

    def offensive(self, moves):
        best = moves[0]
        updated = False

        for domino in moves:
            for opp_d in self.opp_has_played:
                if domino.first in opp_d or domino.second in opp_d:
                    pass
                else:
                    if domino.is_double() is True:
                        return domino
                    elif (domino >= best):
                        best = domino
                        updated = True

        if updated is True:
            return best
        else:
            return self.random(moves)

    def __str__(self):
        return ''.join([str(domino) for domino in self.hand])

behaviors = {  1: Player.random,
               2: Player.greedy,
               3: Player.defensive,
               4: Player.reverse_greedy,
               5: Player.cooperative,
               6: Player.offensive,
               'random': Player.random,
               'greedy': Player.greedy,
               'defensive': Player.defensive,
               'reverse_greedy': Player.reverse_greedy,
               'cooperative': Player.cooperative,
               'offensive': Player.offensive
}

########################## Game Class #####################################
## responsible for commiting moves to the board, determining a stuck board,
## and assigning hands at the beginning of a game.

class Game:
    def __init__(self, starting_player=0, starting_dom=None):

        self.board = Board()
        self.turn = starting_player
        self.starting_dom = starting_dom

        self.is_stuck = False
        self.pass_counter = 0

    def randomized_hands(self):
        dominos = [Domino(i, j) for i in range(7) for j in range(i, 7)]
        random.shuffle(dominos)
        return dominos[0:7], dominos[7:14], dominos[14:21], dominos[21:28]

    # return false if the game is not over
    def commit_move(self, domino_move):
        if not self.board:
            self.board.add_right(domino_move)
            return False

        left_end, right_end = self.board.ends()

        if domino_move is not None:
            if left_end in domino_move:
                self.board.add_left(domino_move)
            elif right_end in domino_move:
                self.board.add_right(domino_move)
            self.pass_counter = 0

        else:
            if self.pass_counter == 4:
                self.is_stuck = True
                return True
            else:
                self.pass_counter += 1
                return False

        return False


###########################################################
## Runner utilities - could make a class, but there is no
##      data besides score that has to be preserved across
##      multiple series (and these data are just local variables
##      in the global run() ), so there's not a clear point of a 
##      new class.
##      It is at this level that the player and game classes
##      are accessible simultaneously
##                  Architecture:
##                      run() --> run_series() --> run_game() --> end_game()

def run_series(players):
    scores = [0,0]
    new_game = Game(starting_dom=Domino(6, 6))

    while max(scores) < 200:
        game_result = run_game(players, new_game)

        last_mover, game_score = game_result
        scores[0] += game_score[0]
        scores[1] += game_score[1]
        new_game = Game(starting_player=last_mover)

    return scores

def run_game(players, game):
    init_hands(players, game)

    if game.starting_dom is not None:
        find_first(players, game)

    done = False
    while not done:
        move = players[game.turn].select_move(game.board)
        if move is not None:
            players_observe(players, game.turn, move)
            players[game.turn].hand.remove(move)
        game.commit_move(move)
        done = players[game.turn].has_empty_hand() or game.is_stuck
        if not done:
            game.turn = (game.turn + 1) % 4


    if game.pass_counter == 3:
        return end_stuck_game(players, game)
    else:
        return end_game(players, game)

## players observe - adds a move to player's set of opp/tm moves
## used for cooperative and offensive strategies 
def players_observe(players, turn, move):
    players[(turn + 2) % 4].tm_has_played.append(move)
    players[(turn + 1) % 4].opp_has_played.append(move)
    players[(turn + 3) % 4].opp_has_played.append(move)

def end_game(players, game):
    winning_team = game.turn % 2
    game_score = [0,0]
    for player in players:
        game_score[winning_team] += player.remaining_pts()

    return [game.turn, game_score]

def end_stuck_game(game, players):
    x = players[0].remaining_pts() + players[2].remaining_pts()
    y = players[1].remaining_pts() + players[3].remaining_pts()
    game_score = []

    if x == y:
        game_score = [0,0]
    if x < y:
        game_score = [x+y,0]    
    if x > y:
        game_score = [0,x+y]

    return [game.turn, game_score]

def init_hands(players, game):       
    hands = game.randomized_hands()
    for x in range (0,4):
        players[x].hand = hands[x]

def find_first(players, game):
    p_index = 0
    for player in players:
        for domino in player.hand:
            if domino == game.starting_dom:
                game.commit_move(game.starting_dom)
                player.hand.remove(game.starting_dom)
                game.turn = (p_index + 1) % 4
                break
        p_index += 1

def run(behaviors, set_length):
    players = []
    for x in range(0, 4):
        players.append(Player(behaviors[x]))

    win_counts = [0,0]

    for x in range (0, set_length):
        series_score = run_series(players)

        if(series_score[0] > series_score[1]):
            win_counts[0] +=1
        else:
            win_counts[1] +=1

    return win_counts




