# Tower of Ish MUD

## Local Setup

Currently, this project uses websockets to connect the game server to clients. The game server is a python websockets server. The client is a web client opened in browser, provided by accessing a webserver.

To run this on your local machine, allowing same computer connections:
- Download the project
- In the server folder, run `python server/server.py localhost 8000` to start the python server
- In the client folder, run `http-server` to start the webserver
- Connect to `http://localhost:8080/` to open the web client

For windows 10, or other bat compatible systems:
- Download the project
- Run `server/run.bat` to start the python server
- Run `client/run.bat` to start the webserver
- Connect to `http://localhost:8080/` to open the web client


## Commits

Try to prefix commits with one of the following categories:
- `Fix`: for commits focused on specific bug fixes
- `Add`: for commits that introduce new functionality
- `Update`: for commits that improve existing functionality
- `Remove`: for commits that remove existing functionality
- `Dev`: for commits that focus on documentation or refactoring