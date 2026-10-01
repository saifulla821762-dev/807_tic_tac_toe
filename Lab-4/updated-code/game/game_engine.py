"""GameEngine for a solo Tic-Tac-Toe match against the computer."""

from game.rules import check_winner, is_board_full
from game.renderer import board_pos_to_cell
from game.ai import choose_move

HUMAN_SYMBOL = 'X'
COMPUTER_SYMBOL = 'O'


class GameEngine:
    def __init__(self):
        self.score = {'X': 0, 'O': 0, 'draws': 0}
        self.starting_player = HUMAN_SYMBOL
        self._start_round()

    def _start_round(self):
        self.board = [[None] * 3 for _ in range(3)]
        self.current_player = self.starting_player
        self.round_over = False
        self.winner = None
        self._maybe_take_computer_turn()

    def restart_round(self):
        """Start a clean round while preserving the match scoreboard."""
        self._start_round()

    def reset_match(self):
        """Clear the scoreboard and start a new round."""
        self.score = {'X': 0, 'O': 0, 'draws': 0}
        self._start_round()

    def handle_click(self, pos):
        if self.round_over or self.current_player != HUMAN_SYMBOL:
            return
        cell = board_pos_to_cell(pos)
        if cell is None:
            return
        row, col = cell
        if self.board[row][col] is not None:
            return
        self.board[row][col] = HUMAN_SYMBOL
        self.check_round_end()
        if not self.round_over:
            self.current_player = COMPUTER_SYMBOL
            self._maybe_take_computer_turn()

    def _maybe_take_computer_turn(self):
        if self.round_over or self.current_player != COMPUTER_SYMBOL:
            return
        move = choose_move(self.board)
        if move is None:
            return
        row, col = move
        self.board[row][col] = COMPUTER_SYMBOL
        self.check_round_end()
        if not self.round_over:
            self.current_player = HUMAN_SYMBOL

    def handle_keydown(self, key):
        import pygame
        if key == pygame.K_x:
            self.starting_player = HUMAN_SYMBOL
        elif key == pygame.K_o:
            self.starting_player = COMPUTER_SYMBOL
        elif key == pygame.K_r:
            self.restart_round()
        elif key == pygame.K_m:
            self.reset_match()

    def check_round_end(self):
        if self.round_over:
            return
        winner = check_winner(self.board)
        if winner:
            self.round_over = True
            self.winner = winner
            self.score[winner] += 1
        elif is_board_full(self.board):
            self.round_over = True
            self.winner = None
            self.score['draws'] += 1

    def draw(self, surface, font, small_font):
        from game import renderer
        renderer.draw_board(surface, self.board)
        turn_label = "Your turn (X)" if self.current_player == HUMAN_SYMBOL else "Computer's turn (O)"
        renderer.draw_text(surface, font, turn_label, (10, 15))
        score_label = f"X: {self.score['X']}   O: {self.score['O']}   Draws: {self.score['draws']}"
        renderer.draw_text(surface, font, score_label, (10, 47))
        renderer.draw_text(
            surface, small_font,
            f"Next starter: {self.starting_player} (press X or O to choose)",
            (10, 80),
        )
        renderer.draw_text(
            surface, small_font, "R: restart round    M: reset match", (10, 101)
        )

        if self.round_over:
            text = f"{self.winner} wins!" if self.winner else "Draw!"
            renderer.draw_banner(surface, font, text)
