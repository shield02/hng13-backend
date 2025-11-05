# STAGE 3 - Build and Integrate AI Agents

Build AI agents and hook them up to Telex.im. 
We want to see how you design intelligent systems, 
handle integrations, and structure your code.

What You're Building
Create an AI agent that does something useful. 
Pick a task, solve a problem, help users.
Ideas:
Code helper that assists developers on Telex
Task tracker that reminds people about their projects
Bot that summarises data or automates chat responses

Other Languages (Python, Go, Java, Rust, C#, PHP, etc.):
Build your agent from scratch. Pick any framework or library you want.
What you need to do:
Write the core logic
Handle incoming messages
Create endpoints that work with Telex.im
Your API needs to be clean and talk to the platform without breaking.
Integration Requirements
Your agent needs to:
Respond to messages or events from Telex.im
Send back valid responses or actions
Use REST or WebSocket (keep it simple and consistent)
Handle errors properly and validate responses
You need to provide:
A public endpoint or repo we can test

## How to Run the App Locally

`make install`: Create venv & install deps

`make run`: Run FastAPI locally (uvicorn)

`make up`: Run full stack (API + Redis)

`make down`: Stop and remove stack

`make logs`: Tail logs for all services

`make build`: Build only API Docker image

`make attach`: Attach to a running container

`make debug`: Start container in DEBUG mode (interactive shell)

`make ngrok`: Expose app publicly via ngrok

`make clean`: Remove cache and pyc files
