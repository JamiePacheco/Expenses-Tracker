import json

#Defines the item class
class item:
    #When intialized the class will have name, cost, and quant attributes
    def __init__(self, name, cost, quant):
        #These references equal the intializes attributes
        self.name = name
        self.cost = cost
        self.quant = quant

#This is the cost class
class Costs:
    #When it is initalizes the instance will have the attributes month name and item list
    def __init__(self, month, items = []):
        #These references equal the intializes attributes
        self.month = month
        self.items = items

    #This is a class method that adds items to the items list attribute, takes in the parameter dict for items
    def add_items(self, dict):
        #Loops through the keys of dict
        for x in dict.keys():
            #Creates an instance of the item class with the arguments name, cost, and quanity
            self.items.append(item(x, dict[x][1], dict[x][0]))
            
        #Returns the items list
        return self.items

    #This is a class method that computes the total value of all item objects in the items list
    def total_amount(self):
        #Sets a variable names total to zero
        total = 0

        #loops through the list of item objects
        for x in self.items:

            #Adds the cost of the object multiplied by the quanitity of the object to the total
            total += x.cost * x.quant

        #Returns a rounded float value of the total
        return round(total, 2)

    #This is a class methods that removes an item from the instance's item list
    def remove_item(self, item):
        
        #Loops through the items list of the instance
        for x in self.items:

            #If the name is the name of the item it removes the item from the list
            if x.name == item:
                return self.items.remove(x)

        raise Exception("Item is not in list")

    #This is a class method that takes the data inside of the items method and turns it into a JSON file
    def turn_to_json(self):

        #Initializes the dictionary for the items
        item_dict = {}

        #Runs a loop through the items of the instance
        for item in self.items:
            #Adds the name, cost, and quanity of the items to the dict
            item_dict.update({item.name : (item.quant, item.cost)})

        #Using JSON library, it takes the dictionary and turns it into JSON object
        json_object = json.dumps(item_dict, indent=4)

        #Returns JSON object
        return json_object

    #This is a class method that allows the use to insert a JSON file into items list
    def insert_json_file(self, json_file):
        
        #Takes JSON file and turns it into dictionary
        JSON = json.load(json_file)

        #Uses the add items method to add all items from inside the dictionary
        return self.add_items(JSON)      

#Menu function definition (for debugging purposes)
def menu():
    
    #Initalizes the x variable
    x = " "

    #Takes in the input for the month variable
    month = input("What month is this record for?: ")
    
    #Creates an instance of the costs class with the user inputed month variable and an empty list for the items
    Overall_costs = Costs(month, [])

    #Provides the user with the proper formating for the input, plus the exit command
    print("Format the entries like: Item Price Quanity (Type 'Done' when finished)")

    #Intializes a dictionary for the item properties
    items_lists = {}

    #Begins a while loop
    while x:
        #Takes input and defines it to x
        x = input(": ")

        #If x is the exit command the loop breaks
        if x == "Done":
            break

        #The user input is split into a list for easy data access
        x = x.split(" ")

        #Inserts data from the x list into the item dictionary 
        items_lists.update({x[0]: (int(x[2]), float(x[1]))})

    #Overall costs instance runs the add items method of the costs class
    Overall_costs.add_items(items_lists)

    #Returns the overall costs object
    return Overall_costs