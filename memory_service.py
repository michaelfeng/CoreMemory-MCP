"""
Core Memory Service (MCP-compliant)

This module runs a high-performance, async FastAPI web server that is compliant
with the Model Context Protocol (MCP), making it compatible with tools like
`gofastmcp`, Cursor, and Gemini-CLI.

It exposes a single `/mcp` endpoint that accepts JSON-RPC 2.0 requests.
"""

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

# Import the synchronous functions from our core engine
from core_memory import (
    add_memory,
    search_memory,
    list_memories,
    get_memory_by_id,
    delete_memory,
)

# --- Pydantic Models for Type Hinting & Validation ---

class JsonRpcRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Optional[Dict[str, Any]] = None
    id: int | str

# --- Tool Manifest (for mcp.discover) ---

# This manifest describes the tools our service provides to any MCP client.
TOOL_MANIFEST = {
    "mcp_version": "0.1.0",
    "tools": [
        {
            "name": "memory.add",
            "description": "Adds a new memory to the long-term memory store.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "The full content of the memory."},
                    "summary": {"type": "string", "description": "An optional, shorter summary of the content."},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "A list of tags for categorization."},
                    "importance": {"type": "integer", "description": "An integer score (1-10) for the memory's importance."},
                },
                "required": ["content"],
            },
        },
        {
            "name": "memory.search",
            "description": "Searches for memories matching a query string.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The text to search for in memories."},
                },
                "required": ["query"],
            },
        },
        {
            "name": "memory.list",
            "description": "Retrieves all memories from the database.",
            "parameters": {"type": "object", "properties": {}},
        },
        {
            "name": "memory.get",
            "description": "Retrieves a single memory by its unique ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "memory_id": {"type": "string", "description": "The UUID of the memory to retrieve."},
                },
                "required": ["memory_id"],
            },
        },
        {
            "name": "memory.delete",
            "description": "Deletes a memory by its unique ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "memory_id": {"type": "string", "description": "The UUID of the memory to delete."},
                },
                "required": ["memory_id"],
            },
        },
    ],
}

# --- FastAPI App and Endpoint ---

app = FastAPI(
    title="CoreMemory-MCP Server",
    description="A compliant MCP server for long-term agent memory.",
)

@app.post("/mcp")
async def mcp_endpoint(request: JsonRpcRequest):
    """Main JSON-RPC endpoint for all MCP interactions."""
    params = request.params if request.params is not None else {}

    try:
        result = None
        if request.method == "mcp.discover":
            result = TOOL_MANIFEST
        
        elif request.method == "memory.add":
            # FastAPI runs sync functions in a thread pool, so we don't block the event loop.
            result = add_memory(**params)
        
        elif request.method == "memory.search":
            result = search_memory(**params)

        elif request.method == "memory.list":
            result = list_memories()

        elif request.method == "memory.get":
            result = get_memory_by_id(**params)
            if result is None:
                 raise ValueError(f"Memory with ID {params.get('memory_id')} not found.")

        elif request.method == "memory.delete":
            was_deleted = delete_memory(**params)
            result = {"success": was_deleted}

        else:
            raise NotImplementedError(f"Method '{request.method}' not found.")

        return {"jsonrpc": "2.0", "result": result, "id": request.id}

    except Exception as e:
        error_payload = {
            "code": -32603,  # Internal error
            "message": str(e),
        }
        return JSONResponse(
            status_code=500,
            content={"jsonrpc": "2.0", "error": error_payload, "id": request.id},
        )


if __name__ == "__main__":
    print("--- Starting Core Memory MCP Service ---")
    print("Compatible with the Model Context Protocol.")
    print("Listening on http://127.0.0.1:5001")
    print("Access the API at the /mcp endpoint.")
    print("Use Ctrl+C to stop.")
    uvicorn.run(app, host="0.0.0.0", port=5001)