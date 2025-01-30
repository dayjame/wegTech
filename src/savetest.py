import json
from pathlib import Path
from typing import Dict
from src.items import Item  # Import your Item class
from src.inventory import Inventory  # Import your Inventory class

def save_inventory(
    inventory: Inventory,
    filename: str = "save.json",
    save_dir: str = "saves"
) -> bool:
    """Save the inventory to a JSON file."""
    try:
        # Create saves directory if it doesn't exist
        project_root = Path(__file__).parent.parent
        save_path = project_root / save_dir
        save_path.mkdir(exist_ok=True)

        # Serialize inventory and write to file
        data = inventory.to_dict()
        with open(save_path / filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving inventory: {e}")
        return False

def load_inventory(
    filename: str = "save.json",
    save_dir: str = "saves",
    all_items: Dict[str, Item] = None
) -> Inventory:
    """Load the inventory from a JSON file."""
    try:
        project_root = Path(__file__).parent.parent
        save_path = project_root / save_dir / filename

        if not save_path.exists():
            print("No save file found. Creating a new inventory.")
            return Inventory()

        with open(save_path, 'r') as f:
            data = json.load(f)

        # Deserialize inventory
        inventory = Inventory.from_dict(data, all_items)
        return inventory
    except json.JSONDecodeError:
        print("Error: Save file is corrupted.")
        return Inventory()
    except Exception as e:
        print(f"Error loading inventory: {e}")
        return Inventory()