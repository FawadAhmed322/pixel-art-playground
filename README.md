
# Pixel Art Playground

**Pixel Art Playground** is an interactive web application that allows users to create pixel art collaboratively in real-time. This application uses Flask and Flask-SocketIO to manage the server and WebSocket connections, enabling a seamless and engaging user experience.

## Features

- **Real-Time Collaboration**: Multiple users can create pixel art simultaneously on the same canvas.
- **Responsive Interface**: The interface is designed to work smoothly across different devices.
- **WebSocket Communication**: Fast and efficient communication using WebSockets for real-time updates.
- **Customizable Canvas**: Users can select colors and paint pixels on a shared canvas.

## Technologies Used

- **Python**
  - `Flask` for serving the web application.
  - `Flask-SocketIO` for managing real-time communication.
  - `Websockets` for handling WebSocket connections.
- **HTML/CSS/JavaScript**: Frontend technologies used to create the user interface.
- **Socket.IO**: Enables real-time, bi-directional communication between the server and clients.

## Installation

To get a local copy up and running, follow these steps:

### Prerequisites

Ensure you have Python installed on your machine. You can check by running:

```bash
python --version
```

### Installation Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/fawadahmed322/pixel-art-playground.git
   cd pixel-art-playground
   ```

2. **Install required Python packages**:

   You can install the dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:

   Start the Flask application by running:

   ```bash
   python app.py
   ```

4. **Access the application**:

   Open your web browser and go to `http://localhost:5000`.

## Usage

- **Create Art**: Use the interactive canvas to create pixel art by clicking on the squares.
- **Collaborate**: Invite friends to join and collaborate on the same canvas in real-time.
- **Reset Canvas**: Clear the canvas to start fresh at any time.

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Acknowledgements

- Special thanks to all contributors and the open-source community for their invaluable tools and libraries.
