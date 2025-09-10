
# MCP Testing Project

This project demonstrates a simple client-server setup using the `fastmcp` library for Model Context Protocol (MCP) communication. It includes:

- A server that exposes tools and resources via MCP (see `server/server.py` and `server/mcp_blog_server.py`)
- A client that connects to the server, lists available tools, and calls a sample tool (see `client/client.py`)

## Advanced Example: Blog MCP Server

The file `server/mcp_blog_server.py` demonstrates advanced MCP server features:

- **Dynamic Resources**: Exposes blog posts, single post, and category-based resources with caching and templates.
- **Complex Tools**: Tools for creating posts, publishing workflows, batch tag updates, and searching posts with parameter validation and caching.
- **Caching**: Uses `cachetools.TTLCache` for efficient response caching.
- **Tool Chaining**: Implements multi-step workflows (e.g., publishing a post and notifying subscribers).
- **Asynchronous Operations**: Batch operations and async processing for scalability.

To run the advanced blog server:

```bash
uv run fastmcp run server/mcp_blog_server.py
```

You can then connect with a compatible MCP client to interact with the blog tools and resources.

## Project Structure


```text
MCP_testing/
│
├── main.py
├── pyproject.toml
├── README.md
├── server.json
├── client/
│   └── client.py
├── server/
│   ├── server.py
│   └── mcp_blog_server.py
└── ...
```

## Requirements

- Python 3.8+
- [fastmcp](https://pypi.org/project/fastmcp/)
- [uv](https://github.com/astral-sh/uv) (for fast Python package management and running)

Install dependencies:


```bash
uv pip install fastmcp
```

## Running the Server

From the project root, run:


```bash
uv run fastmcp run server/server.py
```

This will start the MCP server. Make sure the server is running before starting the client.

## Running the Client

The client reads the MCP server URL from `server.json` and connects to it, listing available tools and calling the `get_weather` tool as an example.

From the `client` directory, run:


```bash
uv run client.py
```

## Configuration

The `server.json` file should look like this:


```json
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


```text
✅ Connected to MCP server!
  • get_weather: Get the weather for a city
Result: { ... }
```

## Notes

- The client and server are both written in Python and use the `fastmcp` library for communication.
- You can add more tools to the server and call them from the client as needed.

---

For more information, see the `fastmcp` documentation or the code in `client/client.py`, `server/server.py`, and `server/mcp_blog_server.py`.
