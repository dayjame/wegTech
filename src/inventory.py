from typing import Dict, Optional
from src.item_registry import ItemRegistry


class Inventory:
    def __init__(self, max_weight: float = 100.0, max_slots: int = 20):
        self.items: Dict[str, int] = {}  # {item_id: quantity}
        self.max_weight = max_weight
        self.max_slots = max_slots

    def add_item(self, item_id: str, quantity: int = 1) -> bool:
        """Add an item by ID. Returns True if successful."""
        item = ItemRegistry.get_item(item_id)
        if not item:
            print(f"Item {item_id} not found in the registry!")
            return False

        # Calculate new weight
        new_weight = self.current_weight() + (item.weight * quantity)
        if new_weight > self.max_weight:
            print(f"Cannot add {item_id}: Overweight!")
            return False

        # Check slot limits
        if self.max_slots and len(self.items) >= self.max_slots:
            print(f"Cannot add {item_id}: Inventory full!")
            return False

        # Add item
        self.items[item_id] = self.items.get(item_id, 0) + quantity
        return True

    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        """Remove a quantity of an item by ID."""
        current_qty = self.items.get(item_id, 0)
        if current_qty < quantity:
            return False
        self.items[item_id] -= quantity
        if self.items[item_id] <= 0:
            del self.items[item_id]
        return True

    def current_weight(self) -> float:
        """Calculate total weight using ItemRegistry."""
        total = 0.0
        for item_id, qty in self.items.items():
            item = ItemRegistry.get_item(item_id)
            if item:
                total += item.weight * qty
        return total

    def display(self) -> str:
        """Generate inventory description using ItemRegistry."""
        if not self.items:
            return "Inventory is empty."

        text = [
            f"Inventory ({self.current_weight():.1f}/{self.max_weight} kg):",
            f"Slots: {len(self.items)}/{self.max_slots if self.max_slots else 'Unlimited'}"
        ]

        for item_id, qty in self.items.items():
            item = ItemRegistry.get_item(item_id)
            if not item:
                continue  # Skip invalid items
            entry = f"- {item.name} x{qty} ({item.item_type}, {item.weight} kg)"
            if item.stat_bonuses:
                entry += f"\n  Stats: {item.stat_bonuses}"
            if item.effect:
                entry += f"\n  Effect: {item.effect['type']}"
            text.append(entry)

        return "\n".join(text)

    def to_dict(self) -> Dict:
        return {
            "max_weight": self.max_weight,
            "max_slots": self.max_slots,
            "items": self.items
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Inventory':
        inventory = cls(
            max_weight=data["max_weight"],
            max_slots=data["max_slots"]
        )
        inventory.items = data["items"]
        return inventory
