# CCDR Explorer RAG client for working with World Bank climate development reports

This is the application layer for a web app for AI-powered semantic search over the World Bank's Country Climate and Development Reports (CCDRs). It is built on the [FastAPI, Jinja2, PostgreSQL Webapp Template](https://github.com/Promptly-Technologies-LLC/fastapi-jinja2-postgres-webapp) and the OpenAI Assistants API.

Eventually, we plan to migrate from OpenAI's infrastructure to our custom infrastructure, which will support a wider range of AI models as the agent driver, and which will use the (Sustainable Sovereign Debt Hub RAG Database and API)[https://github.com/Teal-Insights/nature-finance-rag-api] as the data storage and retrieval layer.

## Getting Started

### Install `uv` for Dependency Management

MacOS and Linux:

``` bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

Windows:

``` bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

See the [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/) for more information.

### Install Python

Install the latest version of Python from either the official [downloads page](https://www.python.org/downloads/) or using `uv`:

``` bash
# Installs the latest version
uv python install
```

### Install Docker Desktop and Docker Compose

Install Docker Desktop and Coker Compose for your operating system by following the [instructions in the documentation](https://docs.docker.com/compose/install/).

### Install PostgreSQL headers

For Ubuntu/Debian:

``` bash
sudo apt update && sudo apt install -y python3-dev libpq-dev libwebp-dev
```

For macOS:

``` bash
brew install postgresql
```

For Windows:

- No installation required

### Install Python Dependencies

From the root directory, run:

``` bash
uv venv
uv sync
```

This will create an in-project virtual environment and install all dependencies.

### Set Environment Variables

Copy `.env.example` to `.env` with `cp .env.example .env`.

Generate a 256 bit secret key with `openssl rand -base64 32` and paste it into the .env file.

Set your desired database name, username, and password in the `.env` file.

[Create an OpenAI assistant](https://platform.openai.com/assistants/) and set your assistant's ID and your OpenAI API key in the `.env` file.

To use password recovery and other email features, register a [Resend](https://resend.com/) account, verify a domain, get an API key, and paste the API key and the email address you want to send emails from into the .env file. Note that you will need to [verify a domain through the Resend dashboard](https://resend.com/docs/dashboard/domains/introduction) to send emails from that domain.

### Start development database

To start the development database, run the following command in your terminal from the root directory:

``` bash
docker compose up -d
```

### Run the development server

Make sure the development database is running and tables and default permissions/roles are created first.

``` bash
uv run python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Navigate to http://localhost:8000/

## Deploy to Production on Modal

``` bash
uv run modal deploy deploy.py
```

## Usage

To "chat with the CCDRs", register and/or sign in and navigate to the chat interface on the home page. Use the chat interface to ask the chatbot questions about the CCDRs.

## Architecture

```mermaid
graph TB
    subgraph "Application"
        A[Browser Client] --> |"User messages"|C[Chat Application Server]
        C -->|"Assistant messages, tool calls, tool results"| A
    end

    subgraph "OpenAI Assistants API"
        D[Assistant Model] -->|"Assistant messages"| C
        D -->|"Code Interpreter<br>or File Search tool calls"| E[OpenAI Function Executor]
        E -->|"Result"| D
        C -->|"User messages"| D
        E -->|"Result"| C
    end
```

## License

This project is created and maintained by Teal Insights and licensed under the MIT License. See the LICENSE file for more details.
