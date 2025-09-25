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

克隆仓库并安装所需的 Python 包。

```bash
git clone https://github.com/michaelfeng/CoreMemory-MCP.git
cd CoreMemory-MCP
pip install -r requirements.txt
```

## 运行服务

在您的终端中运行 `memory_service.py` 脚本以启动服务器。

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

Google Gemini CLI 可以配置为自动启动和使用 MCP 服务器。

1.  打开 Gemini CLI 配置文件，通常位于 `~/.gemini/settings.json`。
2.  在 `mcp_servers` 列表中添加一个条目。您必须提供 `memory_service.py` 脚本的**绝对路径**。

**`settings.json` 示例：**
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
*请将 `/path/to/your/CoreMemory-MCP/` 替换为您系统上的实际绝对路径。*

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

## 如何使用（交互）

配置完成后，您可以通过代理的自然聊天界面与记忆服务进行交互。代理将自动调用适当的工具。

-   要保存一条记忆：`> 记住项目截止日期是下周五`
-   要搜索一条记忆：`> 关于项目截止日期我说了什么？`

您的代理现在已经意识到了 `memory.add` 和 `memory.search` 工具，它将调用您本地的核心记忆服务来完成这些请求。