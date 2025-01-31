from pathlib import Path
import json
import os
from typing import Dict, Optional
from src.items import Item  # Your existing Item class

class ItemRegistry:
    _instance = None
    _items: Dict[str, Item] = {}  # Global item storage

    def __new__(cls):
        """Singleton pattern: Ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._load_all_items()
        return cls._instance

    @classmethod
    def _load_all_items(cls):
        items_dir = Path(__file__).parent.parent / "data" / "items"
        for filename in os.listdir(items_dir):
            if filename.endswith(".json"):
                filepath = items_dir / filename
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    for item_id, item_data in data.items():
                        # Rename 'type' to 'item_type' for the Item constructor
                        if 'type' in item_data:
                            item_data['item_type'] = item_data.pop('type')
                        # Pass all other fields as keyword arguments
                        cls._items[item_id] = Item(item_id=item_id, **item_data)

    @classmethod
    def get_item(cls, item_id: str) -> Optional[Item]:
        """Retrieve an item by ID from the registry."""
        return cls._items.get(item_id)

    @classmethod
    def get_all_items(cls) -> Dict[str, Item]:
        """Return all items in the registry."""
        return cls._items