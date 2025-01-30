import json


class Item:
    def __init__(self, item_id: str, name: str, item_type: str, description: str, weight: float, value: int):
        self.id = item_id  # Unique identifier (e.g., "sword")
        self.name = name
        self.item_type = item_type
        self.description = description
        self.weight = weight
        self.value = value


def load_items(filename: str = "data/items/weapons.json") -> dict:
    """Load all items from a JSON file into a dictionary."""
    with open(filename, 'r') as f:
        item_data = json.load(f)

    items = {}
    for item_id, data in item_data.items():
        items[item_id] = Item(
            item_id=item_id,
            name=data["name"],
            item_type=data["type"],
            description=data["description"],
            weight=data["weight"],
            value=data["value"]
        )
    return items


# Load all items at game startup
ALL_ITEMS = load_items()


class Inventory:
    def __init__(self, max_weight: float = None, max_slots: int = 10):
        self.items = []
        self.max_weight = max_weight
        self.max_slots = max_slots

    def add_item(self, item: Item) -> bool:
        """Add an item to the inventory if there's space."""
        if self._check_can_add(item):
            self.items.append(item)
            return True
        return False

    def remove_item(self, item_name: str) -> bool:
        """Remove an item by name."""
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                return True
        return False

    def get_total_weight(self) -> float:
        """Calculate total weight of the inventory."""
        return sum(item.weight for item in self.items)

    def _check_can_add(self, item: Item) -> bool:
        """Check if the item can be added (weight/slots)."""
        if self.max_slots and len(self.items) >= self.max_slots:
            print("Inventory slots full!")
            return False
        if self.max_weight and (self.get_total_weight() + item.weight) > self.max_weight:
            print("Inventory too heavy!")
            return False
        return True

    def display(self):
        """Print the inventory contents."""
        if not self.items:
            print("Inventory is empty.")
            return
        print("Inventory Contents:")
        for item in self.items:
            print(f"- {item.name} ({item.item_type}, {item.weight} kg)")
        print(f"Total Weight: {self.get_total_weight()} kg")

    def to_dict(self) -> dict:
        """Convert the inventory and its items to a dictionary for JSON serialization."""
        return {
            "max_weight": self.max_weight,
            "max_slots": self.max_slots,
            "items": [vars(item) for item in self.items]  # Convert each Item to a dict
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Inventory':
        """Create an Inventory from a dictionary (loaded from JSON)."""
        inventory = cls(max_weight=data["max_weight"], max_slots=data["max_slots"])
        for item_data in data["items"]:
            item = Item(**item_data)  # Reconstruct Item objects
            inventory.items.append(item)
        return inventory


def save_inventory(inventory: Inventory, filename: str = "save.json"):
    """Save the inventory to a JSON file."""
    data = inventory.to_dict()
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Inventory saved to {filename}!")


def load_inventory(filename: str = "save.json") -> Inventory:
    """Load the inventory from a JSON file."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return Inventory.from_dict(data)
    except FileNotFoundError:
        print("No save file found. Creating a new inventory.")
        return Inventory()


# Create an inventory and add items
player_inventory = Inventory(max_weight=10)
player_inventory.add_item(ALL_ITEMS["iron_sword"])
player_inventory.add_item(ALL_ITEMS["bow"])

player_inventory.display()

# Save to JSON
save_inventory(player_inventory, "save.json")

# Later, load the saved inventory
loaded_inventory = load_inventory("save.json")
loaded_inventory.display()
