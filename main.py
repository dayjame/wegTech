# Load all items first
# Load items first
from src.items import load_all_items
from src.inventory import Inventory
from src.savetest import save_inventory
from src.savetest import load_inventory
from src.character import Character
from src.item_registry import ItemRegistry


from src.item_registry import ItemRegistry
from src.character import Character

def main():
    # Initialize registry (loads all items)
    ItemRegistry()

    # Create character with partial base stats
    playerCharacter = Character(
        name="Leidy",
        base_stats={"intelligence": 18, "strength": 14, "endurance": 12}
    )

    # Add items to inventory
    playerCharacter.inventory.add_item("stormcaller_katana")
    playerCharacter.inventory.add_item("iron_sword")
    playerCharacter.inventory.add_item("minor_healing_potion", quantity=3)
    playerCharacter.inventory.add_item("leather_chestplate")

    # Attempt to equip items
    print("\n=== Equip Attempts ===")
    playerCharacter.equip("stormcaller_katana")  # Should succeed
    playerCharacter.equip("iron_sword")          # Should unequip the first sword

    # Display final state
    print("\n=== Final Stats ===")
    print(f"{playerCharacter.name}'s stats:")
    print(f"HP: {playerCharacter.hp}/{playerCharacter.max_hp}")
    print(f"Effective Strength: {playerCharacter.effective_stats['strength']}")
    print(f"Effective Agility: {playerCharacter.effective_stats['agility']}")

    print("\n=== Final Inventory ===")
    print(playerCharacter.inventory.display())

if __name__ == "__main__":
    main()

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
