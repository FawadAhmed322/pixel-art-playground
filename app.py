from flask import Flask, request, jsonify, render_template, abort
from flask_socketio import SocketIO, emit, join_room
import uuid

app = Flask(__name__)
socketio = SocketIO(app)

boards = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-board', methods=['GET'])
def create_board():
    height = request.args.get('height', type=int)
    width = request.args.get('width', type=int)
    
    if height is None or width is None:
        abort(400, description="Height and width parameters are required")

    board = [["#FFFFFF" for _ in range(width)] for _ in range(height)]
    board_id = str(uuid.uuid4())
    boards[board_id] = board

    return jsonify({"board_id": board_id}), 201

@app.route('/board/<board_id>', methods=['GET'])
def board(board_id):
    if board_id not in boards:
        return jsonify({"error": "Board not found"}), 404
    
    return render_template('board.html', board_id=board_id)

@socketio.on('connect')
def on_connect():
    emit('connected', {'message': 'Successfully Connected'})

@socketio.on('join')
def on_join(data):
    board_id = data['board_id']
    
    if board_id not in boards:
        emit('error', {'message': 'Board not found'})
        return

    join_room(board_id)
    board_data = boards[board_id]
    emit('join_success', {'message': f'You have joined the board {board_id}', 'board': board_data})

@socketio.on('cell_update')
def handle_cell_update(data):
    board_id = data['board_id']
    row = data['row']
    col = data['col']
    color = data['color']
    
    if board_id in boards:
        # Update the board with the new color
        boards[board_id][row][col] = color
        
        # Emit the updated cell to all clients in the room
        emit('cell_updated', {
            'board_id': board_id,
            'row': row,
            'col': col,
            'color': color
        }, room=board_id)
    else:
        emit('error', {'message': 'Board not found'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
