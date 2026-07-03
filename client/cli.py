import argparse, requests
from colorama import Fore


def main():
    base_url = "http://127.0.0.1:5000/api/products"

    parser = argparse.ArgumentParser(description='Inventory Management CLI')
    parser.add_argument('--add', '-a', type=int, help='Add a new item to the inventory, enter the barcode of the product to add')
    parser.add_argument('--remove', '-r', type=str, help='Remove an item from the inventory')
    parser.add_argument('--list', '-ls', action='store_true', help='List all items in the inventory')
    parser.add_argument('--update', '-u', type=str, help='Update an item in the inventory')
    parser.add_argument('--get', '-g', type=str, help='Get details of an item in the inventory')
    parser.add_argument('--low-stock', '-l', action='store_true', help='List all items in the inventory with low stock')

    args = parser.parse_args()

    if args.add:
        barcode = args.add
        response = requests.post(f"{base_url}", json={"barcode": barcode})
        if response.status_code == 200:
            print(Fore.GREEN + "Product added successfully!")
            print(response.json())
        else:
            print(Fore.RED + f"Failed to add product. Status code: {response.status_code}, Response: {response.text}")

    elif args.remove:
        product_id = args.remove
        response = requests.delete(f"{base_url}/{product_id}")
        if response.status_code == 200:
            print(Fore.GREEN + "Product removed successfully!")
        else:
            print(Fore.RED + f"Failed to remove product. Status code: {response.status_code}, Response: {response.text}")

    elif args.list:
        response = requests.get(base_url)
        if response.status_code == 200:
            products = response.json()
            if not products:
                print(Fore.YELLOW + "No products found in inventory.")
            else:
                print(Fore.BLUE + "Current Inventory:")
                for product in products:
                    print(f" Name: {product['name']}")
        else:
            print(Fore.RED + f"Failed to fetch products. Status code: {response.status_code}, Response: {response.text}")

    elif args.update:
        product_id = args.update
        name = input(Fore.CYAN + "Enter new name (leave blank to keep current): ")
        price = input(Fore.CYAN + "Enter new price (leave blank to keep current): ")
        barcode = input(Fore.CYAN + "Enter new barcode (leave blank to keep current): ")

        data = {}
        if name:
            data['name'] = name
        if price:
            try:
                data['price'] = float(price)
            except ValueError:
                print(Fore.RED + "Invalid price. Please enter a numeric value.")
                return
        if barcode:
            data['barcode'] = barcode

        if not data:
            print(Fore.YELLOW + "No updates provided.")
            return

        response = requests.patch(f"{base_url}/{product_id}", json=data)
        if response.status_code == 200:
            print(Fore.GREEN + "Product updated successfully!")
            print(response.json())
        else:
            print(Fore.RED + f"Failed to update product. Status code: {response.status_code}, Response: {response.text}")

    elif args.get:
        product_id = args.get
        response = requests.get(f"{base_url}/{product_id}")
        if response.status_code == 200:
            product = response.json()
            print(Fore.BLUE + f"Product Details: ID: {product['id']}, Name: {product['name']}, Price: ${product['price']}, Barcode: {product['barcode']} Quantity: {product.get('quantity')}")
        else:
            print(Fore.RED + f"Failed to fetch product details. Status code: {response.status_code}, Response: {response.text}")

    elif args.low_stock:
        response = requests.get(f"{base_url}/low-stock")
        if response.status_code == 200:
            low_stock_products = response.json()
            if not low_stock_products:
                print(Fore.YELLOW + "No low stock products found.")
            else:
                print(Fore.BLUE + "Low Stock Products:")
                for product in low_stock_products:
                    print(Fore.BLUE + f" ID: {product['id']}, Name: {product['name']}, Price: ${product['price']}, Barcode: {product['barcode']}, Quantity: {product.get('quantity')}")
        else:
            print(Fore.RED + f"Failed to fetch low stock products. Status code: {response.status_code}, Response: {response.text}")

    


if __name__ == "__main__":
    main()
    
