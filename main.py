from flask import Flask, request, jsonify
import math
import copy

app = Flask(__name__)
board = [' ' for _ in range(9)]

def preveri_zmagovalca(plosca, igralec):
    zmagovalne_poti = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]
    for pot in zmagovalne_poti:
        if plosca[pot[0]] == plosca[pot[1]] == plosca[pot[2]] == igralec:
            return True
    return False

def je_polno(plosca):
    return all(polje != ' ' for polje in plosca)

def oceni_stanje(plosca):
    if preveri_zmagovalca(plosca, 'O'):
        return 1
    elif preveri_zmagovalca(plosca, 'X'):
        return -1
    else:
        return 0

def minimax(plosca, globina, je_maximizirajoci):
    score = oceni_stanje(plosca)
    if abs(score) == 1 or je_polno(plosca):
        return score, None
    if je_maximizirajoci:
        najboljsa_ocena = -math.inf
        najboljsa_poteza = None
        for i in range(9):
            if plosca[i] == ' ':
                nova_plosca = copy.deepcopy(plosca)
                nova_plosca[i] = 'O'
                ocena, _ = minimax(nova_plosca, globina + 1, False)
                if ocena > najboljsa_ocena:
                    najboljsa_ocena = ocena
                    najboljsa_poteza = i
        return najboljsa_ocena, najboljsa_poteza
    else:
        najboljsa_ocena = math.inf
        najboljsa_poteza = None
        for i in range(9):
            if plosca[i] == ' ':
                nova_plosca = copy.deepcopy(plosca)
                nova_plosca[i] = 'X'
                ocena, _ = minimax(nova_plosca, globina + 1, True)
                if ocena < najboljsa_ocena:
                    najboljsa_ocena = ocena
                    najboljsa_poteza = i
        return najboljsa_ocena, najboljsa_poteza

def robot_poteza(plosca):
    _, poteza = minimax(plosca, 0, True)
    if poteza is None:
        for i in range(9):
            if plosca[i] == ' ':
                return i
    return poteza

@app.route('/move', methods=['POST'])
def move():
    global board
    data = request.get_json()
    if not data or 'move' not in data:
        return jsonify({'error': 'Posredujte potezo v formatu {"move": številka med 1 in 9}'}), 400
    try:
        user_move = int(data['move'])
    except ValueError:
        return jsonify({'error': 'Poteza mora biti številka'}), 400
    if user_move < 1 or user_move > 9:
        return jsonify({'error': 'Številka mora biti med 1 in 9'}), 400
    index = user_move - 1
    if board[index] != ' ':
        return jsonify({'error': 'Polje je že zasedeno'}), 400
    board[index] = 'X'
    if preveri_zmagovalca(board, 'X'):
        state = {
            'board': board,
            'message': 'Človek je zmagal!',
            'winner': 'X'
        }
        return jsonify(state)
    if je_polno(board):
        state = {
            'board': board,
            'message': 'Igra je končana z neodločeno izidom',
            'winner': None
        }
        return jsonify(state)
    robot_index = robot_poteza(board)
    board[robot_index] = 'O'
    if preveri_zmagovalca(board, 'O'):
        state = {
            'board': board,
            'message': f'Robot je naredil potezo {robot_index + 1} in zmagal!',
            'robot_move': robot_index + 1,
            'winner': 'O'
        }
        return jsonify(state)
    if je_polno(board):
        state = {
            'board': board,
            'message': f'Robot je naredil potezo {robot_index + 1}. Igra je neodločena.',
            'robot_move': robot_index + 1,
            'winner': None
        }
        return jsonify(state)
    state = {
        'board': board,
        'message': f'Robot je naredil potezo {robot_index + 1}.',
        'robot_move': robot_index + 1,
        'winner': None
    }
    return jsonify(state)

@app.route('/reset', methods=['POST'])
def reset():
    global board
    board = [' ' for _ in range(9)]
    return jsonify({'message': 'Igra je resetirana.', 'board': board})

if __name__ == '__main__':
    app.run(debug=True)
