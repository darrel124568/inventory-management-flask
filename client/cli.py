import argparse, requests


def main():
    base_url = "http://127.0.0.1:5000/api/products"

    parser = argparse.ArgumentParser(description='Inventory Management CLI')
    parser.add_argument('--add', type=int, help='Add a new item to the inventory, enter the barcode of the product to add')
    parser.add_argument('--remove', type=str, help='Remove an item from the inventory')
    parser.add_argument('--list', action='store_true', help='List all items in the inventory')
    parser.add_argument('--update', type=str, help='Update an item in the inventory')
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

    elif args.update:
        product_id = args.update
        name = input("Enter new name (leave blank to keep current): ")
        price = input("Enter new price (leave blank to keep current): ")

        data = {}
        if name:
            data['name'] = name
        if price:
            try:
                data['price'] = float(price)
            except ValueError:
                print("Invalid price. Please enter a numeric value.")
                return

        if not data:
            print("No updates provided.")
            return

        response = requests.patch(f"{base_url}/{product_id}", json=data)
        if response.status_code == 200:
            print("Product updated successfully!")
            print(response.json())
        else:
            print(f"Failed to update product. Status code: {response.status_code}, Response: {response.text}")

    


if __name__ == "__main__":
    main()
    
