from typing import Dict, List, Optional
from src.items import Item, all_items  # Import your Item class


class Inventory:
    def __init__(
            self,
            max_weight: float = 100.0,
            max_slots: int = 20
    ):
        self.items: Dict[str, int] = {}  # {item_id: quantity}
        self.max_weight = max_weight
        self.max_slots = max_slots

    def add_item(
            self,
            item_id: str,
            all_items: Dict[str, Item],  # Required parameter first
            quantity: int = 1
    ) -> bool:
        """Add an item by ID. Returns True if successful."""
        item = all_items.get(item_id)
        if not item:
            print(f"Item {item_id} not found!")
            return False

        # Check weight
        new_weight = self.current_weight(all_items) + (item.weight * quantity)
        if new_weight > self.max_weight:
            print(f"Cannot add {item_id}: Overweight!")
            return False

        # Check slots (if slot-limited)
        if self.max_slots and len(self.items) >= self.max_slots:
            print(f"Cannot add {item_id}: Inventory full!")
            return False

        # Add item
        self.items[item_id] = self.items.get(item_id, 0) + quantity
        return True

    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        """Remove a quantity of an item by ID."""
        if self.items.get(item_id, 0) >= quantity:
            self.items[item_id] -= quantity
            if self.items[item_id] <= 0:
                del self.items[item_id]
            return True
        return False

    def current_weight(self, ALL_ITEMSs: Dict[str, Item]) -> float:
        """Calculate total weight of the inventory."""
        return sum(
            all_items[item_id].weight * qty
            for item_id, qty in self.items.items()
        )

    def display(self, ALL_ITEMS: Dict[str, Item]) -> str:
        """Return a formatted inventory string."""
        if not self.items:
            return "Inventory is empty."

        text = f"Inventory ({self.current_weight(all_items)}/{self.max_weight} kg):\n"
        for item_id, qty in self.items.items():
            item = all_items[item_id]
            text += f"- {item.name} x{qty} ({item.item_type}, {item.weight} kg)\n"
            if item.effect:
                text += f"  Effect: {item.effect['type']}\n"
            if item.stat_bonuses:
                text += f"  Stats: {item.stat_bonuses}\n"
        return text

    def to_dict(self) -> Dict:
        """Serialize inventory for saving."""
        return {

            "max_weight": self.max_weight,
            "max_slots": self.max_slots,
            "items": self.items
        }

    @classmethod
    def from_dict(
        cls,
        data: Dict,
        all_items: Dict[str, Item]
    ) -> 'Inventory':
        """Load inventory from a dictionary."""
        inventory = cls(
            max_weight=data["max_weight"],
            max_slots=data["max_slots"]
        )
        # Validate item IDs exist before adding
        for item_id, qty in data["items"].items():
            if item_id in all_items:
                inventory.items[item_id] = qty
            else:
                print(f"WARNING: Skipping invalid item {item_id} in saved inventory.")
        return inventory

    # Load all items first
    # Load items first
from src.items import load_all_items
all_items = load_all_items()

    # Initialize inventory
inventory = Inventory(max_weight=50.0)

    # Add items (pass ALL_ITEMS explicitly)
inventory.add_item("frostbrand", all_items)
inventory.add_item("minor_healing_potion", all_items, quantity=3)

    # Display
print(inventory.display(all_items))