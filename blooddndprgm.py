import csv
import os

# Donor Blood Type (Key) can safely donate to Recipient Blood Types (Values)
blood_compatibility = {
    "O-": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"], # Universal Donor
    "O+": ["O+", "A+", "B+", "AB+"],
    "A-": ["A-", "A+", "AB-", "AB+"],
    "A+": ["A+", "AB+"],
    "B-": ["B-", "B+", "AB-", "AB+"],
    "B+": ["B+", "AB+"],
    "AB-": ["AB-", "AB+"],
    "AB+": ["AB+"], # Universal Recipient
}

# Default starting inventory used if the CSV file doesn't exist
blood_inventory = {
    "O-": 15, "O+": 25, "A-": 10, "A+": 40, 
    "B-": 5, "B+": 12, "AB-": 8, "AB+": 18,
}

VALID_TYPES = list(blood_compatibility.keys())
CSV_FILE = 'blood_inventory.csv'

def save_inventory_to_csv(filepath, inventory):
    """Saves the current inventory dictionary back to the CSV file."""
    try:
        with open(filepath, mode='w', newline='') as file:
            fieldnames = ['blood_type', 'units']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for b_type, units in inventory.items():
                writer.writerow({'blood_type': b_type, 'units': units})
        print(f"\n[Inventory Updated]: Changes saved to {filepath}.")
    except Exception as e:
        print(f"\nError saving inventory to CSV: {e}")

def load_inventory_from_csv(filepath):
    """Loads the inventory from the CSV file, or creates it if not found."""
    if not os.path.exists(filepath):
        print(f"\n- Initial Setup -")
        print(f"File '{filepath}' not found. Creating it with default inventory.")
        save_inventory_to_csv(filepath, blood_inventory)
        return blood_inventory

    inventory = {}
    try:
        with open(filepath, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                blood_type = row.get('blood_type', '').upper().strip()
                try:
                    units = int(row.get('units', 0))
                    if blood_type in VALID_TYPES:
                        inventory[blood_type] = units
                except ValueError:
                    continue
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        print("Returning an empty inventory.")
        return {}
        
    return inventory

def display_inventory(inventory):
    """Displays the current state of the blood inventory."""
    print("\n- Current Blood Bank Inventory (Units) -")
    if not inventory:
        print("Inventory is empty.")
        return

    sorted_inventory = dict(sorted(inventory.items()))
    for b_type, units in sorted_inventory.items():
        print(f"| {b_type:<3}: {units:>5} Units |")
    print("------------------------------------------")

def add_new_units(inventory):
    print("\n- RECEIVING NEW BLOOD DONATIONS -")
    while True:
        b_type_input = input(f"Enter the Blood Type received ({', '.join(VALID_TYPES)}): ").upper().strip()
        if b_type_input in VALID_TYPES:
            break
        print(f"\nError: '{b_type_input}' is not a valid blood type. Please try again.")
    while True:
        units_input = input(f"Enter the number of units of {b_type_input} received: ")
        try:
            units_received = int(units_input)
            if units_received > 0:
                break
            print("Error: Units received must be a positive number.")
        except ValueError:
            print("Error: Please enter a valid whole number for units.")

    current_units = inventory.get(b_type_input, 0)
    inventory[b_type_input] = current_units + units_received
    
    save_inventory_to_csv(CSV_FILE, inventory)

    print(f"\nSUCCESS: Added {units_received} units of {b_type_input}. Total units now: {inventory[b_type_input]}.")
    display_inventory(inventory)
    
def check_compatible_blood(inventory):
    """Checks compatibility and dispenses stock for a recipient."""
    if not inventory:
        print("Inventory is empty. Please check the CSV file content.")
        return

    required_type = input(f"\nEnter the Recipient's required Blood Type ({', '.join(VALID_TYPES)}): ").upper().strip()

    if required_type not in VALID_TYPES:
        print(f"\nError: '{required_type}' is not a valid blood type. Please try again.")
        return

    print(f"\n- Searching for Compatible Blood for Recipient Type: {required_type} -")

    compatible_options = [
        donor_type for donor_type, can_donate_to in blood_compatibility.items() 
        if required_type in can_donate_to
    ]
    
    available_compatible_stock = {} 

    print(f"Compatible Donor Types Required: {', '.join(compatible_options)}")
    print("-" * 50)
    
    found_stock = False
    for donor_type in compatible_options:
        available_units = inventory.get(donor_type, 0) 
        
        if available_units > 0:
            match_status = "EXACT MATCH" if donor_type == required_type else "Compatible"
            print(f"FOUND STOCK: {donor_type} ({match_status}) - {available_units} Units Available.")
            available_compatible_stock[donor_type] = available_units
            found_stock = True
        
    if not found_stock:
        print(f"\nNo available stock found that is compatible with {required_type} at this time.")
        print("------------------------------------------------------------------")
        return
    print("\n- STOCK DISPENSING -")

    while True:
        selected_type = input("Enter the Blood Type to dispense (must have available stock above): ").upper().strip()
        if selected_type in available_compatible_stock:
            break
        print(f"Error: '{selected_type}' is either incompatible or has no available stock. Try again.")

    while True:
        max_units = available_compatible_stock[selected_type]
        units_input = input(f"Enter number of units of {selected_type} to dispense (Max: {max_units}): ")
        try:
            units_requested = int(units_input)
            if units_requested <= 0:
                print("Error: Units requested must be greater than zero.")
            elif units_requested <= max_units:
                break
            else:
                print(f"Error: Only {max_units} units of {selected_type} are available.")
        except ValueError:
            print("Error: Please enter a valid number for units.")

    inventory[selected_type] -= units_requested
    save_inventory_to_csv(CSV_FILE, inventory)

    print(f"\n DISPENSE SUCCESS: {units_requested} units of {selected_type} have been dispensed for {required_type} recipient.")

    display_inventory(inventory)

def main_menu():
    """Presents a menu for the user to interact with the system."""
    print("\nBlood Bank Inventory & Compatibility System")
    current_inventory = load_inventory_from_csv(CSV_FILE)
    while True:
        print("Select an action:")
        print("1. Display Current Inventory")
        print("2. Receive New Units (Add to Stock)")
        print("3. Dispense Units (Check Compatibility)")
        print("4. Exit System")
  
        choice = input("Enter your choice (1-4): ").strip()
        if choice == '1':
            display_inventory(current_inventory)
        elif choice == '2':
            add_new_units(current_inventory)
        elif choice == '3':
            check_compatible_blood(current_inventory)
        elif choice == '4':
            print("\nThank you for managing the blood bank inventory.")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")
if __name__ == "__main__":
    main_menu()