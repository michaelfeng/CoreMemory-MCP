# Core Memory (核心记忆)

一个为 AI Agent 打造的、基于文件的轻量级长期记忆引擎。

---

**[Read this in English](README.md)**

---

## 什么是核心记忆 (Core Memory)？

核心记忆是一个 Python 模块，它为 AI Agent 提供了一个简单且持久化的长期记忆能力。它允许 Agent 在不同的会话之间保持和回忆信息，克服了有限上下文窗口的束缚。它的工作原理是将结构化的记忆存储在一个本地 JSON 文件中，作为一个可搜索的、长期的知识库。

## 为什么需要核心记忆？

现代由 LLM 驱动的 Agent 功能极其强大，但它们存在一个根本性的限制：它们是无状态的。一旦对话结束或上下文窗口满了，信息就会丢失。核心记忆通过提供以下能力来解决这个问题：

-   **状态保持**: 记住关键事实、用户偏好和历史互动。
-   **上下文增强**: 自动将相关的记忆注入到 Prompt 中，为 Agent 提供更丰富的上下文。
-   **提升效率**: 减少重复提供相同信息的需要，节省 Token 和成本。
-   **知识沉淀**: 随着时间的推移，建立一个永久的、可搜索的知识库。
-   **本地优先与隐私**: 所有数据都存储在您的本地机器上，您完全拥有自己的数据。

## 核心功能

-   **简单的文件存储**: 使用人类可读的 `memory_core.json` 文件。
-   **结构化记忆**: 每条记忆都包含内容、摘要、时间戳、重要性评分和来源。
-   **标签系统**: 支持为记忆添加标签，以实现高效的、基于主题的检索。
-   **开发者友好的 API**: 为所有核心操作提供了一套简洁明了的 Python API。
-   **轻量级与无依赖**: 使用标准 Python 编写，无需任何外部库。

## 如何安装

目前，您只需克隆此仓库，并将 `core_memory.py` 文件放入您项目的源代码目录中即可使用。

```bash
# 无需安装，仅需将 core_memory.py 文件复制到您的项目中
```

## 如何使用 (API 指南)

核心记忆被设计为一个简单的 Python 库来使用。从 `core_memory.py` 模块中导入所需函数即可。

### 添加一条记忆

```python
import core_memory

# 添加一条带标签和重要性评分的简单记忆
new_mem = core_memory.add_memory(
    content="用户最喜欢的编程语言是 Python。",
    tags=['user', 'preference', 'python'],
    importance=8
)

print(f"已添加记忆，ID 为: {new_mem['id']}")
```

### 搜索记忆

搜索不区分大小写，会匹配每条记忆的内容、摘要和标签。

```python
import core_memory

# 搜索所有与 'python' 相关的记忆
results = core_memory.search_memory("python")

for mem in results:
    print(f"找到: {mem['summary']}")
```

### 列出所有记忆

```python
import core_memory

all_memories = core_memory.list_memories()

print(f"数据库中总共有 {len(all_memories)} 条记忆。")
```

### 删除一条记忆

```python
import core_memory

# 您需要提供记忆的 ID 才能删除它
memory_id_to_delete = "... 一个有效的记忆 UUID ..."

was_deleted = core_memory.delete_memory(memory_id_to_delete)

if was_deleted:
    print(f"记忆 {memory_id_to_delete} 已被删除。")
```

## 何时使用？

当您希望您的 Agent 能够跨会话记住信息时，就应该使用核心记忆。

-   **用户偏好**: “请总是用 Markdown 格式回复我。”

-   **会话总结**: 存储一段长对话的摘要，以备将来参考。
-   **特定任务上下文**: 记住为了调试一段代码所执行的步骤。

## 如何与 AI Agent 集成

核心记忆是一个库，而非一个独立应用。它需要被集成到 AI Agent 的业务逻辑中。

主要的集成模式是让 Agent 根据用户的意图，导入并调用 `core_memory` 的函数。

以下是一个简化的 Agent 主循环示例：

```python
import core_memory

def process_user_input(user_input: str):
    # 这里是 Agent 的业务逻辑所在地
    # Agent 的开发者决定何时以及如何调用记忆引擎

    if user_wants_to_remember(user_input):
        # 从用户输入中提取需要记忆的内容
        content_to_remember = "..."
        core_memory.add_memory(content=content_to_remember)
        print("Agent:好的，我会记住的。")

    elif user_is_asking_a_question(user_input):
        # 使用记忆来丰富 Prompt
        relevant_memories = core_memory.search_memory(query=user_input)
        
        context = "\n".join([mem['summary'] for mem in relevant_memories])
        prompt = f""
        来自我长期记忆的背景信息:
        {context}

        用户的问题: {user_input}
        ""
        # 将这个增强版的 Prompt 发送给 LLM
        # llm_response = call_llm(prompt)
        # print(f"Agent: {llm_response}")
```

## 交互模式

Agent 开发者可以实现多种方式让用户与记忆核心进行交互：

1.  **显式命令**: Agent 可以被编程为识别一个特殊前缀（如 `/mem`），给予用户直接的控制权。
    -   `/mem add 我的 API 密钥是 123-xyz。`
    -   `/mem search API 密钥`

2.  **隐式意图识别**: Agent 使用一个 LLM 来理解用户的自然语言意图。
    -   用户: “嘿，记住我的 API 密钥是 123-xyz。”
    -   *Agent 识别出‘记忆’的意图，并在后台调用 `core_memory.add_memory()`。*

## 如何拓展

这是一个开源项目，欢迎任何形式的贡献。这里有一些拓展核心记忆的想法：

-   **多种存储后端**: 创建一个统一的存储接口，并实现针对 SQLite、向量数据库（如 ChromaDB）或云服务的存储后端。
-   **更智能的搜索**: 使用句向量实现语义搜索。
-   **自动摘要**: 在 `add_memory` 函数中集成 LLM 调用，以自动生成摘要和标签。

## 记忆文件位置

默认情况下，核心记忆会在执行脚本的当前工作目录下创建并使用一个名为 `memory_core.json` 的文件。您可以通过修改 `core_memory.py` 文件中的 `DB_FILE` 常量来配置此路径。

