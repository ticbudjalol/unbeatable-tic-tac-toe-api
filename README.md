# Unbeatable-tic-tac-toe-api

This repository contains an implementation of the classic Tic-Tac-Toe game as a REST API built with Flask. In this version, the human player uses the symbol X while the computer (robot) uses O. The computer employs the Minimax algorithm, making it unbeatable when playing optimally.


REST API Endpoints:

- **REST API Endpoints:**
  - **`/move` (POST):**
    - Accepts a JSON payload with the player's move (a number between 1 and 9) and updates the game board accordingly.
    - After processing the human move, the API computes the computer's move and returns the current state of the board along with a message indicating the outcome (win, draw, or game continuation).
  - **`/reset` (POST):**
    - Resets the game board to its initial state, allowing you to start a new game.
  
Game Logic:

The game logic includes checking for win conditions, verifying if the board is full (draw), and implementing the unbeatable Minimax algorithm for the computer's moves.
The code is structured in a straightforward manner, making it easy to understand and extend for educational purposes or further development.

Example of making a move:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"move": 5}' http://127.0.0.1:5000/move
