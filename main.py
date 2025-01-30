# Load all items first
# Load items first
from src.items import load_all_items
from src.inventory import Inventory
from src.savetest import save_inventory
from src.savetest import load_inventory
from src.character import Character

ALL_ITEMS = load_all_items()

# Create a character
kenshin = Character(name="Kenshin", base_stats={"agility": 15, "strength": 12})

# Add items to inventory
kenshin.inventory.add_item("stormcaller_katana", ALL_ITEMS)
kenshin.inventory.add_item("blessed_bandage", ALL_ITEMS, quantity=2)

# Equip the katana
kenshin.equip("stormcaller_katana")

# Check effective stats
print(kenshin.effective_stats["agility"])  # 15 (base) + 12 (katana) = 27

# Apply poison status (agility penalty)
kenshin.apply_status_effect(
    effect_id="poison",
    duration=3,
    stat_modifiers={"agility": -5}
)
print(kenshin.effective_stats["agility"])  # 27 - 5 = 22

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
