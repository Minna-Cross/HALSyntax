import random

class KnucklebonesGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        """Reset the game to its initial state."""
        self.player1_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.player2_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.turn = 1  # Reset the turn counter

    def roll_dice(self):
        return random.randint(1, 6)

    def display_grids_with_scores(self):
        print(f"\nTurn {self.turn}:\n")

        # Display Player 2's grid first
        print("Player 2:")
        for row in self.player2_grid:
            print('| ' + ' | '.join([str(x) if x != 0 else ' ' for x in row]) + ' |')

        # Separator line for grid
        print("-------------")

        # Display Player 2's column scores
        player2_column_scores = self.calculate_column_scores(self.player2_grid)
        total_player2_score = sum(player2_column_scores)
        # Print column scores aligned under the columns
        print("  " + '   '.join([str(score) for score in player2_column_scores]))
        print(f"Total Score: {total_player2_score}\n")

        # Display Player 1's grid
        print("Player 1:")
        for row in self.player1_grid:
            print('| ' + ' | '.join([str(x) if x != 0 else ' ' for x in row]) + ' |')

        # Separator line for grid
        print("-------------")

        # Display Player 1's column scores
        player1_column_scores = self.calculate_column_scores(self.player1_grid)
        total_player1_score = sum(player1_column_scores)
        # Print column scores aligned under the columns
        print("  " + '   '.join([str(score) for score in player1_column_scores]))
        print(f"Total Score: {total_player1_score}")

    def calculate_column_scores(self, grid):
        """Calculate and return the scores for each column."""
        column_scores = []
        for col in range(3):
            col_values = [grid[row][col] for row in range(3) if grid[row][col] != 0]
            column_scores.append(self.calculate_column_score(col_values))
        return column_scores

    def calculate_column_score(self, col_values):
        """Score a column by multiplying matching dice together."""
        score = 0
        dice_counts = {}

        # Count the occurrences of each die value in the column
        for value in col_values:
            if value in dice_counts:
                dice_counts[value] += 1
            else:
                dice_counts[value] = 1

        # Multiply matching dice and sum the total score for the column
        for value, count in dice_counts.items():
            score += value * count ** 2  # Multiply value by how many dice of that value are in the column

        return score

    def column_is_full(self, grid, column):
        """Check if the given column in the grid is full (no zeroes)."""
        return all(row[column] != 0 for row in grid)

    def grid_is_full(self, grid):
        """Check if the entire grid is full."""
        return all(all(cell != 0 for cell in row) for row in grid)

    def place_die(self, grid, column, value):
        """Place the die in the first available row of the given column."""
        for i in range(3):
            if grid[i][column] == 0:
                grid[i][column] = value
                break

    def destroy_opponent_die(self, opponent_grid, column, value):
        """Destroy all opponent's dice in the same column if the value matches and roll up the remaining dice."""
        destroyed = False
        
        # Destroy the matching dice (set them to 0)
        for i in range(3):
            if opponent_grid[i][column] == value:
                opponent_grid[i][column] = 0
                destroyed = True

        # Roll up the remaining dice in the column (shift non-zero values upward)
        if destroyed:
            print(f"Destroyed all opponent's dice with value {value} in column {column+1}")
            self.roll_up_column(opponent_grid, column)

    def roll_up_column(self, grid, column):
        """Shift the non-zero values in the column upward."""
        non_zero_values = [grid[row][column] for row in range(3) if grid[row][column] != 0]
        
        # Set the entire column to 0 first
        for row in range(3):
            grid[row][column] = 0
        
        # Place the non-zero values back into the column from the top
        for i, value in enumerate(non_zero_values):
            grid[i][column] = value

    def calculate_score(self, grid):
        """Calculate the total score of the grid based on column scores."""
        score = 0
        for col in range(3):
            col_values = [grid[row][col] for row in range(3) if grid[row][col] != 0]
            
            if col_values:
                score += self.calculate_column_score(col_values)
        
        return score

    def check_grid_full(self, grid):
        return self.grid_is_full(grid)

    def play_turn(self):
        current_player = 1 if self.turn % 2 != 0 else 2
        print(f"\nPlayer {current_player}'s Turn")

        dice_value = self.roll_dice()
        print(f"Player {current_player} rolled a {dice_value}")

        # Ask for a valid column (column must not be full)
        while True:
            column_input = input("Select a column (1, 2, or 3): ")
            
            # Check if the input is numeric and within range
            if not column_input.isdigit() or not (1 <= int(column_input) <= 3):
                print("Invalid column. Please choose 1, 2, or 3.")
                continue
            
            column = int(column_input) - 1  # Adjust to 0-based index

            if current_player == 1:
                if self.column_is_full(self.player1_grid, column):
                    print(f"Column {column+1} is full. Choose another column.")
                else:
                    break
            else:
                if self.column_is_full(self.player2_grid, column):
                    print(f"Column {column+1} is full. Choose another column.")
                else:
                    break

        # Place the die and destroy opponent's die if the same value exists in the same column
        if current_player == 1:
            self.place_die(self.player1_grid, column, dice_value)
            self.destroy_opponent_die(self.player2_grid, column, dice_value)
        else:
            self.place_die(self.player2_grid, column, dice_value)
            self.destroy_opponent_die(self.player1_grid, column, dice_value)

        # Display the grids with column scores after the move
        self.display_grids_with_scores()

        # Check if either grid is full to end the game
        if self.grid_is_full(self.player1_grid):
            print("Player 1's grid is full! Ending game.")
            self.end_game()
        elif self.grid_is_full(self.player2_grid):
            print("Player 2's grid is full! Ending game.")
            self.end_game()
        else:
            self.turn += 1

    def end_game(self):
        player1_score = self.calculate_score(self.player1_grid)
        player2_score = self.calculate_score(self.player2_grid)

        print(f"\nFinal Scores:")
        print(f"Player 1's Score: {player1_score}")
        print(f"Player 2's Score: {player2_score}")

        if player1_score > player2_score:
            print("Player 1 wins!")
        elif player2_score > player1_score:
            print("Player 2 wins!")
        else:
            print("It's a tie!")

        # Ask if the player wants to play again
        while True:
            play_again = input("Would you like to play again? (yes/y or no/n): ").lower().strip()
            if play_again in ["yes", "y"]:
                print("Starting a new game!")
                self.reset_game()  # Reset the game state
                self.play_game()   # Start a new game
            elif play_again in ["no", "n"]:
                print("Thanks for playing!")
                exit(0)
            else:
                print("Invalid input. Please answer with 'yes/y' or 'no/n'.")

    def play_game(self):
        print("Welcome to Knucklebones!")
        while True:
            self.play_turn()

# To start the game:
game = KnucklebonesGame()
game.play_game()
