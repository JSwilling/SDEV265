#Liquior system sales
#Author. Jose A Vazquez
#The goal of this project is create a inventory systen and a sales system all in one, while using database(sql) to hold  all the data.
from PIL import Image
from PIL import ImageTk
from PIL import Image as PILImage
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import ttkbootstrap as tb
import sqlite3
import re


class Windows(tb.Window):
    def __init__(self):
        super().__init__()
        self.Windows_login()
        self.tree_userlist=None
    #Window login
    def Windows_login(self):
        self.grid_columnconfigure(0, weight=1)

        self.frame_login = Frame(master=self)
        self.frame_login.grid(row=0, column=0, sticky=NSEW)
        image = PILImage.open('liquor_login.gif')
        photo = ImageTk.PhotoImage(image)
        label_image = Label(master=self.frame_login, image=photo)
        label_image.image = photo
        label_image.pack()
    

        Iblframe_login = tb.LabelFrame(master=self.frame_login, text="Welcome Back!")
        Iblframe_login.pack(padx=10, pady=35)

        Ibltitle = tb.Label(master=Iblframe_login, text="Log In")
        Ibltitle.pack(padx=10, pady=10)

        ent_user = tb.Entry(master=Iblframe_login, width=40, justify=CENTER)
        ent_user.pack(padx=10, pady=10)

        ent_password = tb.Entry(master=Iblframe_login, width=40, justify=CENTER)
        ent_password.pack(padx=10, pady=10)
        ent_password.config(show='*')

        btn_enter = tb.Button(master=Iblframe_login, width=38, text='Log in', bootstyle='success')
        btn_enter.pack(padx=10, pady=10)
        btn_enter.config(command=lambda: self.check_login(ent_user.get(), ent_password.get()))
    #Check if the user is in the database
    def check_login(self, username, password):
        conn = sqlite3.connect('user_login_liquor.db')
        cursor = conn.cursor()

        # Example query to check if username and password match
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            messagebox.showinfo("Liquor System", "Welcome back")
            self.startsession()
        else:
            #The login failed
            messagebox.showerror("Login Failed", "Invalid username or password")
    #The menu
    def window_menu(self):
        self.frame_left = Frame(self, width=200)
        self.frame_left.grid(row=0, column=0, sticky=NSEW)

        self.frame_center = Frame(self)
        self.frame_center.grid(row=0, column=1, sticky=NSEW)

        self.frame_right = Frame(self, width=400)
        self.frame_right.grid(row=0, column=2, sticky=NSEW)
        #Creating the buttom at the left side, like menu style.
        
        
        lqs_items = ttk.Button(self.frame_left, text="Sales", width=20, command=self.sales)
        lqs_items.grid(row=0, column=0,padx=10, pady=10)
        lqs_sales = ttk.Button(self.frame_left, text="Items", width=20, command=self.managing_items)
        lqs_sales.grid(row=1, column=0,padx=10, pady=10)
        lqs_manageusers = ttk.Button(self.frame_left, text="Manage Users", width=20, command=self.managing_users)
        lqs_manageusers.grid(row=2, column=0, padx=10, pady=10)
    

    

        lbl3 = ttk.Button(self.frame_right, text="Exit", command=self.close_window)
        lbl3.grid(row=0, column=0, padx=10, pady=10)


    def close_window(self):
        self.destroy()

    #Validation code for data entry.
    #For float data
    def check_float_value(self, action, check_float):
        return re.match(r'^\d*\.?\d*$',check_float) is not None and check_float.count('.') <= 1
    #For integer value
    def check_integers_value(self, action, value):
        return value.isdigit() or value == ""



    def managing_users(self):
        self.frame_magaging_users = Frame(self.frame_center)
        self.frame_magaging_users.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        self.frame_userslist = LabelFrame(self.frame_magaging_users)  # Use self.frame_magaging_users here
        self.frame_userslist.grid(row=0, column=0, sticky=NSEW)
    # Buttons for managing users
        lqs_newuser = ttk.Button(self.frame_userslist, text="Add User", width=20, command=self.new_user)
        lqs_newuser.grid(row=0, column=0, padx=10, pady=10)
        lqs_manageuser = ttk.Button(self.frame_userslist, text="Modify", width=20, command=self.modify_user)
        lqs_manageuser.grid(row=0, column=1, padx=10, pady=10)
        lqs_deleteuser = ttk.Button(self.frame_userslist, text="Delete", width=20, command=self.delete_user)
        lqs_deleteuser.grid(row=0, column=2, padx=10, pady=10)

    # Creating the view for managing users from our database
        self.lqsframe_tree_userlist = LabelFrame(self.frame_magaging_users)    
        self.lqsframe_tree_userlist.grid(row=2,column=0,sticky=NSEW)
    # Creating the columns as same as our database
        Info_columns=("ID", "Username", "Password", "Permissions")
        self.tree_userlist = ttk.Treeview(self.lqsframe_tree_userlist, columns=Info_columns, height=15, show='headings')
        self.tree_userlist.grid(row=0,column=0)
    # Creating the headings
        self.tree_userlist.heading("ID", text="ID", anchor=W)
        self.tree_userlist.heading("Username", text="Username", anchor=W)
        self.tree_userlist.heading("Password", text="Password", anchor=W)
        self.tree_userlist.heading("Permissions", text="Permissions", anchor=W)
        self.tree_userlist['displaycolumns'] = ('ID','Username','Permissions')
        # We do not put password because we need to keep that information hidden.
        self.users_database()

    def users_database(self):
        try:
            # Connecting our database with the program
            connect_database = sqlite3.connect('user_login_liquor.db')
            mouse = connect_database.cursor()
            # Check if self.tree_userlist is not None
            if self.tree_userlist is not None:
                # Delete children if self.tree_userlist is not None
                self.tree_userlist.delete(*self.tree_userlist.get_children())
            # See our database
            mouse.execute("SELECT * FROM Users")  # Use * to select all columns
            data = mouse.fetchall()
            # See every row
            for row in data:
                self.tree_userlist.insert("", 0, text=row[0], values=(row[0], row[1], row[2], row[3]))
            connect_database.commit()
            connect_database.close()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
    
    def new_user(self):
        self.frame_newuser = Toplevel(self)
        self.frame_newuser.title('New User')
        self.frame_newuser.geometry('400x400')
        self.frame_newuser.resizable(0,0)
        self.frame_newuser.grab_set()

        # Use a regular Frame for the main container
        main_frame = Frame(self.frame_newuser)
        main_frame.pack(fill=BOTH, expand=True)

        # Now we have to create the data that we want to introduce in the window
        # of the new user that we are creating here.
        # ID request
        lqs_id_newuser = Label(main_frame, text='ID')
        lqs_id_newuser.grid(row=0, column=0, padx=10, pady=10)
        lqs_entry_id_newuser = Entry(main_frame, width=20)
        lqs_entry_id_newuser.grid(row=0, column=1, padx=10, pady=10)
        #Adding validation
        check_integers_value_cmd = main_frame.register(self.check_integers_value)
        lqs_entry_id_newuser.config(validate='key', validatecommand=(check_integers_value_cmd,'%d','%P'))
        
        
        # username

        lqs_user_newuser = Label(main_frame, text='Username')
        lqs_user_newuser.grid(row=1, column=0, padx=10, pady=10)
        lqs_entry_user_newuser = Entry(main_frame, width=20)
        lqs_entry_user_newuser.grid(row=1, column=1, padx=10, pady=10)
        # password
        lqs_password_newuser = Label(main_frame, text='Password')
        lqs_password_newuser.grid(row=2, column=0, padx=10, pady=10)
        lqs_entry_password_newuser = Entry(main_frame, width=20)
        lqs_entry_password_newuser.grid(row=2, column=1, padx=10, pady=10)
        # permissions
        lqs_permissions_newuser = Label(main_frame, text='Permissions')
        lqs_permissions_newuser.grid(row=3, column=0, padx=10, pady=10)
        lqs_entry_permissions_newuser = ttk.Combobox(main_frame, values=('Admin', 'Sales', 'Inventory'), width=20)
        lqs_entry_permissions_newuser.grid(row=3, column=1, padx=10, pady=10)
        lqs_entry_permissions_newuser.current(0)

        #Creating the function to call our database
        
        def save_user():
        # Retrieve the user input
            user_id = lqs_entry_id_newuser.get()
            username = lqs_entry_user_newuser.get()
            password = lqs_entry_password_newuser.get()
            permissions = lqs_entry_permissions_newuser.get()

            # Connect to the database
            conn = sqlite3.connect('user_login_liquor.db')
            c = conn.cursor()

            # Insert the user into the database
            c.execute("INSERT INTO users (id, username, password, permissions) VALUES (?, ?, ?, ?)", (user_id, username, password, permissions))

            # Commit the transaction and close the connection
            conn.commit()
            conn.close()
            messagebox.showinfo("User Register","The User has been saved")
            self.frame_newuser.destroy()
            #Once that we save the user, we need to be able re-run the database to update it.
            self.users_database()

        lqs_save_newuser = ttk.Button(main_frame, text='Save', width=18, command=save_user)
        lqs_save_newuser.grid(row=4, column=1, padx=10, pady=10)

    def modify_user(self):
        selected_item = self.tree_userlist.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user to modify.")
            return

        # Get the selected user's ID
        user_id = self.tree_userlist.item(selected_item)['values'][0]

        # Fetch the user's information from the database
        conn = sqlite3.connect('user_login_liquor.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user_data = c.fetchone()
        conn.close()

        if user_data:
            # Open a new window to modify user details
            self.frame_modify_user = Toplevel(self)
            self.frame_modify_user.title('Modify User')
            self.frame_modify_user.geometry('400x400')
            self.frame_modify_user.resizable(0, 0)
            self.frame_modify_user.grab_set()

            # Create labels and entry widgets for user details
            Label(self.frame_modify_user, text="ID").grid(row=0, column=0, padx=10, pady=10)
            Label(self.frame_modify_user, text="Username").grid(row=1, column=0, padx=10, pady=10)
            Label(self.frame_modify_user, text="Password").grid(row=2, column=0, padx=10, pady=10)
            Label(self.frame_modify_user, text="Permissions").grid(row=3, column=0, padx=10, pady=10)

            entry_id = Entry(self.frame_modify_user, width=20)
            entry_id.grid(row=0, column=1, padx=10, pady=10)
            entry_id.insert(0, user_data[0])

            entry_username = Entry(self.frame_modify_user, width=20)
            entry_username.grid(row=1, column=1, padx=10, pady=10)
            entry_username.insert(0, user_data[1])

            entry_password = Entry(self.frame_modify_user, width=20)
            entry_password.grid(row=2, column=1, padx=10, pady=10)
            entry_password.insert(0, user_data[2])

            entry_permissions = ttk.Combobox(self.frame_modify_user, values=('Admin', 'Sales', 'Inventory'), width=20)
            entry_permissions.grid(row=3, column=1, padx=10, pady=10)
            entry_permissions.set(user_data[3])

            # Create a function to update user details in the database
            def save_changes():
                new_username = entry_username.get()
                new_password = entry_password.get()
                new_permissions = entry_permissions.get()

                conn = sqlite3.connect('user_login_liquor.db')
                c = conn.cursor()
                c.execute("UPDATE users SET username=?, password=?, permissions=? WHERE id=?", (new_username, new_password, new_permissions, user_id))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "User details updated successfully.")
                self.users_database()
                self.frame_modify_user.destroy()

            # Create a button to save changes
            Button(self.frame_modify_user, text="Save Changes", command=save_changes).grid(row=4, column=1, padx=10, pady=10)


    def delete_user(self):
        selected_item = self.tree_userlist.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user to delete.")
            return

        # Get the selected user's ID
        user_id = self.tree_userlist.item(selected_item)['values'][0]

        # Confirm deletion
        if messagebox.askyesno("Delete User", "Are you sure you want to delete this user?"):
            # Connect to the database and delete the user
            conn = sqlite3.connect('user_login_liquor.db')
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE id=?", (user_id,))
            conn.commit()
            conn.close()

            # Refresh the user list
            self.users_database()



    def managing_items(self):
        self.frame_magaging_items = Frame(self.frame_center)
        self.frame_magaging_items.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        self.frame_itemslist = LabelFrame(self.frame_magaging_items)  
        self.frame_itemslist.grid(row=0, column=0, sticky=NSEW)
        # Buttons for managing items
        lqs_newitem = ttk.Button(self.frame_itemslist, text="Add Item", width=20, command=self.new_item)
        lqs_newitem.grid(row=0, column=0, padx=10, pady=10)
        lqs_manageitems = ttk.Button(self.frame_itemslist, text="Modify Item", width=20, command=self.modify_item)
        lqs_manageitems.grid(row=0, column=1, padx=10, pady=10)
        lqs_deleteitem = ttk.Button(self.frame_itemslist, text="Delete Item", width=20, command=self.delete_item)
        lqs_deleteitem.grid(row=0, column=2, padx=10, pady=10)

        # Creating the view for managing items from our database
        self.lqsframe_tree_itemslist = LabelFrame(self.frame_magaging_items)    
        self.lqsframe_tree_itemslist.grid(row=1,column=0,sticky=NSEW)
        # Creating the columns as same as our database
        Info_columns=("ID", "Product", "Size", "Quantity", "Price")
        self.tree_useritems = ttk.Treeview(self.lqsframe_tree_itemslist, columns=Info_columns, height=15, show='headings')
        self.tree_useritems.grid(row=0,column=0)
        # Creating the headings
        self.tree_useritems.heading("ID", text="ID", anchor=W)
        self.tree_useritems.heading("Product", text="Product", anchor=W)
        self.tree_useritems.heading("Size", text="Size", anchor=W)
        self.tree_useritems.heading("Quantity", text="Quantity", anchor=W)
        self.tree_useritems.heading("Price", text="Price", anchor=W)
        self.tree_useritems['displaycolumns'] = ('ID','Product','Size', 'Quantity', 'Price')
        
        self.items_database()

    def items_database(self):
        try:
            # Connecting our database with the program
            connect_database = sqlite3.connect('user_login_liquor.db')
            mouse = connect_database.cursor()
            # Check if self.tree_userlist is not None
            if self.tree_useritems is not None:
                # Delete children if self.tree_userlist is not None
                self.tree_useritems.delete(*self.tree_useritems.get_children())
            # See our database
            mouse.execute("SELECT * FROM items")  # Use * to select all columns
            data = mouse.fetchall()
            # See every row
            for row in data:
                self.tree_useritems.insert("", 0, text=row[0], values=(row[0], row[1], row[2], row[3], row[4]))
            connect_database.commit()
            connect_database.close()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def new_item(self):
        self.frame_newitem = Toplevel(self)
        self.frame_newitem.title('New Item')
        self.frame_newitem.geometry('400x400')
        self.frame_newitem.resizable(0,0)
        self.frame_newitem.grab_set()

        # Use a regular Frame for the main container
        main_frame = Frame(self.frame_newitem)
        main_frame.pack(fill=BOTH, expand=True)

        # Now we have to create the data that we want to introduce in the window
        # of the new user that we are creating here.
        # ID request
        lqs_id_newitem = Label(main_frame, text='ID')
        lqs_id_newitem.grid(row=0, column=0, padx=10, pady=10)
        lqs_entry_id_newitem = Entry(main_frame, width=20)
        lqs_entry_id_newitem.grid(row=0, column=1, padx=10, pady=10)
        
        #VALIDATION


        check_integers_value_cmd = self.register(self.check_integers_value)
        lqs_entry_id_newitem.config(validate='key', validatecommand=(check_integers_value_cmd, '%d', '%P'))
        # product
        lqs_item_newitem = Label(main_frame, text='Product')
        lqs_item_newitem.grid(row=1, column=0, padx=10, pady=10)
        lqs_entry_item_newitem = Entry(main_frame, width=20)
        lqs_entry_item_newitem.grid(row=1, column=1, padx=10, pady=10)
        # size
        lqs_size_newitem = Label(main_frame, text='Size')
        lqs_size_newitem.grid(row=2, column=0, padx=10, pady=10)
        lqs_entry_size_newitem = Entry(main_frame, width=20)
        lqs_entry_size_newitem.grid(row=2, column=1, padx=10, pady=10)
        # quantity
        lqs_quantity_newitem = Label(main_frame, text='Quantity')
        lqs_quantity_newitem.grid(row=3, column=0, padx=10, pady=10)
        lqs_entry_quantity_newitem = Entry(main_frame,  width=20)
        lqs_entry_quantity_newitem.grid(row=3, column=1, padx=10, pady=10)
        #VALIDATION-VALIDATION-VALIDATION
        check_integers_value_cmd = main_frame.register(self.check_integers_value)
        lqs_entry_quantity_newitem.config(validate='key', validatecommand=(check_integers_value_cmd,'%d','%P'))
        #Price
        lqs_price_newitem = Label(main_frame, text='Price')
        lqs_price_newitem.grid(row=4, column=0, padx=10, pady=10)
        lqs_entry_price_newitem = Entry(main_frame, width=20)
        lqs_entry_price_newitem.grid(row=4, column=1, padx=10, pady=10)
        #VALIDATIONNNNNN
        validate_float_cmd = self.frame_newitem.register(self.check_float_value)
        lqs_entry_price_newitem.config(validate='key', validatecommand=(validate_float_cmd, '%d', '%P'))


        #Creating the function to call our database
        
        def save_item():
        # Retrieve the user input
            item_id = lqs_entry_id_newitem.get()
            product = lqs_entry_item_newitem.get()
            size = lqs_entry_size_newitem.get()
            quantity = lqs_entry_quantity_newitem.get()
            price = lqs_entry_price_newitem.get()

            # Connect to the database
            conn = sqlite3.connect('user_login_liquor.db')
            c = conn.cursor()

            # Insert the user into the database
            c.execute("INSERT INTO items (id, Product, Size, Quantity, Price) VALUES (?, ?, ?, ?,?)", (item_id,product,size,quantity,price,))

            # Commit the transaction and close the connection
            conn.commit()
            conn.close()
            messagebox.showinfo("New Item","The Item has been saved")
            self.frame_newitem.destroy()
            #Once that we save the user, we need to be able re-run the database to update it.
            self.items_database()

        lqs_save_newitem = ttk.Button(main_frame, text='Save', width=18, command=save_item)
        lqs_save_newitem.grid(row=5, column=1, padx=10, pady=10)
        # Refresh the user list
        self.items_database()
    def modify_item(self):
        selected_item = self.tree_useritems.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a item to modify.")
            return

        # Get the selected user's ID
        item_id = self.tree_useritems.item(selected_item)['values'][0]

        # Fetch the user's information from the database
        conn = sqlite3.connect('user_login_liquor.db')
        c = conn.cursor()
        c.execute("SELECT * FROM items WHERE id=?", (item_id,))
        item_data = c.fetchone()
        conn.close()

        if item_data:
            # Open a new window to modify user details
            self.frame_modify_item = Toplevel(self)
            self.frame_modify_item.title('Modify Item')
            self.frame_modify_item.geometry('400x400')
            self.frame_modify_item.resizable(0, 0)
            self.frame_modify_item.grab_set()

            # Create labels and entry widgets for user details
            Label(self.frame_modify_item, text="ID").grid(row=0, column=0, padx=10, pady=10)
            Label(self.frame_modify_item, text="Product").grid(row=1, column=0, padx=10, pady=10)
            Label(self.frame_modify_item, text="Size").grid(row=2, column=0, padx=10, pady=10)
            Label(self.frame_modify_item, text="Quantity").grid(row=3, column=0, padx=10, pady=10)
            Label(self.frame_modify_item, text="Price").grid(row=4, column=0, padx=10, pady=10)

            entry_id = Entry(self.frame_modify_item, width=20)
            entry_id.grid(row=0, column=1, padx=10, pady=10)
            entry_id.insert(0, item_data[0])

            entry_Product = Entry(self.frame_modify_item, width=20)
            entry_Product.grid(row=1, column=1, padx=10, pady=10)
            entry_Product.insert(0, item_data[1])

            entry_Size = Entry(self.frame_modify_item, width=20)
            entry_Size.grid(row=2, column=1, padx=10, pady=10)
            entry_Size.insert(0, item_data[2])
            
            entry_Quantity = Entry(self.frame_modify_item, width=20)
            entry_Quantity.grid(row=3, column=1, padx=10, pady=10)
            entry_Quantity.insert(0,item_data[3])

            entry_Price = Entry(self.frame_modify_item, width=20)
            entry_Price.grid(row=4, column=1, padx=10, pady=10)
            entry_Price.insert(0, item_data[4])

            

            # Create a function to update user details in the database
            def save_changes():
                new_id=entry_id.get()
                new_Product = entry_Product.get()
                new_Size = entry_Size.get()
                new_Quantity = entry_Quantity.get()
                new_Price = entry_Price.get()

                conn = sqlite3.connect('user_login_liquor.db')
                c = conn.cursor()
                c.execute("UPDATE items SET Product=?, Size=?, Quantity=?, Price=? WHERE id=?", (new_Product,new_Size,new_Quantity,new_Price,new_id))
                conn.commit()
                conn.close()

                messagebox.showinfo("Saved", "Items Updated")
                self.items_database()
                self.frame_modify_item.destroy()

            # Create a button to save changes
            Button(self.frame_modify_item, text="Save Changes", command=save_changes).grid(row=5, column=1, padx=10, pady=10)


    def delete_item(self):
        selected_item = self.tree_useritems.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a item to delet.")
            return

        # Get the selected user's ID
        item_id = self.tree_useritems.item(selected_item)['values'][0]

        # Confirm deletion
        if messagebox.askyesno("Delete item", "Do you want to delete the item?"):
            # Connect to the database and delete the user
            conn = sqlite3.connect('user_login_liquor.db')
            c = conn.cursor()
            c.execute("DELETE FROM items WHERE id=?", (item_id,))
            conn.commit()
            conn.close()

            # Refresh the user list
            self.items_database()


    #SALES
    def sales(self):
        
        #We declared the list
        #The list is temporary,it means that when we close the program is not going to save anything
        #we are saving all the items in the database.
        self.selected_items = []
        
        
        
        self.frame_sales = Frame(self.frame_center)
        self.frame_sales.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        lbl_item_id = Label(self.frame_sales, text="Item ID:")
        lbl_item_id.grid(row=0, column=0, padx=10, pady=10)

        entry_item_id = Entry(self.frame_sales, width=20)
        entry_item_id.grid(row=0, column=1, padx=10, pady=10)

        btn_search_item = Button(self.frame_sales, text="Search Item", command=lambda: self.search_item(entry_item_id.get()))
        btn_search_item.grid(row=0, column=2, padx=10, pady=10)

        self.lbl_item_details = Label(self.frame_sales, text="")
        self.lbl_item_details.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        
        #SPIN
        sp_quantity = Spinbox(self.frame_sales, from_=1, to =100, width= 8)
        sp_quantity.grid(row=2,column=2,padx=10,pady=10)
        self.lbl_quan_details = Label(self.frame_sales, text="Quantity")
        self.lbl_quan_details.grid(row=1, column=2, padx=10, pady=10)
        #Buttom to add to cart
        btn_add_to_cart = Button(self.frame_sales, text="Add to Cart", command=lambda: self.add_to_cart(entry_item_id.get(), int(sp_quantity.get())))
        btn_add_to_cart.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        
        

        self.cart_items = Listbox(self.frame_sales, width=50)
        self.cart_items.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        btn_checkout = Button(self.frame_sales, text="Checkout", command=self.checkout)
        btn_checkout.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        image = PILImage.open('bar.gif')
        photo = ImageTk.PhotoImage(image)
        label_image = Label(master=self.frame_sales, image=photo)
        label_image.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        label_image.image = photo
        

    def search_item(self, item_id):
        #we are going to look in our database if the item_id belong to anything that we have in the database
        conn = sqlite3.connect('user_login_liquor.db')
        c = conn.cursor()
        c.execute("SELECT * FROM items WHERE id=?", (item_id,))
        item = c.fetchone()
        conn.close()

        if item:
            self.lbl_item_details.config(text=f"ID: {item[0]}, Product: {item[1]}, Size: {item[2]}, Quantity: {item[3]}, Price: {item[4]}")
        else:
            self.lbl_item_details.config(text="Item not found")

    def add_to_cart(self, item_id, quantity):
        conn = sqlite3.connect('user_login_liquor.db')
        c = conn.cursor()
        #Once that we access to our database, we need to select the item based in the item_id
        #SQL databases works with id bettet
        c.execute("SELECT * FROM items WHERE id=?", (item_id,))
        item = c.fetchone()


        #The first thing that we need to check is if the item_id exist
        #If does not exist, we need to show a message error
        if item is None:
            messagebox.showerror("Error", "Item does not exist")
        
        #If the items exist, and there is stock, and also we can sell the quantity selecgted
        #We are going to add to our car
        elif item[3] >= quantity:
            self.selected_items.append((item ,quantity))
            self.cart_items.insert(END, f"{item[1]}  Price: {item[4]} Quantity: {quantity}")
            update_stock = item[3] - quantity
            #And of course we need to update the database with the items sales, and reduce the stock
            c.execute("UPDATE items SET Quantity=? WHERE id=?", (update_stock, item_id))
            conn.commit()
            conn.close()
        else:
            #If the items is not in stock we are going to show an error
            messagebox.showerror("Error ",f"The {item[1]} is out of stock")


    def checkout(self):
        
        total_items = sum(float(item[0][4]) * item[1] for item in self.selected_items)
        taxes = total_items * 0.07
        grand_total = total_items + taxes

        #We show the  grand total, incluide taxes
        messagebox.showinfo("Total", f"Total sale amount: {grand_total} Taxes: {taxes}")
        self.selected_items.clear()
        self.cart_items.delete(0, END)


    
    
    
    
    
    #Start session
    def startsession(self):
        self.frame_login.destroy()
        self.window_menu()
    
       



def main():
    app = Windows()
    app.title('Liquor system sales')
    app.state('zoomed')
    tb.Style('darkly')
    app.mainloop()


if __name__ == '__main__':
    main()

