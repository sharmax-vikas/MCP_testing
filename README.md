# MCP Testing Project

This project demonstrates a simple client-server setup using the `fastmcp` library for Model Context Protocol (MCP) communication. It includes a server that exposes tools via MCP and a client that connects to the server, lists available tools, and calls a sample tool.

## Project Structure

```
MCP_testing/
│
├── main.py
├── pyproject.toml
├── README.md
├── server.json
├── client/
│   └── client.py
├── server/
│   └── server.py
└── ...
```

## Requirements

- Python 3.8+
- [fastmcp](https://pypi.org/project/fastmcp/)
- [uv](https://github.com/astral-sh/uv) (for fast Python package management and running)

Install dependencies:

```
uv pip install fastmcp
```

## Running the Server

From the project root, run:

```
uv run fastmcp run server/server.py
```

This will start the MCP server. Make sure the server is running before starting the client.

## Running the Client

The client reads the MCP server URL from `server.json` and connects to it, listing available tools and calling the `get_weather` tool as an example.

From the `client` directory, run:

```
uv run client.py
```

## Configuration

The `server.json` file should look like this:

```
{
  "mcpServers": {
    "weather-mcp": {
      "url": "http://127.0.0.1:8000/sse",
      "transport": "sse"
    }
  }
}
```

## Example Output

```
✅ Connected to MCP server!
  • get_weather: Get the weather for a city
Result: { ... }
```

## Notes

- The client and server are both written in Python and use the `fastmcp` library for communication.
- You can add more tools to the server and call them from the client as needed.

---

For more information, see the `fastmcp` documentation or the code in `client/client.py` and `server/server.py`.
