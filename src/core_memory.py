"""
Core Memory Engine

This module provides the core functionalities for managing a persistent, file-based
long-term memory for AI agents. It supports adding, searching, listing, and
deleting memories, with a strong emphasis on structured data including tags.

The memory database is a simple JSON file (`memory_core.json`).
"""

import json
import os
import uuid
from datetime import datetime, timezone

# --- Constants ---
DB_FILE = "memory_core.json"


# --- Private Helper Functions ---

def _init_db():
    """Initializes the database file if it doesn't exist."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

def _load_db() -> list:
    """Loads the memory database from the JSON file."""
    _init_db()  # Ensure DB file exists before loading
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def _save_db(data: list):
    """Saves the memory database to the JSON file."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# --- Public API Functions ---

def add_memory(
    content: str,
    summary: str = None,
    tags: list = None,
    importance: int = 5,
    source: dict = None,
    memory_type: str = "USER_INPUT"
) -> dict:
    """
    Adds a new memory to the database.

    Args:
        content: The full, original content of the memory.
        summary: An optional, shorter summary of the content.
        tags: A list of string tags for categorization and efficient search.
        importance: An integer score (1-10) representing the memory's importance.
        source: A dictionary describing the origin of the memory (e.g., {'type': 'cli'}).
        memory_type: The type of memory (e.g., 'USER_INPUT', 'AI_OUTPUT').

    Returns:
        The newly created memory object.
    """
    if tags is None:
        tags = []

    memories = _load_db()

    new_memory = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": memory_type,
        "content": content,
        "summary": summary if summary else content[:100],  # Simple summary fallback
        "tags": [tag.lower() for tag in tags], # Store tags in lowercase
        "importance": importance,
        "source": source if source else {'type': 'unknown'},
    }

    memories.append(new_memory)
    _save_db(memories)
    return new_memory

def search_memory(query: str) -> list:
    """
    Searches for memories matching a query string.

    The search is case-insensitive and checks for the query in the
    content, summary, and tags of each memory.

    Args:
        query: The string to search for.

    Returns:
        A list of memory objects that match the query, sorted by importance.
    """
    if not query:
        return []

    memories = _load_db()
    query_lower = query.lower()
    
    results = []
    for mem in memories:
        # Check if query is in content, summary, or any of the tags
        in_content = query_lower in mem.get('content', '').lower()
        in_summary = query_lower in mem.get('summary', '').lower()
        in_tags = any(query_lower in tag for tag in mem.get('tags', []))

        if in_content or in_summary or in_tags:
            results.append(mem)
            
    # Sort results by importance, descending
    results.sort(key=lambda x: x.get('importance', 0), reverse=True)
    
    return results

def list_memories() -> list:
    """
    Retrieves all memories from the database.

    Returns:
        A list of all memory objects.
    """
    return _load_db()

def get_memory_by_id(memory_id: str) -> dict | None:
    """
    Retrieves a single memory by its unique ID.

    Args:
        memory_id: The UUID of the memory to retrieve.

    Returns:
        The memory object if found, otherwise None.
    """
    memories = _load_db()
    for mem in memories:
        if mem.get('id') == memory_id:
            return mem
    return None

def delete_memory(memory_id: str) -> bool:
    """
    Deletes a memory by its unique ID.

    Args:
        memory_id: The UUID of the memory to delete.

    Returns:
        True if a memory was deleted, False otherwise.
    """
    memories = _load_db()
    initial_count = len(memories)
    
    memories_to_keep = [mem for mem in memories if mem.get('id') != memory_id]
    
    if len(memories_to_keep) < initial_count:
        _save_db(memories_to_keep)
        return True
    return False

# --- Example Usage & Simple Test ---
if __name__ == "__main__":
    print("--- Core Memory Engine Test ---")
    
    # Clean up previous test runs
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    # 1. Add memories
    print("\n1. Adding memories...")
    add_memory(
        "Python is a versatile programming language.",
        tags=['python', 'programming'],
        importance=8
    )
    add_memory(
        "The project 'Cortex' will use a JSON file for storage initially.",
        summary="Cortex project to use JSON storage.",
        tags=['cortex', 'storage', 'json'],
        importance=7
    )
    add_memory(
        "FastAPI is a modern, fast web framework for building APIs with Python.",
        tags=['python', 'fastapi', 'webdev'],
        importance=9
    )

    all_mems = list_memories()
    print(f"   -> Total memories: {len(all_mems)}")
    assert len(all_mems) == 3

    # 2. Search for memories
    print("\n2. Searching for 'python'...")
    python_results = search_memory("python")
    print(f"   -> Found {len(python_results)} results (should be 2).")
    assert len(python_results) == 2
    # The FastAPI memory should be first due to higher importance
    assert python_results[0]['tags'][1] == 'fastapi'
    print("   -> Search results seem correct.")

    # 3. Get a memory by ID
    print("\n3. Getting memory by ID...")
    first_mem_id = all_mems[0]['id']
    retrieved_mem = get_memory_by_id(first_mem_id)
    print(f"   -> Retrieved content: \"{retrieved_mem['content'][:30]}...\"")
    assert retrieved_mem is not None

    # 4. Delete a memory
    print("\n4. Deleting a memory...")
    delete_memory(first_mem_id)
    all_mems_after_delete = list_memories()
    print(f"   -> Total memories after delete: {len(all_mems_after_delete)} (should be 2).")
    assert len(all_mems_after_delete) == 2
    assert get_memory_by_id(first_mem_id) is None
    print("   -> Deletion successful.")
    
    print("\n--- Test Complete ---")
