import datetime

class InventoryManager:
    def __init__(self):
        self.inventory = {}  # {product_id: {"name": str, "quantity": int, "location": str, "supplier": str}}
        self.stock_receipts = []  # [{"receipt_id": str, "products": list, "date": datetime, "supplier": str}]
        self.supplies = {}  # {supply_id: {"name": str, "quantity": int, "threshold": int}}
        self.distribution_log = []  # [{"order_id": str, "products": list, "date": datetime, "customer": str}]

    def receive_goods(self, product_id: str, name: str, quantity: int, supplier: str) -> str:
        """Record incoming goods and update inventory."""
        if product_id in self.inventory:
            self.inventory[product_id]["quantity"] += quantity
        else:
            self.inventory[product_id] = {"name": name, "quantity": quantity, "location": "Pending", "supplier": supplier}
        return f"Received {quantity} units of {name} from {supplier}."

    def unload_and_shelve(self, product_id: str, location: str) -> str:
        """Assign a storage location to unloaded goods."""
        if product_id in self.inventory:
            self.inventory[product_id]["location"] = location
            return f"Shelved {self.inventory[product_id]['name']} at {location}."
        return f"Product ID {product_id} not found in inventory."

    def generate_stock_receipt(self, products: list, supplier: str) -> dict:
        """Generate a stock receipt for incoming goods."""
        receipt_id = f"REC{len(self.stock_receipts) + 1}"
        receipt = {
            "receipt_id": receipt_id,
            "products": products,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "supplier": supplier
        }
        self.stock_receipts.append(receipt)
        return receipt

    def manage_supplies(self, supply_id: str, name: str, quantity: int, threshold: int = 10) -> str:
        """Add or update supplies and set restocking thresholds."""
        if supply_id in self.supplies:
            self.supplies[supply_id]["quantity"] += quantity
        else:
            self.supplies[supply_id] = {"name": name, "quantity": quantity, "threshold": threshold}
        return f"Updated {name} supply. Current quantity: {self.supplies[supply_id]['quantity']}."

    def check_supply_levels(self) -> list:
        """Check which supplies are below threshold and need restocking."""
        low_supplies = []
        for supply_id, details in self.supplies.items():
            if details["quantity"] < details["threshold"]:
                low_supplies.append(f"{details['name']} (ID: {supply_id}) is low: {details['quantity']} < {details['threshold']}")
        return low_supplies if low_supplies else ["All supplies are adequately stocked."]

    def distribute_goods(self, order_id: str, products: list, customer: str) -> str:
        """Distribute goods to a customer and update inventory."""
        order_products = []
        for product_id, quantity in products:
            if product_id in self.inventory and self.inventory[product_id]["quantity"] >= quantity:
                self.inventory[product_id]["quantity"] -= quantity
                order_products.append((product_id, quantity))
            else:
                return f"Insufficient stock for {self.inventory.get(product_id, {'name': 'Unknown'})['name']}."

        log_entry = {
            "order_id": order_id,
            "products": order_products,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customer": customer
        }
        self.distribution_log.append(log_entry)
        return f"Order {order_id} fulfilled for {customer}."

    def get_inventory_status(self) -> dict:
        """Return the current inventory status."""
        return self.inventory

    def get_stock_receipts(self) -> list:
        """Return all stock receipts."""
        return self.stock_receipts

    def get_distribution_log(self) -> list:
        """Return the distribution log."""
        return self.distribution_log

# Example Usage
if __name__ == "__main__":
    manager = InventoryManager()

    # Receive and shelve goods
    print(manager.receive_goods("P001", "Laptop", 50, "TechSupplies Inc."))
    print(manager.unload_and_shelve("P001", "Aisle 5, Shelf 3"))

    # Generate stock receipt
    receipt = manager.generate_stock_receipt([("P001", 50)], "TechSupplies Inc.")
    print(f"Stock receipt generated: {receipt['receipt_id']}")

    # Manage supplies
    print(manager.manage_supplies("S001", "Packaging Boxes", 100, 20))
    print(manager.check_supply_levels())

    # Distribute goods
    print(manager.distribute_goods("ORD123", [("P001", 5)], "Customer A"))

    # Check inventory and logs
    print("\nCurrent Inventory:")
    print(manager.get_inventory_status())
    print("\nStock Receipts:")
    print(manager.get_stock_receipts())
    print("\nDistribution Log:")
    print(manager.get_distribution_log())
