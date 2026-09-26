"""
data_manager.py — Async History Storage
=========================================
Handles saving and loading health assessment history using asyncio + JSON.
Each entry stores inputs, risk label, and timestamp.
"""

import asyncio
import json
import os
from datetime import datetime


HISTORY_FILE = "health_history.json"


class DataManager:
    """Manages persistent storage of health assessment history."""

    def __init__(self, filepath: str = HISTORY_FILE):
        self.filepath = filepath
        self._lock = asyncio.Lock()

    async def save_entry(self, inputs: dict, risk_label: str) -> None:
        """Async save a new assessment entry to JSON history."""
        async with self._lock:
            history = await self._read_file()
            entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "risk_label": risk_label,
                **inputs
            }
            history.append(entry)
            await self._write_file(history)

    async def load_history(self) -> list[dict]:
        """Async load full history list."""
        return await self._read_file()

    async def _read_file(self) -> list:
        """Read JSON file asynchronously (offloaded to thread)."""
        def _read():
            if not os.path.exists(self.filepath):
                return []
            try:
                with open(self.filepath, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []

        return await asyncio.to_thread(_read)

    async def _write_file(self, data: list) -> None:
        """Write JSON file asynchronously (offloaded to thread)."""
        def _write():
            with open(self.filepath, "w") as f:
                json.dump(data, f, indent=2)

        await asyncio.to_thread(_write)

    async def clear_history(self) -> None:
        """Clear all stored history."""
        async with self._lock:
            await self._write_file([])
