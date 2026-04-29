# Create file paths for the JSON data file and the text report file.
# These files will be stored in the same folder as the Python program.
DATA_FILE = Path(__file__).with_name("inventory_data.json")
REPORT_FILE = Path(__file__).with_name("inventory_report.txt")


def load_inventory() -> list:
"""Load inventory items from the JSON data file."""
# If the file does not exist yet, return an empty list.
if not DATA_FILE.exists():
return []

try:
# Open the JSON file and load the saved inventory data.
with open(DATA_FILE, "r", encoding="utf-8") as file:
data = json.load(file)

# Make sure the loaded data is a list before returning it.
return data if isinstance(data, list) else []

# If the file is invalid or cannot be read, return an empty list.
except (json.JSONDecodeError, OSError):
return []


def save_inventory(items: list) -> None:
"""Save inventory items to the JSON data file."""
# Write the current inventory list into the JSON file.
with open(DATA_FILE, "w", encoding="utf-8") as file:
json.dump(items, file, indent=4)


def print_header(title: str) -> None:
"""Display a formatted section header."""
print("\n" + "=" * 72)
print(title.center(72))
print("=" * 72)


def pause() -> None:
"""Pause the program until the user presses Enter."""
input("\nPress Enter to continue...")


def get_next_id(items: list) -> int:
"""Generate the next item ID."""
# If there are no items yet, start IDs at 1.
if not items:
return 1

# Otherwise, return one greater than the current highest ID.
return max(item["id"] for item in items) + 1


def prompt_non_empty(message: str) -> str:
"""Prompt the user until a non-empty value is entered."""
while True:
value = input(message).strip()
if value:
return value
print("Input cannot be empty. Please try again.")


def prompt_int(message: str, allow_zero: bool = True) -> int:
"""Prompt the user for a valid integer."""
while True:
value = input(message).strip()
try:
number = int(value)

# Reject negative values.
if number < 0:
print("Please enter 0 or a positive whole number.")

# Reject zero if allow_zero is False.
elif not allow_zero and number == 0:
print("Value must be greater than 0.")
else:
return number

# Handle invalid input that cannot be converted to an integer.
except ValueError:
print("Please enter a valid whole number.")


def prompt_float(message: str, allow_zero: bool = True) -> float:
"""Prompt the user for a valid decimal number."""
while True:
value = input(message).strip()
try:
number = float(value)

# Reject negative numbers.
if number < 0:
print("Please enter 0 or a positive number.")

# Reject zero if allow_zero is False.
elif not allow_zero and number == 0:
print("Value must be greater than 0.")
else:
return round(number, 2)

# Handle invalid input that cannot be converted to a float.
except ValueError:
print("Please enter a valid number.")


def prompt_date(message: str) -> str:
"""Prompt the user for a date in YYYY-MM-DD format."""
while True:
value = input(message).strip()
try:
# Validate the date format using datetime.
parsed_date = datetime.strptime(value, "%Y-%m-%d")
return parsed_date.strftime("%Y-%m-%d")
except ValueError:
print("Invalid date. Use YYYY-MM-DD format.")


def find_item_by_id(items: list, item_id: int):
"""Find and return an item by its ID."""
for item in items:
if item["id"] == item_id:
return item
return None


def add_item(items: list) -> None:
"""Add a new item to the inventory."""
print_header("Add New Inventory Item")

# Ask the user to enter information for the new item.
name = prompt_non_empty("Enter item name: ").title()
category = prompt_non_empty("Enter category: ").title()
quantity = prompt_int("Enter quantity: ")
price = prompt_float("Enter price per item: $")
reorder_level = prompt_int("Enter reorder level: ")
supplier = input("Enter supplier name (optional): ").strip().title()
date_added = prompt_date("Enter date added (YYYY-MM-DD): ")

# Create a dictionary to store the new item.
item = {
"id": get_next_id(items),
"name": name,
"category": category,
"quantity": quantity,
"price": price,
"reorder_level": reorder_level,
"supplier": supplier,
"date_added": date_added,
}

# Add the new item to the list and save the updated inventory.
items.append(item)
save_inventory(items)
print("\nInventory item added successfully.")


def view_inventory(items: list) -> None:
"""Display all inventory items."""
print_header("Current Inventory")

# If there are no items, show a message and return.
if not items:
print("No inventory items found.")
return

# Print a table header.
header = f"{'ID':<5}{'Name':<18}{'Category':<16}{'Qty':<8}{'Price':<12}{'Value':<12}{'Reorder':<10}Supplier"
print(header)
print("-" * 72)

# Sort items alphabetically by name before displaying.
for item in sorted(items, key=lambda entry: entry["name"].lower()):
value = item["quantity"] * item["price"]

# Print each item in a formatted row.
print(
f"{item['id']:<5}"
f"{item['name'][:17]:<18}"
f"{item['category'][:15]:<16}"
f"{item['quantity']:<8}"
f"${item['price']:<11.2f}"
f"${value:<11.2f}"
f"{item['reorder_level']:<10}"
f"{item['supplier'][:15]}"
)


def update_quantity(items: list) -> None:
"""Update the quantity of an existing inventory item."""
print_header("Update Item Quantity")

# If inventory is empty, there is nothing to update.
if not items:
print("No inventory items available.")
return

# Show current inventory first so the user can choose an ID.
view_inventory(items)
item_id = prompt_int("\nEnter the item ID to update: ", allow_zero=False)
item = find_item_by_id(items, item_id)

# If the ID is not found, show an error.
if not item:
print("Item ID not found.")
return

# Show update options.
print(f"\nSelected item: {item['name']}")
print("1. Restock item")
print("2. Reduce quantity after sale/use")
choice = input("Choose an option: ").strip()

if choice == "1":
# Add stock to the existing quantity.
amount = prompt_int("Enter amount to add: ", allow_zero=False)
item["quantity"] += amount
save_inventory(items)
print("Quantity updated successfully.")

elif choice == "2":
# Subtract stock, but do not allow quantity to go below zero.
amount = prompt_int("Enter amount to subtract: ", allow_zero=False)
if amount > item["quantity"]:
print("Cannot subtract more than the current quantity.")
else:
item["quantity"] -= amount
save_inventory(items)
print("Quantity updated successfully.")
else:
print("Invalid option.")


def search_inventory(items: list) -> None:
"""Search inventory by item name or category."""
print_header("Search Inventory")

# If inventory is empty, there is nothing to search.
if not items:
print("No inventory items available.")
return

# Get the search keyword from the user.
keyword = input("Enter item name or category to search: ").strip().lower()

# Find all items where the keyword appears in the name or category.
matches = [
item for item in items
if keyword in item["name"].lower() or keyword in item["category"].lower()
]

# If no items match, show a message.
if not matches:
print("No matching inventory items found.")
return

print(f"\nFound {len(matches)} matching item(s):")
header = f"{'ID':<5}{'Name':<18}{'Category':<16}{'Qty':<8}{'Price':<12}{'Supplier'}"
print(header)
print("-" * 72)

# Display all matching items.
for item in matches:
print(
f"{item['id']:<5}"
f"{item['name'][:17]:<18}"
f"{item['category'][:15]:<16}"
f"{item['quantity']:<8}"
f"${item['price']:<11.2f}"
f"{item['supplier'][:20]}"
)


def remove_item(items: list) -> None:
"""Remove an item from the inventory."""
print_header("Remove Inventory Item")

# If there are no items, nothing can be removed.
if not items:
print("No inventory items to remove.")
return

# Show inventory and ask the user which item to remove.
view_inventory(items)
item_id = prompt_int("\nEnter the item ID to remove: ", allow_zero=False)
item = find_item_by_id(items, item_id)

# If the ID does not exist, show an error.
if not item:
print("Item ID not found.")
return

# Ask the user to confirm deletion.
confirm = input(f"Are you sure you want to remove '{item['name']}'? (y/n): ").strip().lower()
if confirm == "y":
items.remove(item)
save_inventory(items)
print("Item removed successfully.")
else:
print("Removal canceled.")


def inventory_summary(items: list) -> None:
"""Display a summary of the inventory."""
print_header("Inventory Summary")

# If no data exists, show a message.
if not items:
print("No inventory data available.")
return

# Calculate overall totals.
total_items = len(items)
total_quantity = sum(item["quantity"] for item in items)
total_value = sum(item["quantity"] * item["price"] for item in items)

# Find low-stock items where quantity is less than or equal to reorder level.
low_stock_items = [item for item in items if item["quantity"] <= item["reorder_level"]]

# Display summary statistics.
print(f"Total unique items: {total_items}")
print(f"Total quantity in stock: {total_quantity}")
print(f"Total inventory value: ${total_value:.2f}")
print(f"Low-stock items: {len(low_stock_items)}")

# Display low-stock item details.
if low_stock_items:
print("\nItems that need restocking:")
for item in low_stock_items:
print(
f"- {item['name']} | Quantity: {item['quantity']} | "
f"Reorder level: {item['reorder_level']}"
)


def export_report(items: list) -> None:
"""Export an inventory report to a text file."""
print_header("Export Inventory Report")

# Calculate summary information for the report.
total_items = len(items)
total_quantity = sum(item["quantity"] for item in items)
total_value = sum(item["quantity"] * item["price"] for item in items)
low_stock_items = [item for item in items if item["quantity"] <= item["reorder_level"]]

# Build report lines as a list of strings.
lines = [
"INVENTORY MANAGER REPORT",
"=" * 50,
f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
f"Total unique items: {total_items}",
f"Total quantity in stock: {total_quantity}",
f"Total inventory value: ${total_value:.2f}",
"",
"LOW-STOCK ITEMS",
"-" * 50,
]

# Add low-stock items to the report.
if low_stock_items:
for item in low_stock_items:
lines.append(
f"{item['name']} | Qty: {item['quantity']} | Reorder level: {item['reorder_level']}"
)
else:
lines.append("No low-stock items.")

# Add full inventory list to the report.
lines.extend(["", "FULL INVENTORY LIST", "-" * 50])
for item in sorted(items, key=lambda entry: entry["name"].lower()):
item_value = item["quantity"] * item["price"]
lines.append(
f"ID {item['id']} | {item['name']} | Category: {item['category']} | "
f"Qty: {item['quantity']} | Price: ${item['price']:.2f} | Value: ${item_value:.2f}"
)

# Write the report to a text file.
with open(REPORT_FILE, "w", encoding="utf-8") as file:
file.write("\n".join(lines))

print(f"Report exported successfully to {REPORT_FILE.name}.")


def display_menu() -> None:
"""Display the main menu options."""
print_header("Inventory Manager")
print("1. Add a new inventory item")
print("2. View all inventory items")
print("3. Update item quantity")
print("4. Search inventory")
print("5. Remove an item")
print("6. View inventory summary")
print("7. Export inventory report")
print("8. Exit")


def main() -> None:
"""Run the main program loop."""
# Load the existing inventory data when the program starts.
items = load_inventory()

while True:
display_menu()
choice = input("Enter your choice (1-8): ").strip()

# Run the appropriate function based on the user's choice.
if choice == "1":
add_item(items)
pause()
elif choice == "2":
view_inventory(items)
pause()
elif choice == "3":
update_quantity(items)
pause()
elif choice == "4":
search_inventory(items)
pause()
elif choice == "5":
remove_item(items)
pause()
elif choice == "6":
inventory_summary(items)
pause()
elif choice == "7":
export_report(items)
pause()
elif choice == "8":
print("\nThank you for using Inventory Manager.")
break
else:
print("\nInvalid choice. Please enter a number from 1 to 8.")
pause()


# Start the program only when this file is run directly.
if __name__ == "__main__":
main()
