# import asyncio
# from fastmcp import Client

# async def test_server():
#     """Test the MCP server via SSE"""
#     print("🚀 Testing MCP Server via SSE...")
#     print("-" * 30)
    
#     try:
        
#         async with Client("http://127.0.0.1:8000/sse") as client: # SSE
        
#             print("✅ Connected to SSE server!")

#             # List of tools
#             tools = await client.list_tools()
#             for tool in tools:
#                 print(f"  • {tool.name}: {tool.description}")

#             result = await client.call_tool("get_weather", {"city": "NEW DELHI"})
#             print(f"Result: {result}")
#             return result
            
            
            
#     except Exception as e:
#         print(f"❌ Error: {e}")
        

# if __name__ == "__main__":
#     asyncio.run(test_server())

import json
import asyncio
from fastmcp import Client

def load_mcp_config(path):
    """Load MCP server info from config JSON file"""
    with open(path, "r") as f:
        config = json.load(f)
    # Access the server details by its name (e.g. 'weather-mcp')
    server_info = config["mcpServers"]["weather-mcp"]
    return server_info["url"], server_info.get("transport", "sse")

async def main():
    url, tp = load_mcp_config("../server.json")
    async with Client(url) as client:
        print("✅ Connected to MCP server!")
        tools = await client.list_tools()
        for tool in tools:
            print(f"  • {tool.name}: {tool.description}")
        result = await client.call_tool("get_weather", {"city": "NEW DELHI"})
        print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())

