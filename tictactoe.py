import json
import random
from abc import abstractmethod
import click


class TicTacToe(object):

    def __init__(self, player_x, player_o):
        self.board = [' '] * 9
        self.player_x = player_x
        self.player_o = player_o
        self.player_x.game = self
        self.player_o.game = self
        self.player_x_turn = random.choice([True, False])

    def play(self):
        self.player_x.start_game()
        self.player_o.start_game()
        while True:
            if self.player_x_turn:
                player, char, other_player = self.player_x, 'X', self.player_o
            else:
                player, char, other_player = self.player_o, 'O', self.player_x
            if isinstance(player, HumanPlayer):
                self.display_board()
            space = player.move(self.board) - 1  # Subtract to get 0 based index
            self.board[space] = char
            if self.winner(char):
                player.reward(1, self.board)
                other_player.reward(-1, self.board)
                break
            if self.board_full():
                player.reward(.5, self.board)
                other_player.reward(.5, self.board)
                break
            other_player.reward(0, self.board)
            self.player_x_turn = not self.player_x_turn

    def winner(self, char):
        # All possible winning combinations
        for a, b, c in [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),
                        (0, 4, 8), (2, 4, 6)]:
            if char == self.board[a] == self.board[b] == self.board[c]:
                return True
        return False

    def board_full(self):
        return not any([space == ' ' for space in self.board])

    def display_board(self):
        row = " {} | {} | {}"
        hr = "\n-----------\n"
        print hr.join([row] * 3).format(*self.board)


class Player(object):
    @abstractmethod
    def start_game(self):
        pass

    @abstractmethod
    def move(self, board):
        pass

    @abstractmethod
    def reward(self, value, board):
        pass

    @staticmethod
    def available_moves(board):
        return [i + 1 for i in range(0, len(board)) if board[i] == ' ']


class HumanPlayer(Player):

    def start_game(self):
        pass

    def move(self, board):
        actions = self.available_moves(board)
        while True:
            try:
                print("Available Moves: {}".format(",".join(map(str, actions))))
                new_move = int(raw_input("Your move? "))
            except ValueError:
                continue
            if new_move not in actions:
                print("That move is not allowed. Please enter a different value.")
                continue
            break
        return new_move

    def reward(self, value, board):
        print "{} rewarded: {}".format(self.__class__.__name__, value)


class QLearningPlayer(Player):
    def __init__(self, q=None, epsilon=0.2, alpha=0.3, gamma=0.95):
        if q is None:
            self.q = {}
        else:
            self.q = q
        self.epsilon = epsilon  # chance of random exploration
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # discount factor for future rewards
        self.state = '         '
        self.action = None

    def start_game(self):
        self.state = '         '
        self.action = None

    def get_q(self, state, action):
        key = '{}:{}'.format(state, action)
        if self.q.get(key) is None:
            self.q[key] = 1.0
        return self.q.get(key)

    def move(self, board):
        self.state = "".join(board)
        actions = self.available_moves(board)

        # Explore the space
        if random.random() < self.epsilon:
            self.action = random.choice(actions)
            return self.action

        qs = [self.get_q(self.state, a) for a in actions]
        max_q = max(qs)

        if qs.count(max_q) > 1:
            # If multiple best options, choose one randomly
            best_options = [i for i in range(len(actions)) if qs[i] == max_q]
            i = random.choice(best_options)
        else:
            i = qs.index(max_q)

        self.action = actions[i]
        return actions[i]

    def reward(self, value, board):
        if self.action:
            self.learn(self.state, self.action, value, "".join(board))

    def learn(self, state, action, reward, result_state):
        prev = self.get_q(state, action)
        new_max_q = max([self.get_q(result_state, a) for a in self.available_moves(state)])
        key = '{}:{}'.format(state, action)
        self.q[key] = prev + self.alpha * ((reward + self.gamma * new_max_q) - prev)

    def save_q(self, filename):
        with open(filename, 'w') as f:
            f.write(json.dumps(self.q))

    @classmethod
    def load_q_from_file(cls, filename, epsilon=0.2, alpha=0.3, gamma=0.95):
        with open(filename, 'r') as f:
            q = json.loads(f.read())
        return cls(q=q, epsilon=epsilon, alpha=alpha, gamma=gamma)


@click.command()
@click.option('--training_iterations', prompt='Training Iterations', type=click.INT)
@click.option('--filename', default="", prompt="Filename", help='path to JSON file to store Q values')
@click.option('--save_learner', default=False, prompt="Save Learner?")
@click.option('--load_learner', default=False, prompt="Load Learner?")
def main(training_iterations, filename, save_learner, load_learner):
    p1 = QLearningPlayer()
    if load_learner and filename:
        p2 = QLearningPlayer.load_q_from_file(filename)
    else:
        p2 = QLearningPlayer()

    for i in xrange(training_iterations):
        t = TicTacToe(p1, p2)
        t.play()

    if save_learner and filename:
        p2.save_q(filename)

    p1 = HumanPlayer()

    while True:
        t = TicTacToe(p1, p2)
        t.play()

if __name__ == "__main__":
    main()
