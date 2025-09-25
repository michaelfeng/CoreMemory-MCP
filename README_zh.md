# CoreMemory-MCP (核心记忆组件)

一个为 AI 代理设计的、兼容 MCP 标准的本地长期记忆*服务*。

---

**[Read this in English (阅读英文版)](README.md)**

---

## CoreMemory-MCP 是什么？

CoreMemory-MCP 是一个后台服务，它为任何支持 **模型上下文协议 (MCP)** 的 AI 代理提供简单且持久的长期记忆。它允许像 **Cursor**、**Gemini-CLI** 和 **Claude Code-Cli** 这样的工具跨会话保留和回忆信息。

它作为独立服务器在您的本地计算机上运行，为您最喜欢的 AI 工具充当一个与语言无关、可插拔的大脑。

## 工作原理

该架构是基于 MCP 标准的典型客户端-服务器模型：

`[您的代理 / IDE] <--> [MCP (基于 HTTP 的 JSON-RPC)] <--> [核心记忆服务]`

1.  您运行核心记忆服务。
2.  您配置您的客户端应用程序（例如 Cursor、Gemini-CLI）以连接到该服务。
3.  然后，您的客户端应用程序可以发现并执行由该服务提供的记忆工具（`memory.add`、`memory.search` 等）。

## 安装

> **请注意**：该软件包尚未发布到 PyPI。以下是计划中的安装方法。

发布后，建议通过 pip 安装：

```bash
pip install core-memory-mcp
```

或者，对于开发，您可以克隆仓库并以可编辑模式安装：
```bash
git clone https://github.com/michaelfeng/CoreMemory-MCP.git
cd CoreMemory-MCP
pip install -e .
```

## 运行服务

如果您通过 pip 安装了该软件包，您可以在终端中运行以下命令来启动服务：

```bash
core-memory-server
```

如果您从源代码运行，您也可以直接运行脚本：
```bash
python memory_service.py
```

您将看到输出，表明服务正在运行并准备接受连接：
```
--- Starting Core Memory MCP Service ---
Compatible with the Model Context Protocol.
Listening on http://127.0.0.1:5001
Access the API at the /mcp endpoint.
Use Ctrl+C to stop.
```
**重要提示：** 请保持此终端窗口打开。该服务需要在后台运行，以便您的客户端可以连接到它。

## 配置您的客户端

以下是针对支持 MCP 的流行工具的具体说明。

### 针对 Gemini-CLI

Google Gemini CLI 可以配置为自动启动和使用 MCP 服务器。安装此软件包后，您可以配置 Gemini-CLI 来使用它。

1.  打开 Gemini CLI 配置文件，通常位于 `~/.gemini/settings.json`。
2.  在 `mcp_servers` 列表中添加一个指向 `core-memory-server` 命令的条目。

**`settings.json` 示例：**
```json
{
  "mcp_servers": [
    {
      "name": "CoreMemory",
      "command": [
        "core-memory-server"
      ]
    }
  ]
}
```
*（此配置假设 `core-memory-server` 命令在您系统的 PATH 中可用，这在 `pip install` 后是标准情况。）*

3.  保存文件。下次运行 `gemini` 时，它将自动启动记忆服务并可以访问 `memory.*` 工具。

### 针对 Cursor

Cursor 使用 MCP 进行其深度 AI 集成。要连接 CoreMemory-MCP，您可以将其配置为工具源。

1.  在 Cursor 中，打开设置（例如，通过 `Cmd/Ctrl + ,`）。
2.  搜索与 **"Tools"**、**"AI Sources"** 或 **"MCP"** 相关的设置。
3.  查找 **"Add a new MCP Server"** 或 **"Tool Provider"** 的选项。
4.  在配置中，提供您**正在运行的**核心记忆服务的地址：`http://127.0.0.1:5001/mcp`。
5.  保存设置。Cursor 现在应该能够发现和使用 `memory.*` 工具。

*（注意：Cursor 的用户界面可能会发生变化。有关添加外部 MCP 工具提供程序的最新说明，请参阅其官方文档。）*

### 针对 Claude Code-Cli

Claude Code-Cli 也支持 MCP 以使用外部工具。
配置过程预计与 Gemini-CLI 类似，可能涉及一个中央配置文件，您可以在其中声明 MCP 服务器。

1.  找到 Claude Code-Cli 的主配置文件（例如，它可能在 `~/.claude/config.json` 中）。
2.  为 Core Memory MCP 服务器添加一个条目，类似于 Gemini-CLI 的示例。

**Claude Code-Cli 的假设 `config.json`：**
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
*（注意：这是一个假设的示例。有关如何注册已在运行的 MCP 服务器，请查阅 Claude Code-Cli 的具体文档。）*

### 与 FastMCP 的集成

[FastMCP](https://gofastmcp.com/) 是一个同样兼容模型上下文协议（MCP）的框架。由于 `CoreMemory-MCP` 也遵循 MCP 标准，因此两者天然兼容，可以协同工作。

作为用户，您需要了解以下几点：

*   **完全兼容**：您可以使用任何基于 `fastmcp` 开发的客户端来连接您本地的 `CoreMemory-MCP` 服务。因为双方都遵循同一协议，集成是无缝的。

*   **现有用户不受影响**：如果您已在通过 Cursor、Gemini-CLI 等工具使用 `CoreMemory-MCP`，这项集成不会对您现有的工作流程产生任何影响。

*   **如何连接 FastMCP 客户端**：当您需要将一个 `fastmcp` 客户端连接到本服务时，只需在该客户端的配置中填入您本地服务的地址，默认为 `http://127.0.0.1:5001/mcp`。

*   **本地与云端的选择**：`CoreMemory-MCP` 的核心设计是**本地优先**，确保您的数据保留在自己的设备上。FastMCP 提供了云服务，但请注意，如果您选择使用 FastMCP 的云产品，您的数据可能会被发送到云端服务器。通过运行 `CoreMemory-MCP`，您可以始终选择将记忆数据保留在本地。

## 如何使用（交互）

### 命令式交互（推荐）

为了进行更精确的控制，您可以直接在与代理的聊天中使用斜杠命令。这是与记忆服务交互的推荐方式，因为它可以避免自然语言带来的歧义。

*   **/cortex add**: 保存一条新记忆。
*   **/cortex search**: 搜索记忆。
*   **/cortex list**: 列出所有记忆。

**示例:**

```
> /cortex add "项目截止日期是下周五"
```

```
> /cortex search "截止日期"
```

```
> /cortex list
```

*（请注意：此功能的实现依赖于代理端（Agent）的解析能力，需要代理能识别这些命令并调用相应的 `memory.*` 工具。我们计划在 Gemini-CLI 等客户端中支持此功能。）*

### 自然语言交互

您也可以通过自然语言与记忆服务进行交互。代理会尽力理解您的意图并调用适当的工具。

-   要保存一条记忆：`> 记住项目截止日期是下周五`
-   要搜索一条记忆：`> 关于项目截止日期我说了什么？`

您的代理现在已经意识到了 `memory.add` 和 `memory.search` 工具，它将调用您本地的核心记忆服务来完成这些请求。