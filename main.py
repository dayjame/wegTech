# Load all items first
# Load items first
from src.items import load_all_items
from src.inventory import Inventory
from src.savetest import save_inventory
from src.savetest import load_inventory
from src.character import Character
from src.item_registry import ItemRegistry


# Initialize the registry (loads all items)
ItemRegistry()

# ALL_ITEMS = load_all_items()

# Create a character
kenshin = Character(name="Kenshin", base_stats={"agility": 15, "strength": 12})


# Create inventory
player_inventory = Inventory(max_weight=50.0)

# Add items by ID
player_inventory.add_item("frostbrand")
player_inventory.add_item("minor_healing_potion", quantity=3)

# Display
print(player_inventory.display())

"""
all_items = load_all_items()

# Initialize inventory
inventory = Inventory(max_weight=50.0)

# Add items (pass ALL_ITEMS explicitl
# y)
inventory.add_item("frostbrand", all_items)
inventory.add_item("minor_healing_potion", all_items, quantity=3)
inventory.add_item("chainmail_tunic", all_items)

# Display
print(inventory.display(all_items))

save_inventory(inventory)"""
