# Core Memory

A lightweight, file-based, long-term memory engine for AI agents.

---

**[Read this in Chinese (中文文档)](README_zh.md)**

---

## What is Core Memory?

Core Memory is a Python module that provides a simple and persistent long-term memory for AI agents. It allows an agent to retain and recall information across different sessions, overcoming the limitations of finite context windows. It works by storing structured memories in a local JSON file, acting as a searchable, long-term knowledge base.

## Why Core Memory?

Modern LLM-powered agents are incredibly powerful but suffer from a fundamental limitation: they are stateless. Once a conversation ends, or the context window is full, information is lost. Core Memory solves this by providing:

-   **Statefulness**: Remembers key facts, user preferences, and past interactions.
-   **Context Enrichment**: Automatically injects relevant memories into prompts to give the agent better context.
-   **Efficiency**: Reduces the need to re-feed the same information, saving tokens and cost.
-   **Knowledge Persistence**: Builds a permanent, searchable knowledge base over time.
-   **Local-First & Private**: All data is stored locally on your machine. You own your data.

## Key Features

-   **Simple File-Based Storage**: Uses a human-readable `memory_core.json` file.
-   **Structured Memories**: Each memory includes content, a summary, timestamp, importance score, and source.
-   **Tagging System**: Supports adding tags to memories for efficient, topic-based retrieval.
-   **Developer-Friendly API**: A clean and simple Python API for all core operations.
-   **Lightweight & Dependency-Free**: Written in standard Python with no external libraries required.

## Installation

Currently, you can use Core Memory by simply cloning this repository and placing the `core_memory.py` file in your project's source directory.

```bash
# No installation required, just copy the file to your project.
```

## How to Use (API Guide)

Core Memory is designed to be used as a simple Python library. Import the functions from the `core_memory.py` module.

### Adding a Memory

```python
import core_memory

# Add a simple memory with tags and importance
new_mem = core_memory.add_memory(
    content="The user's favorite programming language is Python.",
    tags=['user', 'preference', 'python'],
    importance=8
)

print(f"Added memory with ID: {new_mem['id']}")
```

### Searching Memories

Search is case-insensitive and matches against content, summary, and tags.

```python
import core_memory

# Search for all memories related to 'python'
results = core_memory.search_memory("python")

for mem in results:
    print(f"Found: {mem['summary']}")
```

### Listing All Memories

```python
import core_memory

all_memories = core_memory.list_memories()

print(f"Total memories in database: {len(all_memories)}")
```

### Deleting a Memory

```python
import core_memory

# You need the ID of the memory to delete it
memory_id_to_delete = "... a-valid-uuid-from-a-memory ..."

was_deleted = core_memory.delete_memory(memory_id_to_delete)

if was_deleted:
    print(f"Memory {memory_id_to_delete} was deleted.")
```

## When to Use?

Use Core Memory whenever you want your agent to remember information for longer than a single session. 

-   **User Preferences**: "Please always respond in Markdown."

-   **Session Summaries**: Storing a summary of a long conversation for future reference.
-   **Task-Specific Context**: Remembering the steps taken to debug a piece of code.

## Integration with AI Agents

Core Memory is a library, not a standalone application. It is meant to be integrated into the logic of an AI agent.

The primary integration pattern is for the agent to import and call the `core_memory` functions based on the user's intent.

Here is a simplified example of an agent's main loop:

```python
import core_memory

def process_user_input(user_input: str):
    # This is where the agent's logic lives.
    # The agent developer decides how and when to call the memory engine.

    if user_wants_to_remember(user_input):
        # Logic to extract content from user_input
        content_to_remember = "..."
        core_memory.add_memory(content=content_to_remember)
        print("Agent: Okay, I'll remember that.")

    elif user_is_asking_a_question(user_input):
        # Use memory to enrich the prompt
        relevant_memories = core_memory.search_memory(query=user_input)
        
        context = "\n".join([mem['summary'] for mem in relevant_memories])
        prompt = f"""
        Background information from my memory:
        {context}

        User question: {user_input}
        """
        # Send the enriched prompt to the LLM
        # llm_response = call_llm(prompt)
        # print(f"Agent: {llm_response}")
```

## Interaction Patterns

An agent developer can implement several ways for a user to interact with the memory:

1.  **Explicit Commands**: The agent can be programmed to recognize a special prefix (e.g., `/mem`) to give the user direct control.
    -   `/mem add My API key is 123-xyz.`
    -   `/mem search API key`

2.  **Implicit Intent Recognition**: The agent uses an LLM to understand the user's natural language intent.
    -   User: "Hey, remember that my API key is 123-xyz."
    -   *Agent recognizes the 'remember' intent and calls `core_memory.add_memory()` behind the scenes.*

## How to Extend

This is an open-source project, and contributions are welcome. Here are some ideas for extending Core Memory:

-   **Multiple Storage Backends**: Create a storage provider interface and implement backends for SQLite, a vector database (like ChromaDB), or a cloud service.
-   **Smarter Search**: Implement semantic search using sentence embeddings.
-   **Automatic Summarization**: Integrate an LLM call within the `add_memory` function to automatically generate the summary and tags.

## Memory File Location

By default, Core Memory creates and uses a file named `memory_core.json` in the current working directory from where the script is executed. This can be configured by modifying the `DB_FILE` constant in `core_memory.py`.

