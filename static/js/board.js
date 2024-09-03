document.addEventListener('DOMContentLoaded', function() {
    // Establish connection with the Flask-SocketIO server
    const socket = io();

    // Selected color state
    let selectedColor = '#000000';

    // Store the board data in a globally accessible variable
    let board = [];

    // Update selected color when the user picks a new color
    document.getElementById('colorPicker').addEventListener('input', (event) => {
        selectedColor = event.target.value;
        console.log('Selected color:', selectedColor);
    });

    // Function to extract the board ID from the URL
    function getBoardIdFromUrl() {
        const pathArray = window.location.pathname.split('/');
        return pathArray[pathArray.length - 1];
    }

    // Handle successful connection
    socket.on('connected', (data) => {
        console.log(data.message);
        
        // Get the board ID from the URL and join the board
        const boardId = getBoardIdFromUrl();
        if (boardId) {
            joinBoard(boardId);
        } else {
            console.error('Board ID not found in the URL.');
        }
    });

    // Handle join success and render the board
    socket.on('join_success', (data) => {
        console.log(data.message);

        // Store the 2D board array in the global `board` variable
        board = data.board;
        if (Array.isArray(board)) {
            renderBoard(board);
        } else {
            console.error('Board data is not a valid 2D array.');
        }
    });

    // Handle cell update broadcast from the server
    socket.on('cell_updated', (data) => {
        console.log('Cell updated:', data);
        const { row, col, color } = data;

        // Update the specific cell on the client-side
        const boardContainer = document.getElementById('boardContainer');
        const cell = boardContainer.children[row * board[0].length + col];
        if (cell) {
            cell.style.backgroundColor = color;
            // Update the board array with the new color
            board[row][col] = color;
        }
    });

    // Handle errors
    socket.on('error', (data) => {
        console.log(data.message);
    });

    // Function to join the board using the boardId
    function joinBoard(boardId) {
        if (boardId) {
            socket.emit('join', { board_id: boardId });
        } else {
            console.error('Board ID is required to join a board.');
        }
    }

    // Function to render the board on the client
    function renderBoard(board) {
        console.log('Rendering board:', board);

        const boardContainer = document.getElementById('boardContainer');
        const height = board.length;
        const width = board[0].length;

        // Set grid dimensions
        boardContainer.style.gridTemplateColumns = `repeat(${width}, 20px)`;
        boardContainer.style.gridTemplateRows = `repeat(${height}, 20px)`;

        // Clear any existing content
        boardContainer.innerHTML = '';

        // Iterate through the 2D array and render each cell
        for (let row = 0; row < height; row++) {
            for (let col = 0; col < width; col++) {
                const cell = document.createElement('div');
                cell.style.width = '20px';
                cell.style.height = '20px';
                cell.style.backgroundColor = board[row][col];

                // Add a click event to send the cell's row, column, and color to the server
                cell.addEventListener('click', () => {
                    console.log(`Clicked cell at row: ${row}, column: ${col}`);
                    // Send the information to the server
                    socket.emit('cell_update', {
                        board_id: getBoardIdFromUrl(),
                        row: row,
                        col: col,
                        color: selectedColor
                    });
                });

                boardContainer.appendChild(cell);
            }
        }
    }

    // Event listener for the copy button
    document.getElementById('copyBoardIdButton').addEventListener('click', () => {
        const boardId = getBoardIdFromUrl();
        if (boardId) {
            navigator.clipboard.writeText(boardId).then(() => {
                console.log('Board ID copied to clipboard:', boardId);
            }).catch(err => {
                console.error('Failed to copy Board ID:', err);
            });
        } else {
            console.error('Board ID not found in the URL.');
        }
    });
});
