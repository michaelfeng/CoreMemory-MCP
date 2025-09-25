# Project: Core Memory MCP

## Project Overview

This project aims to create an open-source "Core Memory" MCP (Memory Component/Platform) to optimize the context for user-LLM interactions. It acts as a long-term memory module for AI agents and IDEs, solving the problems of limited context windows, loss of important information, and the need to repeatedly provide background information.

**Future Brand Name**: The project is being developed with the future brand name "Cortex" in mind for its commercial version.

The system is built around three main concepts:
*   **Memory Store**: A simple, file-based storage for memories (e.g., JSON or SQLite).
*   **Memory Processor**: The "brain" of the system, responsible for processing, distilling, and indexing memories.
*   **Memory Interface**: An API for external tools (AI agents, IDE plugins, CLI) to interact with the memory core.

## MVP Plan

The MVP will be a command-line tool (CLI) named `core_memory` built with Python.

*   **Technology**: Python
*   **Database**: A single `memory_core.json` file.
*   **Core Functionalities**:
    *   `core_memory add "<memory_text>"`: Adds a new memory to the `memory_core.json` file.
    *   `core_memory search "<keyword>"`: Searches for memories containing a specific keyword.
    *   `core_memory list`: Lists all the stored memories.

## Development Conventions

*   The project will follow standard Python best practices.
*   Code will be formatted using a consistent style (e.g., Black).
*   The project will be licensed under an open-source license (e.g., MIT).

## Building and Running

As the project is in its initial phase, there are no build or run commands yet. The first step is to develop the `core_memory` CLI tool in Python.

**TODO**:
*   [ ] Implement the `core_memory` CLI tool with `add`, `search`, and `list` commands.
*   [ ] Define the exact JSON structure for a memory object.
*   [ ] Create a `requirements.txt` file for dependencies.
