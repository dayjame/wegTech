import json

"""class Item:
    def __init__(self, name: str, item_type: str, description: str = "", weight: float = 0.0, value: int = 0):
        self.name = name
        self.item_type = item_type  # e.g., "weapon", "potion", "key"
        self.description = description
        self.weight = weight
        self.value = value

    def __repr__(self):
        return f"{self.name} ({self.item_type})"""



#class Inventory:
    def __init__(self, max_weight: float = None, max_slots: int = 10):
        self.items = []  # List of Item objects
        self.max_weight = max_weight  # Optional weight limit
        self.max_slots = max_slots  # Optional slot limit

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

def save_inventory(inventory: Inventory, filename: str):
    data = {
        "items": [
            {
                "name": item.name,
                "type": item.item_type,
                "weight": item.weight,
                "value": item.value,
                "description": item.description
            } for item in inventory.items
        ],
        "max_weight": inventory.max_weight,
        "max_slots": inventory.max_slots
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def load_inventory(filename: str) -> Inventory:
    with open(filename, 'r') as f:
        data = json.load(f)
    inventory = Inventory(max_weight=data["max_weight"], max_slots=data["max_slots"])
    for item_data in data["items"]:
        item = Item(**item_data)
        inventory.add_item(item)
    return inventory


# Create items
sword = Item("weapon", "A sharp blade.", weight=2.5, value=50)
potion = Item("Health Potion", "potion", "Restores 20 HP.", weight=0.5, value=10)
key = Item("Rusty Key", "key", "Opens old doors.", weight=0.1, value=5)

# Create an inventory with a weight limit of 5 kg and 4 slots
player_inventory = Inventory(max_weight=10, max_slots=4)

# Add items
player_inventory.add_item(sword)  # Success
player_inventory.add_item(potion) # Success
player_inventory.add_item(key)    # Success
player_inventory.add_item(Item("Shield", "armor", weight=3.0))  # Fails (total weight exceeds 5 kg)

player_inventory.display()

# Remove an item
player_inventory.remove_item("Health Potion")

# Display inventory
player_inventory.display()

save_inventory(player_inventory, "../inventory.json")