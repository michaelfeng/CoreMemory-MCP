# CoreMemory-MCP

A local, MCP-compliant, long-term memory *service* for AI agents.

---

**[Read this in Chinese (中文文档)](README_zh.md)**

---

## What is CoreMemory-MCP?

CoreMemory-MCP is a background service that provides a simple and persistent long-term memory for any AI agent that supports the **Model Context Protocol (MCP)**. It allows tools like **Cursor**, **Gemini-CLI**, and **Claude Code-Cli** to retain and recall information across sessions.

It runs as a standalone server on your local machine, acting as a language-agnostic, pluggable brain for your favorite AI tools.

## How It Works

The architecture is a standard client-server model based on the MCP standard:

`[Your Agent / IDE] <--> [MCP (JSON-RPC over HTTP)] <--> [Core Memory Service]`

1.  You run the Core Memory service.
2.  You configure your client application (e.g., Cursor, Gemini-CLI) to connect to the service.
3.  Your client application can then discover and execute the memory tools (`memory.add`, `memory.search`, etc.) provided by the service.

## Installation

Clone the repository and install the required Python packages.

```bash
git clone https://github.com/michaelfeng/CoreMemory-MCP.git
cd CoreMemory-MCP
pip install -r requirements.txt
```

## Running the Service

Run the `memory_service.py` script in your terminal to start the server.

```bash
python memory_service.py
```

You will see output indicating the service is running and ready to accept connections:
```
--- Starting Core Memory MCP Service ---
Compatible with the Model Context Protocol.
Listening on http://127.0.0.1:5001
Access the API at the /mcp endpoint.
Use Ctrl+C to stop.
```
**Important:** Keep this terminal window open. The service needs to be running in the background for your clients to connect to it.

## Configuring Your Client

Here are specific instructions for popular tools that support MCP.

### For Gemini-CLI

The Google Gemini CLI can be configured to automatically start and use MCP servers.

1.  Open the Gemini CLI settings file, typically located at `~/.gemini/settings.json`.
2.  Add an entry to the `mcp_servers` list. You must provide the **absolute path** to the `memory_service.py` script.

**Example `settings.json`:**
```json
{
  "mcp_servers": [
    {
      "name": "CoreMemory",
      "command": [
        "python",
        "/path/to/your/CoreMemory-MCP/memory_service.py"
      ]
    }
  ]
}
```
*Replace `/path/to/your/CoreMemory-MCP/` with the actual absolute path on your system.*

3.  Save the file. The next time you run `gemini`, it will automatically start the memory service and have access to the `memory.*` tools.

### For Cursor

Cursor uses MCP for its deep AI integrations. To connect CoreMemory-MCP, you can configure it as a tool source.

1.  In Cursor, open the settings (e.g., via `Cmd/Ctrl + ,`).
2.  Search for settings related to **"Tools"**, **"AI Sources"**, or **"MCP"**.
3.  Look for an option to **"Add a new MCP Server"** or **"Tool Provider"**.
4.  In the configuration, provide the address of your **running** Core Memory service: `http://127.0.0.1:5001/mcp`.
5.  Save the settings. Cursor should now be able to discover and use the `memory.*` tools.

*(Note: Cursor's UI for this may evolve. Please refer to their official documentation for the most up-to-date instructions on adding external MCP tool providers.)*

### For Claude Code-Cli

Claude Code-Cli also supports MCP for external tooling.
The configuration process is expected to be similar to Gemini-CLI, likely involving a central configuration file where you can declare MCP servers.

1.  Locate the main configuration file for Claude Code-Cli (e.g., it might be in `~/.claude/config.json`).
2.  Add an entry for the Core Memory MCP server, similar to the Gemini-CLI example.

**Hypothetical `config.json` for Claude Code-Cli:**
```json
{
  "mcp_servers": [
    {
      "name": "CoreMemory",
      "address": "http://127.0.0.1:5001/mcp"
    }
  ]
}
```
*(Note: This is a hypothetical example. Please consult the specific documentation for Claude Code-Cli on how to register an already running MCP server.)*

## Integration with FastMCP

[FastMCP](https://gofastmcp.com/) is another framework that is compatible with the Model Context Protocol (MCP). Because `CoreMemory-MCP` also follows the MCP standard, they are compatible and can work together.

Here's what you need to know as a user:

*   **Full Compatibility**: You can use any `fastmcp`-based client to connect to your local `CoreMemory-MCP` service. The integration is seamless because both tools "speak" the same protocol.

*   **No Changes for Existing Users**: If you are already using `CoreMemory-MCP` with clients like Cursor or Gemini-CLI, this integration does not change anything for you. Your existing setup will continue to work as before.

*   **Connecting a `fastmcp` Client**: To connect a `fastmcp` client to this service, you will need to provide the client with the address of your local `CoreMemory-MCP` server, which is typically `http://127.0.0.1:5001/mcp`.

*   **Local vs. Cloud**: `CoreMemory-MCP` is designed to be a **local-first** memory service, meaning your data stays on your machine. While `fastmcp` offers a cloud service, please be aware that if you use it, your data might be sent to their servers. You have the choice to keep your memory local by running `CoreMemory-MCP`.

## How to Use (Interaction)

### Command-Based Interaction (Recommended)

For more precise control, you can use slash commands directly in your chat with the agent. This is the recommended way to interact with the memory service as it avoids ambiguity.

*   **/memory add**: Saves a new memory.
*   **/memory search**: Searches for memories.
*   **/memory list**: Lists all memories.

**Examples:**

```
> /memory add "The project deadline is next Friday"
```

```
> /memory search "deadline"
```

```
> /memory list
```

*(Note: This functionality depends on the agent's implementation to parse these commands and call the corresponding `memory.*` tools. This feature is planned for clients like Gemini-CLI.)*

### Natural Language Interaction

You can also interact with the memory service through natural language. The agent will do its best to understand your intent and call the appropriate tool.

-   To save a memory: `> remember that the project deadline is next Friday`
-   To search for a memory: `> what did I say about the project deadline?`

Your agent, now aware of the `memory.add` and `memory.search` tools, will call your local Core Memory service to fulfill these requests.