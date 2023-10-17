
#========================Warehouses===========================#

class Warehouse():
    def __init__(self):
        self.stock = []
    
    def get_stock(self):
        return self.stock
    
    def search_stock(self, item_name):
        for stock in self.stock:
            if stock.name == item_name:
                return stock.quantity
        return 0
            
    def add_stock(self, item):
        for stock in self.stock:
            if stock.name == item.name:
                stock.quantity += item.quantity
                return
        self.stock.append(item)
        
    def remove_stock(self, item):
        for stock in self.stock:
            if stock.name == item.name:
                stock.quantity -= item.quantity
                if stock.quantity <= 0:     
                    self.stock.remove(stock)

#Perishables such as Meat and Fruit are stored in our refrigeration warehouse (North warehouse )
class NorthWarehouse(Warehouse):
    def __init__(self):
        self.warehouse_name = "North Warehouse"
        self.warehouse_description = "Perishables such as Meat and Fruit are stored in our refrigeration warehouse (North warehouse )"
        Warehouse.__init__(self)

# Things like canned drinks and bottled liquids are stored in 
# Large Vats and are bottled upon an order  (South warehouse )
class SouthWarehouse(Warehouse):
    def __init__(self):
        self.warehouse_name = "South Warehouse"
        self.warehouse_description = "Things like canned drinks and bottled liquids are stored in Large Vats and are bottled upon an order  (South warehouse )"
        Warehouse.__init__(self)

#Non Perishables are stored in our East Wearhouse
class EastWarehouse(Warehouse):
    def __init__(self):
        self.warehouse_name = "East Warehouse"
        self.warehouse_description = "Non Perishables are stored in our East Wearhouse"
        Warehouse.__init__(self)
    
#Frozen food is stored at our freezer warehouse (West Wearhouse) 
class WestWarehouse(Warehouse):
    def __init__(self):
        self.warehouse_name = "West Warehouse"
        self.warehouse_description = "Frozen food is stored at our freezer warehouse (West Wearhouse) "
        Warehouse.__init__(self)    

#============================Users=============================#


"""class User():
    def __init__(self, name, password):
        self.name = name
        self.password = password
        
    def search_stock(self, item_name, stock_controller):
        stock_amount = stock_controller.search_stock(item_name)
        print(stock_amount)
        return stock_amount
    
    def get_stock(self, stock_controller):
        stock = stock_controller.get_stock()
        for item in stock:
            print(item.name, item.quantity)
        return stock

class Employee(User):
    def __init__(self, name):
        User.__init__(self, name)
        
    def add_stock(self, item, stock_controller):
        stock_controller.add_stock(item)
    
    def remove_stock(self, item, stock_controller):
        stock_controller.remove_stock(item)"""
    

#=============================Stock Classes=====================#

class StockItem():
    def __init__(self, quantity, name):
        self.quantity = quantity
        self.name = name
    
class Perishables(StockItem):
    def __init__(self, quantity, name):
        StockItem.__init__(self, quantity, name)
    
class Liquid(StockItem):
    def __init__(self, quantity, name):
        StockItem.__init__(self, quantity, name)
    
class NonPerishables(StockItem):
    def __init__(self, quantity, name):
        StockItem.__init__(self, quantity, name)
            
class Frozen(StockItem):
    def __init__(self, quantity, name):
        StockItem.__init__(self, quantity, name)    

#==========================Stock Controller======================#    
    
class StockController():
    
    def __init__(self):
        self.north_warehouse = NorthWarehouse()
        self.south_warehouse = SouthWarehouse()
        self.east_warehouse = EastWarehouse()
        self.west_warehouse = WestWarehouse()
        self.warehouse_allocation_rules = [(Perishables, self.north_warehouse),
                                           (Liquid, self.south_warehouse),
                                           (NonPerishables, self.east_warehouse),
                                           (Frozen, self.west_warehouse)]
        
    def add_stock(self, item): 
        for rule in self.warehouse_allocation_rules:
            if type(item) == rule[0]:
                rule[1].add_stock(item)
        
    def get_stock(self):
        total_stock = []
        total_stock.append(self.north_warehouse.get_stock())
        total_stock.append(self.south_warehouse.get_stock())
        total_stock.append(self.east_warehouse.get_stock())
        total_stock.append(self.west_warehouse.get_stock())
        return sum(total_stock, [])
        
    def search_stock(self, item_name):
        quantity = 0
        quantity += self.north_warehouse.search_stock(item_name)
        quantity += self.south_warehouse.search_stock(item_name)
        quantity += self.east_warehouse.search_stock(item_name)
        quantity += self.west_warehouse.search_stock(item_name)
        return quantity
        
    def remove_stock(self, item):
        for rule in self.warehouse_allocation_rules:
            if type(item) == rule[0]:
                rule[1].remove_stock(item)
    

"""if __name__ == "__main__":
    stock_controller = StockController()
    while True:
        print("[1] Login as User")
        print("[2] Login as Employee")
        option = int(input("Enter Choice>"))
        if option == 1:
            name = input("Enter User Name>")
            user = User(name)
            while True:
                print("[1] Check the stock of a specific item")
                print("[2] Show the whole stock")
                print("[3] Logout of user account")
                option = int(input("Enter choice>"))
                if option == 1:
                    item = input("Item name to check >")
                    user.search_stock(item, stock_controller)
                elif option == 2:
                    user.get_stock(stock_controller)
                elif option == 3:
                    break
        elif option == 2:
            name = input("Enter Employee Name>")
            user = Employee(name)
            while True:
                print("[1] Check the stock of a specific item")
                print("[2] Show the whole stock")
                print("[3] Add item to stock")
                print("[4] Remove item from stock")
                print("[5] Logout of employee account")
                option = int(input("Enter choice>"))
                if option == 1:
                    item = input("Item name to check>")
                    user.search_stock(item, stock_controller)
                elif option == 2:
                    user.get_stock(stock_controller)
                elif option == 3:
                    name = input("Enter name of item to add>")
                    quantity = int(input("Quantity of item to add >"))
                    print("[1] Perishable [2] Liquid [3] Non-Perishable [4] Frozen")
                    item_type = int(input("Enter the type of item being added>"))
                    item_types = [Perishables, Liquid, NonPerishables, Frozen]
                    item = item_types[item_type-1](quantity, name)
                    user.add_stock(item, stock_controller)
                elif option == 4:
                    name = input("Enter name of item to remove>")
                    quantity = int(input("Quantity of item to remove >"))
                    print("[1] Perishable [2] Liquid [3] Non-Perishable [4] Frozen")
                    item_type = int(input("Enter the type of item being removed>"))
                    item_types = [Perishables, Liquid, NonPerishables, Frozen]
                    item = item_types[item_type-1](quantity, name)
                    user.remove_stock(item, stock_controller)
                elif option == 5:
                    break"""