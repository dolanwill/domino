import collections
import random
import json


# added sum and double functions, and operator overloads, for later use in
# preferential strategies
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
        return (self.point_sum() >= other.point_sum())

    def __le__(self, other):
        return (self.point_sum() <= other.point_sum())

    def __ne__(self, other):
        return not self == other

    def __contains__(self, key):
        return key == self.first or key == self.second

class Board:
    def __init__(self):
        self.board = collections.deque()

    def left_end(self):
        if len(self.board) == 0:
            return None
        return self.board[0].first

    def right_end(self):
        if len(self.board) == 0:
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
                            ' the board - numbers do not match!'.format(domino))

    def add_right(self, domino):
        if not self.board or domino.first == self.right_end():
            self.board.append(domino)
        elif domino.second == self.right_end():
            self.board.append(domino.inverted())
        else:
            raise Exception('{0} cannot be added to the right of'
                            ' the board -numbers do not match!'.format(domino))

    def __len__(self):
        return len(self.board)

    def __str__(self):
        return ''.join([str(domino) for domino in self.board])

class Player:
    # hand is an array of dominos
    def __init__(self, hand, attribute=0):
        self.hand = hand
        self.attribute = attribute
        self.behaviors = { 1: self.random,
                           2 : self.greedy,
                           3 : self.defensive,
                           "random": self.random,
                           "greedy": self.greedy,
                           "defensive": self.defensive
        }

    def has_empty_hand(self):
        has = bool(len(self.hand))
        return not has

    def remaining_pts(self):
        player_points = 0
        for domino in self.hand:
            player_points += domino.point_sum()
        return player_points

    def print_hand(self):
        for domino in self.hand:
            print domino

    # for first move of game, they'll be -1,-1
    def valid_moves(self, left_end, right_end):
        #return all if all are valid
        if (left_end is None and right_end is None):
            return [domino for domino in self.hand]

        moves = []

        for domino in self.hand:
            if left_end in domino:
                moves.append(domino)
            elif right_end in domino:
                moves.append(domino)

        return moves

    def move_selection(self, moves):
        if(len(moves) == 0):
            return None
        else:
            return self.behaviors[self.attribute](moves)

    def greedy(self, dominos):
        best = Domino(0,0)
        for domino in dominos:
            if domino >= best:
                best = domino
                print "critical decision made!"
        return best

    def defensive(self, dominos):
        best = dominos[0]
        for domino in dominos:
            if (domino.is_double() is True):
                print "critical decision made! double found."
                return domino
            elif (domino >= best):
                best = domino
        return best

    def random(self, dominos):
        return dominos[0]

    def __str__(self):
        return ''.join([str(domino) for domino in self.board])



class Game:
    def __init__(self, starting_player=0, starting_dom=None, team_attrs=[0,0]):
        print "GAME: STARTING DOMINO ="
        print starting_dom

        self.board = Board()
        # generate players
        self.players = []
        self.init_players(team_attrs)
        self.turn_index = starting_player

        self.scores = [0,0]
        self.turn_number = 0
        self.turn = self.players[starting_player]

        if starting_dom is None:
            self.turn = self.players[starting_player]
        else:
            for player in self.players:
                    if starting_dom in player.hand:
                        self.turn = player
                        self.commit_move(player, starting_dom)
                        break
                    else:
                        self.turn_index += 1
            
    def init_players(self, team_attrs):
        hands = self.randomized_hands()
        attr_index = 0
        for hand in hands:
            self.players.append(Player(hand, team_attrs[attr_index % 2]))
            print "adding player with attribute {0}".format(team_attrs[attr_index%2])
            attr_index += 1
        self.print_player_hands()

    def randomized_hands(self):
        dominos = [Domino(i, j) for i in range(7) for j in range(i, 7)]
        random.shuffle(dominos)
        return dominos[0:7], dominos[7:14], dominos[14:21], dominos[21:28]

    def print_player_hands(self):
        for x in range(0, 4):
            print "player %d" % (x) 
            self.players[x].print_hand()

    def run_game(self):
        done = False
        while(done is False):
            done = self.new_move(self.turn)

    #new/commit move:
    # return false if the game is not over
    # return true if the game is over in some way
    def new_move(self, curr_player):
        left_end, right_end = self.board.ends()

        moves = curr_player.valid_moves(left_end, right_end)
        domino_move = curr_player.move_selection(moves)
        return self.commit_move(curr_player, domino_move)

    def commit_move(self, curr_player, domino_move):
        print "adding move {0}! domino is {1}".format(self.turn_number, domino_move)
        self.turn_number += 1
        if not self.board:
            self.board.add_right(domino_move)
            curr_player.hand.remove(domino_move)
            self.turn_index = (self.turn_index + 1) % 4
            self.turn = self.players[self.turn_index]
            return False

        left_end, right_end = self.board.ends()

        if domino_move is not None:
            if (left_end in domino_move or left_end == None):
                self.board.add_left(domino_move)
            elif right_end in domino_move:
                self.board.add_right(domino_move)
            
            curr_player.hand.remove(domino_move)

            if (curr_player.has_empty_hand() is True):
                print len(curr_player.hand)
                print "empty hand!"
                #self.print_player_hands()
                self.end_game()
                return True
            else:
                self.turn_index = (self.turn_index + 1) % 4
                self.turn = self.players[self.turn_index]
                return False
        else:
            if (self.is_stuck()):
                print "board stuck!"
                #self.print_player_hands()
                self.end_stuck_game()
                return True
            else:
                self.turn_index = (self.turn_index + 1) % 4
                self.turn = self.players[self.turn_index]
                return False

        return False

    def end_game(self):
        print(self.board)
        winning_team = self.turn_index % 2
        losing_team = (self.turn_index + 1) % 2

        for player in self.players:
            self.scores[winning_team] += player.remaining_pts() 
        
    def is_stuck(self):
        if not self.board:
            return False

        left_end, right_end = self.board.ends()
        for player in self.players:
            for domino in player.hand:
                if left_end in domino or right_end in domino:
                    return False

        return True

    def end_stuck_game(self):
        print(self.board)
        self.scores[0] = self.players[0].remaining_pts() + self.players[2].remaining_pts()
        print "scores [0]: {0}".format(self.scores[0])
        self.scores[1] = self.players[1].remaining_pts() + self.players[3].remaining_pts()
        print "scores [1]: {0}".format(self.scores[1])


    def result(self):
        return self.turn_index, self.scores[0], self.scores[1]

class Series:
    def __init__(self, attrs=[0,0], target_score=200):
        self.games = [Game(starting_dom=Domino(6, 6), team_attrs=attrs)]
        self.scores = [0, 0]
        self.target_score = target_score
        self.game_count = 0
        self.attrs = attrs

    def is_over(self):
        return max(self.scores) >= self.target_score

    def run_games(self):

        while(self.is_over() is False):
            game = self.games[self.game_count]
            game.run_game()
            result = game.result()

            last_mover, points0, points1 = result
            print result

            self.scores[0] += points0
            self.scores[1] += points1

            if self.is_over():
                return self.scores

            else:
                self.games.append(Game(starting_player=last_mover,
                                        team_attrs=self.attrs))
                self.game_count += 1
