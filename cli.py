import argparse, requests


def main():
    base_url = "http://127.0.0.1:5000/api/products"

    parser = argparse.ArgumentParser(description='Inventory Management CLI')
    parser.add_argument('--add', type=int, help='Add a new item to the inventory, enter the barcode of the product to add')
    parser.add_argument('--remove', type=str, help='Remove an item from the inventory')
    parser.add_argument('--list', action='store_true', help='List all items in the inventory')
    # parser.add_argument('--update', type=str, help='Update an item in the inventory')
    # parser.add_argument('--get', type=str, help='Get details of an item in the inventory')

    args = parser.parse_args()

    if args.add:
        barcode = args.add
        response = requests.post(f"{base_url}", json={"barcode": barcode})
        if response.status_code == 200:
            print("Product added successfully!")
            print(response.json())
        else:
            print(f"Failed to add product. Status code: {response.status_code}, Response: {response.text}")

    elif args.remove:
        product_id = args.remove
        response = requests.delete(f"{base_url}/{product_id}")
        if response.status_code == 200:
            print("Product removed successfully!")
        else:
            print(f"Failed to remove product. Status code: {response.status_code}, Response: {response.text}")

    elif args.list:
        response = requests.get(base_url)
        if response.status_code == 200:
            products = response.json()
            if not products:
                print("No products found in inventory.")
            else:
                print("Current Inventory:")
                for product in products:
                    print(f"ID: {product['id']}, Name: {product['name']}, Price: ${product['price']}")
        else:
            print(f"Failed to fetch products. Status code: {response.status_code}, Response: {response.text}")



if __name__ == "__main__":
    main()

# BASE_URL = "http://127.0.0.1:5000/inventory"  # Adjust based on your Flask routes

# def display_menu():
#     print("\n=== Inventory Management Admin Portal ===")
#     print("1. View All Inventory Items")
#     print("2. Search Product (via External API/Local)")
#     print("3. Add New Product")
#     print("4. Update Product (Patch)")
#     print("5. Delete Product")
#     print("6. Exit")

# def view_all_items():
#     try:
#         response = requests.get(BASE_URL)
#         if response.status_code == 200:
#             items = response.json()
#             if not items:
#                 print("No items found in inventory.")
#                 return
#             print("\n--- Current Inventory ---")
#             for item in items:
#                 print(f"ID: {item['id']} | Name: {item['name']} | Qty: {item['quantity']} | Price: ${item['price']}")
#         else:
#             print(f"Failed to fetch inventory. Server responded with status: {response.status_code}")
#     except requests.exceptions.ConnectionError:
#         print("Error: Could not connect to the Flask server. Is it running?")

# def add_product():
#     print("\n--- Add New Product ---")
#     name = input("Enter product name: ")
#     quantity = int(input("Enter quantity: "))
#     price = float(input("Enter price: "))
    
#     payload = {
#         "name": name,
#         "quantity": quantity,
#         "price": price
#     }
    
#     response = requests.post(BASE_URL, json=payload)
#     if response.status_code == 201:
#         print(f"Success: {name} added to inventory!")
#     else:
#         print(f"Error {response.status_code}: {response.text}")

# def update_product():
#     print("\n--- Update Product ---")
#     product_id = input("Enter the ID of the product to update: ")
#     print("Leave field blank if you do not want to change it.")
    
#     name = input("Enter new name: ")
#     quantity = input("Enter new quantity: ")
#     price = input("Enter new price: ")
    
#     # Dynamically build payload for PATCH (only update what changed)
#     payload = {}
#     if name: payload["name"] = name
#     if quantity: payload["quantity"] = int(quantity)
#     if price: payload["price"] = float(price)
    
#     if not payload:
#         print("No changes specified.")
#         return

#     response = requests.patch(f"{BASE_URL}/{product_id}", json=payload)
#     if response.status_code == 200:
#         print("Product updated successfully!")
#     else:
#         print(f"Error {response.status_code}: {response.text}")

# def delete_product():
#     print("\n--- Delete Product ---")
#     product_id = input("Enter the ID of the product to delete: ")
    
#     confirm = input(f"Are you sure you want to delete product {product_id}? (y/n): ")
#     if confirm.lower() == 'y':
#         response = requests.delete(f"{BASE_URL}/{product_id}")
#         if response.status_code == 204 or response.status_code == 200:
#             print("Product deleted successfully.")
#         else:
#             print(f"Error {response.status_code}: {response.text}")

# def main():
#     while True:
#         display_menu()
#         choice = input("\nSelect an option (1-6): ").strip()
        
#         if choice == "1":
#             view_all_items()
#         elif choice == "2":
#             # This is where your external API search integration function will go
#             print("Feature coming soon: External API Lookup")
#         elif choice == "3":
#             add_product()
#         elif choice == "4":
#             update_product()
#         elif choice == "5":
#             delete_product()
#         elif choice == "6":
#             print("Exiting Admin Portal. Goodbye!")
#             break
#         else:
#             print("Invalid choice. Please select a valid option.")

# if __name__ == "__main__":
#     main()
    
# def fetch_external_product():
#     barcode = input("Enter product barcode to search: ")
#     # Hit an endpoint on your Flask server that handles the OpenFoodFacts request
#     response = requests.get(f"http://127.0.0.1:5000/external/product/{barcode}")
    
#     if response.status_code == 200:
#         product_data = response.json()
#         print(f"\nFound Product: {product_data['product_name']}")
        
#         save = input("Do you want to add this product to your inventory? (y/n): ")
#         if save.lower() == 'y':
#             # Post this data back to your local database route
#             requests.post(BASE_URL, json={
#                 "name": product_data['product_name'],
#                 "quantity": 1, 
#                 "price": 0.00  # Admin can update this later via patch
#             })
#     else:
#         print("Product not found or external API error.")