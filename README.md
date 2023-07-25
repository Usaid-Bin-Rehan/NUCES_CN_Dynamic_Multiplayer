Dots and Boxes application
==========================
This is a simple implementation of the Dots and Boxes game using Javascript & Python. PoC open to contributions.

Overview
------------------

The Dots and Boxes game is a classic pencil-and-paper game for two players. The game is played on a rectangular grid of dots, where each player takes turns connecting two adjacent dots with a horizontal or vertical line. When a player completes a box by connecting its four sides, they get a point and can make another move. The game ends when all boxes are completed, and the player with the most points wins.

This implementation is a web-based version of the game that can be played by two players on different devices connected to the same network.

Requirements
------------------

Python 3.x
Modern web browser (Chrome, Firefox, Safari, etc.)

Usage
------------------

Clone this repository to your local machine.
Open a terminal window and navigate to the project directory.
Run the server by executing the following command: python3 server.py <port>
Replace <port> with the port number you want to use for the server (e.g., 8000).
Open a web browser and navigate to http://<server-ip>:<port>/ to play the game.
Replace <server-ip> with the IP address of the machine running the server.
Replace <port> with the port number you specified in step 3.
Click on the "Connect" button to join the game.
The game requires two players to start playing.
Use the mouse to click on two adjacent dots to create a line.
If the line completes a box, you get a point and can make another move.
Continue playing until all boxes are completed.
The player with the most points at the end of the game wins.


Start the game GUI
------------------

This program shows a web-based GUI to play the Dots and Boxes
game. 
It is a simple Javascript based application that runs entirely in the browser.
You can start it by opening the file `static/dotsandboxes.html` in a browser.
Or alternatively, you can start the app using the included simple server:

    $ ./server.py 8080

The game can then be played by directing your browser to http://127.0.0.1:8080.


Start the client
----------------------

This is the program that runs a game-playing clients
Starting the agent client is done using the following command:

    $ ./client <ip host> <port>
