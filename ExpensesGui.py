from tkinter import *
from ExpensesClass import *
from tkinter import filedialog

root = Tk()
root.title("Expense Tracker")
root.geometry("550x545")
#root.resizable(FALSE, FALSE)
root.config(bg = "#555555")

OverallCosts = Costs("None", [])

global filestatusopen
filestatusopen = False

#Command for deleting all files 
def Delete_all_command():

    #Loops through the item name list boxes
    for x in Item_name_list.get(0, END):

        #Removes the item in the index
        OverallCosts.remove_item(x.replace(" - ", ""))

    #Deletes all of the names, prices, and quanity information.
    Item_name_list.delete(0,END)
    Item_price_list.delete(0,END)
    Item_quanity_list.delete(0,END)

    #Replaces the total amount spend information
    Total_Amount_Label.config(text = "Total Amount Spend: $0")

#Command for deleting file entries
def Delete_command():

    #Finds the index of the selected item
    index = Item_name_list.index(ANCHOR)

    #Removes the item of the selected index using the remove item method
    OverallCosts.remove_item(Item_name_list.get(index).replace(" - ", ""))

    #Deletes the selected item at the specific index
    Item_name_list.delete(index)
    Item_price_list.delete(index)
    Item_quanity_list.delete(index)

    #Configures the total amount label to the recalculated total amount.
    Total_Amount_Label.config(text = f"Total Amount Spend: ${OverallCosts.total_amount()}")

#Command for menu button to make a new file
def New_File_Command():

    global filestatusopen
    filestatusopen = False

    #Changes the title of the window
    root.title("Expense Tracker: New File")

    #Loops through all of the items and removes them as an object of the Overall Costs object
    for x in Item_name_list.get(0,END):
        OverallCosts.remove_item(x.replace(" - ", ""))

    #Deletes all of the strings from all of the listboxes
    Item_name_list.delete(0,END)
    Item_price_list.delete(0,END)
    Item_quanity_list.delete(0,END)

    #Configures the total to say $0
    Total_Amount_Label.config(text = "Total Amount Spend: $0")

#Command for opening files
def Open_File_Command():

    #Declares the json and filestatus open as global for later reference
    global json_file, filestatusopen

    #Trys the code blocks within indent
    try:
        #prompts the user to open a JSON file
        json_file = filedialog.askopenfilename(initialdir="C:\\Documents", title = "Open File", filetypes=(("JSON Files", "*.json"),))
        
        #Opens selected JSON file with read premissions
        JSON = open(json_file, "r")

        #Strips the file name of the directory and the .json extension
        file_name = json_file.replace('C:/Documents', '')
        file_name = file_name.replace(".json", "")

        #Inserts the file name inside of the window title
        root.title(f"Expense Tracker: {file_name}")

        #Removes all objects from with the list box and within Overallcosts.items
        for x in Item_name_list.get(0,END):
            OverallCosts.remove_item(x.replace(" - ", ""))

        #Uses the insert JSON method to insert the JSON dict
        OverallCosts.insert_json_file(JSON)

        #Closes the JSON file
        JSON.close()

        #Deletes all of the strings inside of the listboxes
        Item_name_list.delete(0,END)
        Item_price_list.delete(0,END)
        Item_quanity_list.delete(0,END)

        #Loops through the items of OverallCosts and inserts the properties within them
        for x in OverallCosts.items:
            Item_name_list.insert(END, f" - {x.name}")
            Item_price_list.insert(END, f" - ${str(x.cost)}")
            Item_quanity_list.insert(END, f" - {str(x.quant)}")

        #Sets the file open status to True (referenced when saving the file)
        filestatusopen = True

        #Configures the label to display correct total amount
        Total_Amount_Label.config(text = f"Total Amount Spend: {OverallCosts.total_amount()}")

    #If the user does not open the file an exception will be raised, to prevent that it will pass if any expeptions are found    
    except:
        pass

#Command for saving a file as
def Save_As_Command():

    #Declares these variables as global for later reference
    global json_file, filestatusopen
    
    #Prompts user to save file as 
    json_file = filedialog.asksaveasfilename(initialdir="C:\Documents", title = "Save As", filetypes=(("JSON Files", "*.json"),), defaultextension="*.")
    
    #Strips file name of the directory and the file extension
    file_name = json_file.replace('C:/Documents', '')
    file_name = file_name.replace(".json", "")

    #Inserts the file into the title
    root.title(f"Expense Tracker: {file_name}")

    #Opens the JSON file with the write premissions
    JSON = open(json_file, "w")

    #Within the JSON file it writes the overallcost items that use the turn to json method to convert to a propert dictonary from an objects list
    JSON.write(OverallCosts.turn_to_json())

    #Closes the json file
    JSON.close()

    filestatusopen = True

#Command for saving current file
def Save_Command():

    #Sets the variable as global so the save method can see the variable status
    global filestatusopen

    #if the file status is true then executes the code
    if filestatusopen:

        #Turns the items inside of OverallCosts object into a JSON file
        Json_File_data = OverallCosts.turn_to_json()

        #Open the JSON file with write permissions
        Json_file = open(json_file, "w")

        #Writes the data to the already opened file
        Json_file.write(Json_File_data)
    #If the filestatusopen variable is False then then this cose executes
    else:
        #Trys to execute the save as command
        try:
            Save_As_Command()
        #If exception is raised then code passes
        except:
            pass

#Command for inserting data inside of the Listboxes/Tables
def Enter_Command():

    #Tries the code in the block
    try:

        #Takes the user inputed entries and puts them into a dictonary with the proper data type
        Item = {User_itemname_input.get(): (int(User_itemamount_input.get()), float(User_itemprice_input.get()))}
        
        #Adds the item dict to the costs object using the add items method
        OverallCosts.add_items(Item)

        #Inserts the item into the listboxs
        Item_name_list.insert(END, f" - {str(OverallCosts.items[(len(OverallCosts.items)-1)].name)}")
        Item_price_list.insert(END, f" - ${str(OverallCosts.items[(len(OverallCosts.items)-1)].cost)}")
        Item_quanity_list.insert(END, f" - {str(OverallCosts.items[(len(OverallCosts.items)-1)].quant)}")

        #Deletes the entires inside of the entry widgets
        User_itemname_input.delete(0,END)
        User_itemamount_input.delete(0,END)
        User_itemprice_input.delete(0,END)

        #Recalculates and updates the total amount label
        Total_Amount_Label.config(text=f"Total Amount Spend: ${OverallCosts.total_amount()}")

    #If exception is raised the code is simply passed.
    except:
        pass

#Frame for the user input fields
Input_Frame = Frame(root, bg = "#555555")
Input_Frame.pack(padx=10, pady=5)

#Label and Entry widgets for item entry
User_itemname_label = Label(Input_Frame, text = "Item Name", font = (12), bg = "#555555")
User_itemname_label.grid(row = 1, column= 1)

User_itemprice_label = Label(Input_Frame, text = "Item Price", font = (12), bg = "#555555")
User_itemprice_label.grid(row = 2, column= 1)

User_itemamount_label = Label(Input_Frame, text = "Item Amount", font = (12), bg = "#555555")
User_itemamount_label.grid(row = 3, column= 1)

User_itemname_input = Entry(Input_Frame, font = (12))
User_itemname_input.grid(row = 1, column=2)

User_itemprice_input = Entry(Input_Frame, font = (12))
User_itemprice_input.grid(row = 2, column=2)

User_itemamount_input = Entry(Input_Frame, font = (12))
User_itemamount_input.grid(row = 3, column=2)

#Enter button for the input
Enter_button = Button(Input_Frame,text = "  Insert  \n Item  ", font = (12), command=Enter_Command)
Enter_button.grid(column=3, row = 1, rowspan=3, padx = 5, pady=5)

#Frame for the listbox and the labels
List_frame = Frame(root, bg= "#555555")
List_frame.pack(padx=5,pady=5)

#Lables of the list boxes
Item_name_label = Label(List_frame, text = "Item Name", font = (12), bg = "#555555")
Item_name_label.grid(column=1, row = 0, padx=5, pady=10)

Item_price_label = Label(List_frame, text = "Item Price", font = (12), bg = "#555555")
Item_price_label.grid(column=2, row = 0, padx=5, pady=10)

Item_quanity_label = Label(List_frame, text = "Item Amount", font = (12), bg = "#555555")
Item_quanity_label.grid(column=3, row = 0, padx=5, pady=10)

#List box that holds items characteristics in them
Item_name_list = Listbox(List_frame, width=20, height=20, font = (12))
Item_name_list.grid(column=1,row=1, padx=5)

Item_price_list = Listbox(List_frame, width=20, height=20, font = (12))
Item_price_list.grid(column=2,row=1, padx=5)

Item_quanity_list = Listbox(List_frame, width=20, height=20, font = (12))
Item_quanity_list.grid(column=3,row=1, padx=5)

#Total Amount Spent Label
Total_Amount_Label = Label(root, text = f"Total Amount Spend: ${OverallCosts.total_amount()}", font = (20))
Total_Amount_Label.pack()

#Creating the top menu for saving files
Top_menu = Menu(root)
root.config(menu= Top_menu)

#Creates the file submenu
File_Handling_Menu = Menu(Top_menu, tearoff=FALSE)
Top_menu.add_cascade(label = "File", menu = File_Handling_Menu)

#Adds the different commands for the file submenu
File_Handling_Menu.add_command(label = "New File", command = New_File_Command)
File_Handling_Menu.add_command(label = "Open File", command = Open_File_Command)
File_Handling_Menu.add_command(label = "Save", command = Save_Command)
File_Handling_Menu.add_command(label = "Save As", command = Save_As_Command)

#Creates the delete submenu
Delete_Handling = Menu(Top_menu, tearoff=FALSE)
Top_menu.add_cascade(label = "Delete", menu = Delete_Handling)

#adds the commands for the delete submenu
Delete_Handling.add_command(label = "Delete Entry", command = Delete_command)
Delete_Handling.add_command(label = "Delete All Entries", command = Delete_all_command)

#The GUI main loop
root.mainloop()