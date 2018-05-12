'''
File       : grocery_store.py
Created By : Anurag Gupta
Created On : 12 May 2018
Description: A simple script to manage the store's transactions
'''
import pprint
from datetime import datetime

class Inventory:
    '''
    Creates & manages inventory
    '''
    __inventory_list = 0
    __items_sold = 0

    def __init__(self):
        self.__inventory_list = []
        self.__items_sold = []

    def display_inventory(self):
        '''
        Displays the inventory
        '''
        print("\n{0:^95}".format("INVENTORY:"))
        print("{plus}{hyphens}{plus}".format(plus = '+', hyphens = '-'*90))
        print("| {0:^10} | {1:^10} | {2:^10} | {3:^10} | {4:^10} | {5:^10} | {6:^10} |".format("Item No.", "Item", "Category", "Quantity", "Price", "Sold", "Total"))
        print("{plus}{hyphens}{plus}".format(plus = '+', hyphens = '-'*90))
        for items in self.__inventory_list:
            print("| {0:^10} | {1:^10} | {2:^10} | {3:^10} | {4:^10} | {5:^10} | {6:^10} |".format(items['id'], items['item'], items['category'], items['quantity'], items['price'], items['sold'], items['left']))
            print("{plus}{hyphens}{plus}".format(plus = '+', hyphens = '-'*90))

    def get_items_list(self):
        return self.__inventory_list
    
    def update_inventory(self, list_of_items_sold):
        for items in list_of_items_sold:
            for item_index in range(len(self.__inventory_list)):
                if items['id'] == self.__inventory_list[item_index]['id']:
                    self.__inventory_list[item_index]['sold'] += items['quantity']
                    self.__inventory_list[item_index]['left'] -= items['quantity']
    
    def insert_items_into_inventory(self, items_list):
        '''
        Simply inserts the items into inventory
        '''
        for items in items_list:
            self.__inventory_list.append(items)
    
    def validate_items(self, item, quantity):
        '''
        checks whether the item to be sold has right amount quantity
        in the inventory.
        '''
        is_sufficient = False
        for items in self.__inventory_list:
            if items['item'] == item and items['left'] >= quantity:
                is_sufficient = True
                break
        return is_sufficient
    
    def update_items_sold_list(self, items_list):
        '''
        '''
        # check if the __items_sold is empty
        if self.__items_sold == []:
            for items in items_list:
                self.__items_sold.append(items)
        else:
            # check if the item already present in the items_sold list
            # If so, then update the particular items 'sold' & 'left' parameter
            item_found = False
            for items in items_list:
                for item_index in range(len(self.__items_sold)):
                    if items['item'] == self.__items_sold[item_index]["item"]:
                        self.__items_sold[item_index]["quantity"] += items['quantity']
                        item_found = True
                        break;
                if item_found is False:
                    self.__items_sold.append(items)

class Registers:
    '''
    '''
    pass
    
class Store:
    '''
    '''
    __inventory = None
    __register_1 = None
    __register_2 = None

    def __init__(self):
        self.__inventory = Inventory()
        self.__register_1 = Registers()
        self.__register_2 = Registers()
    
    def initialize_inventory(self, items_list):
        self.__inventory.insert_items_into_inventory(items_list)

    def display_inventory(self):
        self.__inventory.display_inventory()
    
    def update_inventory(self, items_list):
        self.__inventory.update_inventory(items_list)

class GroceryStore(Store):
    '''
    '''
    __balance = 0
    __total_sale_amount = 0
    __cart = None
    __transactions = None

    def __init__(self, items_list):
        super().__init__()
        self.__transactions = Transactions()
        self.init_grocery_store(items_list)
        self.__cart = []
    
    def init_grocery_store(self, items_list):
        self._Store__inventory.insert_items_into_inventory(items_list)
    
    @property
    def sale_amount(self):
        return self.__total_sale_amount

    @sale_amount.setter
    def sale_amount(self, amount):
        self.__total_sale_amount += amount

    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, balance):
        self.__balance += balance

    def add_to_cart(self, items):
        '''
        Adds items to cart
        '''
        print('\nAdding items to cart...')
        # get available items list from inventory
        items_in_inventory = self._Store__inventory.get_items_list()
        # loop through each items selected by customer, validate it 
        # & add it to cart
        for item in items:
            if self._Store__inventory.validate_items(item[0], item[1]):
                for item_index in range(len(items_in_inventory)):
                    if item[0] == items_in_inventory[item_index]['item']:
                        cart_obj = { 
                            'id': items_in_inventory[item_index]['id'],
                            'item': item[0],
                            'quantity': item[1],
                            'price': items_in_inventory[item_index]['price'],
                            'amount': items_in_inventory[item_index]['price'] * item[1]
                        }
                        self.__cart.append(cart_obj)
                        del cart_obj
                        break
            else:
                print("\nError: Insufficient quantity:")
                print("The availability of {} is less than the quantity purchased.".format(item[0]))
                print("Removing {} from cart...".format(item[0]))
        
        print("\tItems added successfully.")

    def total_amount(self, items_in_cart):
        '''
        Calculate the total amount for the items in cart
        '''
        items_in_inventory = self._Store__inventory.get_items_list()
        total_amount = 0
        for cart_item in items_in_cart:
            for inventory_item in items_in_inventory:
                if cart_item['item'] == inventory_item["item"]:
                    total_amount += cart_item['amount']
                    break;
        return total_amount
    
    def checkout(self, customer):
        '''
        Check out the items purchased by the customer.
        It accepts customer object as input
        '''
        print("\nChecking out items...")

        # calculate total amount to be paid by customer
        total_amount_to_be_paid = self.total_amount(self.__cart)
        # validate that customer has enough amount to purchase
        # the items
        if customer.validate_balance(total_amount_to_be_paid) is True:
            # start transaction
            self.__transactions.do_transacton(customer, total_amount_to_be_paid, datetime.now().isoformat(sep=' ', timespec='seconds'))
            # update sale amount
            self.sale_amount += total_amount_to_be_paid
            # update store's balance
            self.balance += total_amount_to_be_paid
            # update inventories
            self._Store__inventory.update_items_sold_list(self.__cart)
            self._Store__inventory.update_inventory(self.__cart)
            # generate biil
            self.generate_bill()
            return customer.balance - total_amount_to_be_paid
        else:
            print("Error: Customer does not enough money to make the purchase.")

    def generate_bill(self):
        '''
        Simply generates the bill for the items purchased
        '''
        print("\n{0:^79}".format("BILL:"))
        print("{plus}{hyphens}{plus}".format(plus = '+', hyphens = '-'*79))
        print("| {0:^10} | {1:^10} | {2:^10} | {3:^10} | {4:^10} | {5:^10} |".format("Sr. No.", "Item", "Quantity", "Price", "Discount", "Total Amount"))
        print("{plus}{hyphens}{plus}".format(plus = '+', hyphens = '-'*79))
        total_amount = 0
        for index in range(len(self.__cart)):
            total_amount += self.__cart[index]['amount']
            print("| {0:^10} | {1:^10} | {2:^10} | {3:^10} | {4:^10} | {5:^12} |".format(index+1, self.__cart[index]['item'], self.__cart[index]['quantity'], self.__cart[index]['price'], '-', self.__cart[index]['amount']))
            print("{plus}{hyphens}{plus}".format(plus = '+', hyphens = '-'*79))
        print("| {0:>62} = {1:^12} |".format("Total Amount", total_amount))
        print("{plus}{hyphens}{plus}".format(plus = '+', hyphens = '-'*79))
        self.empty_cart()
    
    def empty_cart(self):
        '''
        Clears the cart
        '''
        self.__cart = []

    def get_todays_sale_amount(self):
        '''
        Simply prints total sale 
        '''
        print('\nTotal Sales during the day = Rs.%d\n' %self.sale_amount)

    def get_transaction_history(self):
        '''
        Retreives transaction history
        '''
        return self.__transactions.display_transaction_history()


class Transactions:
    '''
    '''
    __transaction_history = None

    def __init__(self):
        self.__transaction_history = []

    @property
    def transaction_history(self):
        return self.__transaction_history
    
    def update_transaction_history(self, transaction):
        self.__transaction_history.append(transaction)
    
    def do_transacton(self, customer, total_amount, date_time):
        transaction = {
            "customer": customer.get_customer_name(),
            "amount": total_amount,
            "datetime": date_time
        }
        self.__transaction_history.append(transaction)

    def display_transaction_history(self):
        '''
        Prints transaction history
        '''
        print("\n{0:^81}".format("TRANSACTIONS HISTORY:"))
        print("{plus}{hyphens}{plus}".format(plus = '+', hyphens = '-'*81))
        print("| {0:^10} | {1:^20} | {2:^20} | {3:^20} |".format("Sr. No.", "Customer Name", "Transaction Amount", "Transaction Time"))
        print("{plus}{hyphens}{plus}".format(plus = '+', hyphens = '-'*81))
        for index in range(len(self.__transaction_history)):
            print("| {0:^10} | {1:^20} | {2:^20} | {3:^20} |".format(index+1, self.__transaction_history[index]['customer'], self.__transaction_history[index]['amount'], self.__transaction_history[index]['datetime']))
            print("{plus}{hyphens}{plus}".format(plus = '+', hyphens = '-'*81))

class Customers:
    '''
    '''
    customer_name = ''
    __balance = 0

    def __init__(self, name):
        self.__balance = 1000
        self.customer_name = name

    @property
    def balance(self):
        return self.__balance

    def get_customer_name(self):
        return self.customer_name
    
    def validate_balance(self, balance):
        return self.__balance >= balance

    def selected_items_to_purchase(self, selected_items):
        print('\nCustomer has selected few items to purchase...')
        # items to purchase
        return selected_items

def items_in_grocery_store():
    items_list = [
        {
            "id": 101,
            "item": "Apples",
            "category": "Fruit",
            "quantity": 20,
            "price": 5,
            "sold": 0,
            "left": 20,
        },
        {
            "id": 102,
            "item": "Oranges",
            "category": "Fruit",
            "quantity": 30,
            "price": 6,
            "sold": 0,
            "left": 30,
        },
        {
            "id": 103,
            "item": "Mangoes",
            "category": "Fruit",
            "quantity": 20,
            "price": 7,
            "sold": 0,
            "left": 20,
        }
    ]
    return items_list

if __name__ == '__main__':
    # Create items_list
    items_list = items_in_grocery_store()

    # Create a Grocery Store
    grocery_store = GroceryStore(items_list)
     
    # Display items available in Grocery Store
    grocery_store.display_inventory()

    #########################################################
    
    # Create a customer
    yogesh = Customers('Yogesh')

    # Lets make customer go to grocery store &
    # purchase few items
    shopping_list = [
        ["Apples", 5],
        ["Oranges", 7]
    ]

    # lets add items to cart
    grocery_store.add_to_cart(yogesh.selected_items_to_purchase(shopping_list))

    # lets checkout
    grocery_store.checkout(yogesh)
    
    #########################################################

    # Create a customer
    milap = Customers('milap')

    # Lets make customer go to grocery store &
    # purchase few items
    shopping_list = [
        ["Mangoes", 10],
        ["Oranges", 9],
        ["Apples", 10]
    ]

    # lets add items to cart
    grocery_store.add_to_cart(milap.selected_items_to_purchase(shopping_list))

    # lets checkout
    grocery_store.checkout(milap)

    #########################################################

    # list the items in invertory
    grocery_store.display_inventory()

    # get today's sale
    grocery_store.get_todays_sale_amount()