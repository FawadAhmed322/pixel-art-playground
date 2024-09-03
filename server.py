import asyncio
import json
import uuid
import websockets
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

# Initialize the boards and connections dictionaries
boards = {}
connections = {}

async def broadcast(id):
    board = boards[id]
    for websocket in connections[id]:
        try:
            await websocket.send(json.dumps({"type": "set_board", "board": board}))
        except (ConnectionClosedError, ConnectionClosedOK):
            # Remove disconnected websockets from the connections list
            connections[id].remove(websocket)

async def handle(websocket, path):
    async for message in websocket:
        message = json.loads(message)
        match message['type'].lower():
            case "create_board":
                try:
                    height, width = message["content"]["height"], message["content"]["width"]
                    # Validate height and width
                    if not isinstance(height, int) or not isinstance(width, int) or height <= 0 or width <= 0:
                        raise ValueError("Height and width must be positive integers.")
                    id = str(uuid.uuid4())
                    boards[id] = [["#FFFFFF"] * width for _ in range(height)]
                    connections[id] = []
                    await websocket.send(json.dumps({"type": "create_board", "status": 201, "id": id}))
                except (KeyError, ValueError) as e:
                    # Handle missing or invalid height/width with a single catch-all response
                    await websocket.send(json.dumps({"type": "create_board", "status": 400, "error": str(e)}))
                except Exception as e:
                    # Handle any unexpected errors
                    await websocket.send(json.dumps({"type": "create_board", "status": 500, "error": "Internal server error."}))
            case "connect":
                try:
                    id = message["content"]["id"]
                    if id not in boards:
                        raise KeyError("Board ID does not exist.")
                    connections[id].append(websocket)
                    await websocket.send(json.dumps({"type": "connect", "status": 200, "message": "Logged In"}))
                except (KeyError, ValueError) as e:
                    await websocket.send(json.dumps({"type": "connect", "status": 400, "error": str(e)}))
                except Exception as e:
                    await websocket.send(json.dumps({"type": "connect", "status": 500, "error": "Internal server error."}))
            case "get_board":
                try:
                    id = message["content"]["id"]
                    if id not in boards:
                        raise KeyError("Board ID does not exist.")
                    board = boards[id]
                    await websocket.send(json.dumps({"type": "get_board", "status": 200, "board": board}))
                except (KeyError, ValueError) as e:
                    await websocket.send(json.dumps({"type": "get_board", "status": 400, "error": str(e)}))
                except Exception as e:
                    await websocket.send(json.dumps({"type": "get_board", "status": 500, "error": "Internal server error."}))
            case "set_pixel":
                try:
                    id = message["content"]["id"]
                    if id not in boards:
                        raise KeyError("Board ID does not exist.")
                    board = boards[id]
                    color = message["content"]["color"]
                    row, col = message["content"]["row"], message["content"]["col"]
                    # Validate row, col, and color
                    if not (0 <= row < len(board)) or not (0 <= col < len(board[0])):
                        raise ValueError("Row or column is out of bounds.")
                    if not isinstance(color, str) or not color.startswith("#") or len(color) != 7:
                        raise ValueError("Color must be a valid hex code (e.g., '#FFFFFF').")
                    board[row][col] = color
                    print(f"Row: {row}\nCol: {col}\nColor: {color}")
                    await broadcast(id)
                    # await websocket.send(json.dumps({"type": "set_pixel", "status": 200, "message": "Pixel updated"}))
                except (KeyError, ValueError) as e:
                    await websocket.send(json.dumps({"type": "set_pixel", "status": 400, "error": str(e), "id": message["content"]["id"]}))
                except Exception as e:
                    await websocket.send(json.dumps({"type": "set_pixel", "status": 500, "error": "Internal server error.", "id": message["content"]["id"]}))
            case _:
                await websocket.send(json.dumps({"type": "unknown", "status": 400, "error": "Invalid request type", "echo": json.dumps(message)}))

# Start the WebSocket server
async def main():
    async with websockets.serve(handle, "", 8000):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
