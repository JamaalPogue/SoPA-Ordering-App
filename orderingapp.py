import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk, messagebox
import hashlib
import mysql.connector
from mysql.connector import Error


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.current_user_id = None  # Initialize current_user_id
        
        # Start the app in fullscreen mode
        self.attributes('-fullscreen', True)

        # Option to exit fullscreen with Escape
        self.bind("<Escape>", self.end_fullscreen)

        # Load the logo
        self.logo_image = PhotoImage(file="logo.png")

        # Define colors based on the logo and exit button
        self.colors = {
            'bg': '#FFFFFF',
            'button_bg': '#005a34',
            'button_fg': '#FFFFFF',
            'button_active_bg': '#004225',
            'exit_button_bg': '#007848',  # Green color for exit button
        }

        # Initializing frames
        self.frames = {}
        for F in (LoginFrame, DashboardFrame, ProductOrderFrame, UserSettingsFrame, UpdateUserInfoFrame, WaterBottleFrame, YogaMatFrame, CartFrame):
            frame = F(self, self.colors, self.logo_image)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginFrame)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

    def end_fullscreen(self, event=None):
        self.attributes("-fullscreen", False)

class BaseFrame(tk.Frame):
    def __init__(self, master, colors, logo):
        super().__init__(master, bg=colors['bg'])
        self.grid(sticky="nsew")
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        self.logo_image = logo
        self.colors = colors
        self.create_widgets()

    def create_widgets(self):
        # Widgets specific to each frame are added in their respective classes
        pass

class LoginFrame(BaseFrame):
    def create_widgets(self):
        center_frame = tk.Frame(self, bg=self.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, image=self.logo_image, bg=self.colors['bg']).grid(row=0, columnspan=2, pady=10)
        tk.Label(center_frame, text="UserID", bg=self.colors['bg'], font=("Helvetica", 14)).grid(row=1, column=0, pady=10, sticky="e")
        self.user_id_entry = tk.Entry(center_frame, font=("Helvetica", 14))
        self.user_id_entry.grid(row=1, column=1, pady=10, sticky="ew")
        tk.Label(center_frame, text="Password", bg=self.colors['bg'], font=("Helvetica", 14)).grid(row=2, column=0, pady=10, sticky="e")
        self.password_entry = tk.Entry(center_frame, show="*", font=("Helvetica", 14))
        self.password_entry.grid(row=2, column=1, pady=10, sticky="ew")

        login_button = tk.Button(center_frame, text="Login", bg=self.colors['button_bg'], fg=self.colors['button_fg'],
                                 font=("Helvetica", 14), activebackground=self.colors['button_active_bg'],
                                 command=self.login)
        login_button.grid(row=3, columnspan=2, pady=20)

        exit_button = tk.Button(self, text="Exit Application", bg=self.colors['exit_button_bg'], fg="white",
                                command=self.master.destroy, font=("Arial", 12))
        exit_button.place(relx=1.0, rely=0.0, anchor="ne", width=120, height=50)

    def login(self):
        user_email = self.user_id_entry.get()  # Assuming this entry is used for email
        password = self.password_entry.get()

        if not user_email or not password:
            messagebox.showerror("Login Failed", "Email or password cannot be blank.")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="SoPAStudentDB!#!",
                database="aafesorder"
            )
            cursor = connection.cursor(buffered=True)

            # Hash the password entered by the user
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Adjusted query to join Users and Authentication tables
            query = """
            SELECT Users.UserID 
            FROM Users 
            JOIN Authentication 
            ON Users.UserID = Authentication.UserID 
            WHERE Users.UserEmail = %s AND Authentication.HashedPassword = %s
            """
            cursor.execute(query, (user_email, hashed_password))
            result = cursor.fetchone()

            if result:
                self.master.current_user_id = result[0]  # Storing the current user's ID
                self.master.show_frame(DashboardFrame)
            else:
                messagebox.showerror("Login Failed", "Invalid email or password.")
        except Error as error:
            messagebox.showerror("Database Error", str(error))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


class DashboardFrame(BaseFrame):
    def create_widgets(self):
        center_frame = tk.Frame(self, bg=self.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, image=self.logo_image, bg=self.colors['bg']).grid(row=0, columnspan=2, pady=10)
        tk.Label(center_frame, text="Dashboard", bg=self.colors['bg'], font=("Helvetica", 16)).grid(row=1, columnspan=2, pady=10)
        product_order_button = tk.Button(center_frame, text="Create Order", bg=self.colors['button_bg'], fg=self.colors['button_fg'],
                                         font=("Helvetica", 14), activebackground=self.colors['button_active_bg'],
                                         command=lambda: self.master.show_frame(ProductOrderFrame))
        product_order_button.grid(row=2, column=0, padx=10, pady=20)
        user_settings_button = tk.Button(center_frame, text="User Settings", bg=self.colors['button_bg'], fg=self.colors['button_fg'],
                                         font=("Helvetica", 14), activebackground=self.colors['button_active_bg'],
                                         command=lambda: self.master.show_frame(UserSettingsFrame))
        user_settings_button.grid(row=2, column=1, padx=10, pady=20)
        logout_button = tk.Button(center_frame, text="Log Out", bg=self.colors['button_bg'], fg=self.colors['button_fg'],
                                  font=("Helvetica", 14), activebackground=self.colors['button_active_bg'],
                                  command=lambda: self.master.show_frame(LoginFrame))
        logout_button.grid(row=3, columnspan=2, pady=10)
        exit_button = tk.Button(self, text="Exit Application", bg=self.colors['exit_button_bg'], fg="white",
                                command=self.master.destroy, font=("Arial", 12))
        exit_button.place(relx=1.0, rely=0.0, anchor="ne", width=120, height=50)

class ProductOrderFrame(BaseFrame):
    def create_widgets(self):
        center_frame = tk.Frame(self, bg=self.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, image=self.logo_image, bg=self.colors['bg']).grid(row=0, columnspan=2, pady=10)
        tk.Label(center_frame, text="Products", bg=self.colors['bg'], font=("Helvetica", 16)).grid(row=1, columnspan=2, pady=10)

        # Create buttons for each product type
        water_bottle_button = tk.Button(center_frame, text="Water Bottles", bg=self.colors['button_bg'], fg=self.colors['button_fg'], font=("Helvetica", 14), activebackground=self.colors['button_active_bg'], command=self.show_water_bottle_frame)
        water_bottle_button.grid(row=2, column=0, padx=20, pady=10)

        yoga_mat_button = tk.Button(center_frame, text="Yoga Mats", bg=self.colors['button_bg'], fg=self.colors['button_fg'], font=("Helvetica", 14), activebackground=self.colors['button_active_bg'], command=self.show_yoga_mat_frame)
        yoga_mat_button.grid(row=2, column=1, padx=20, pady=10)

        checkout_button = tk.Button(center_frame, text="Check Out", bg=self.colors['button_bg'], fg=self.colors['button_fg'], font=("Helvetica", 14), activebackground=self.colors['button_active_bg'], command=self.show_cart_frame)
        checkout_button.grid(row=3, columnspan=2, pady=10)

        back_button = tk.Button(center_frame, text="Return to Dashboard", bg=self.colors['button_bg'], fg=self.colors['button_fg'], font=("Helvetica", 14), activebackground=self.colors['button_active_bg'], command=lambda: self.master.show_frame(DashboardFrame))
        back_button.grid(row=4, columnspan=2, pady=10)

        exit_button = tk.Button(self, text="Exit Application", bg=self.colors['exit_button_bg'], fg="white", command=self.master.destroy, font=("Arial", 12))
        exit_button.place(relx=1.0, rely=0.0, anchor="ne", width=120, height=50)

    def show_water_bottle_frame(self):
        self.master.show_frame(WaterBottleFrame)

    def show_yoga_mat_frame(self):
        self.master.show_frame(YogaMatFrame)

    def show_cart_frame(self):
        self.master.show_frame(CartFrame)

class WaterBottleFrame(BaseFrame):
    def create_widgets(self):
        back_button = tk.Button(self, text="Back to Product Order", bg=self.colors['button_bg'], fg=self.colors['button_fg'], font=("Helvetica", 14), activebackground=self.colors['button_active_bg'], command=self.back_to_product_order)
        back_button.grid(row=0, columnspan=2, pady=10)

        exit_button = tk.Button(self, text="Exit Application", bg=self.colors['exit_button_bg'], fg="white", command=self.master.destroy, font=("Arial", 12))
        exit_button.place(relx=1.0, rely=0.0, anchor="ne", width=120, height=50)

    def back_to_product_order(self):
        self.master.show_frame(ProductOrderFrame)

class YogaMatFrame(BaseFrame):
    def create_widgets(self):
        back_button = tk.Button(self, text="Back to Product Order", bg=self.colors['button_bg'], fg=self.colors['button_fg'], font=("Helvetica", 14), activebackground=self.colors['button_active_bg'], command=self.back_to_product_order)
        back_button.grid(row=0, columnspan=2, pady=10)

        exit_button = tk.Button(self, text="Exit Application", bg=self.colors['exit_button_bg'], fg="white", command=self.master.destroy, font=("Arial", 12))
        exit_button.place(relx=1.0, rely=0.0, anchor="ne", width=120, height=50)

    def back_to_product_order(self):
        self.master.show_frame(ProductOrderFrame)

class CartFrame(BaseFrame):
    def create_widgets(self):
        add_more_button = tk.Button(self, text="Add More to Order", bg=self.colors['button_bg'], fg=self.colors['button_fg'], font=("Helvetica", 14), activebackground=self.colors['button_active_bg'], command=self.add_more_to_order)
        add_more_button.grid(row=0, column=0, padx=20, pady=10)

        submit_order_button = tk.Button(self, text="Submit Order", bg=self.colors['button_bg'], fg=self.colors['button_fg'], font=("Helvetica", 14), activebackground=self.colors['button_active_bg'], command=self.submit_order)
        submit_order_button.grid(row=0, column=1, padx=20, pady=10)

        exit_button = tk.Button(self, text="Exit Application", bg=self.colors['exit_button_bg'], fg="white", command=self.master.destroy, font=("Arial", 12))
        exit_button.place(relx=1.0, rely=0.0, anchor="ne", width=120, height=50)

    def add_more_to_order(self):
        self.master.show_frame(ProductOrderFrame)

    def submit_order(self):
        # Implement order submission logic
        pass


    def create_widgets(self):
        center_frame = tk.Frame(self, bg=self.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="Update User Information", bg=self.colors['bg'], font=("Helvetica", 16)).grid(row=0, columnspan=2, pady=10)

        # Display current user information
        tk.Label(center_frame, text="First Name:", bg=self.colors['bg']).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.first_name_var = tk.StringVar()
        self.first_name_entry = tk.Entry(center_frame, textvariable=self.first_name_var)
        self.first_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(center_frame, text="Last Name:", bg=self.colors['bg']).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.last_name_var = tk.StringVar()
        self.last_name_entry = tk.Entry(center_frame, textvariable=self.last_name_var)
        self.last_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(center_frame, text="User Role:", bg=self.colors['bg']).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.user_role_var = tk.StringVar()
        self.user_role_entry = tk.Entry(center_frame, textvariable=self.user_role_var, state="readonly")  # Disable user role entry
        self.user_role_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(center_frame, text="User Email:", bg=self.colors['bg']).grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.user_email_var = tk.StringVar()
        self.user_email_entry = tk.Entry(center_frame, textvariable=self.user_email_var)
        self.user_email_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        tk.Label(center_frame, text="Preferred Payment Method:", bg=self.colors['bg']).grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.preferred_payment_var = tk.StringVar()
        self.preferred_payment_entry = tk.Entry(center_frame, textvariable=self.preferred_payment_var)
        self.preferred_payment_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Update User Information Button
        update_user_info_button = tk.Button(center_frame, text="Update Information", command=self.update_user_info,
                                            bg=self.colors['button_bg'], fg=self.colors['button_fg'],
                                            font=("Helvetica", 14))
        update_user_info_button.grid(row=6, columnspan=2, pady=20)

        # Button to navigate back
        back_button = tk.Button(center_frame, text="Return to User Settings", bg=self.colors['button_bg'], fg=self.colors['button_fg'],
                                font=("Helvetica", 14), activebackground=self.colors['button_active_bg'],
                                command=lambda: self.master.show_frame(UserSettingsFrame))
        back_button.grid(row=7, columnspan=2, pady=10)

    def update_user_info(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="SoPAStudentDB!#!",
                database="aafesorder"
            )
            cursor = connection.cursor()

            # Get updated user information from entry widgets
            updated_first_name = self.first_name_var.get()
            updated_last_name = self.last_name_var.get()
            updated_user_email = self.user_email_var.get()
            updated_preferred_payment = self.preferred_payment_var.get()

            # Update user information in the database
            query = "UPDATE Users SET FirstName = %s, LastName = %s, UserEmail = %s, PreferredPaymentMethod = %s WHERE UserID = %s"
            cursor.execute(query, (updated_first_name, updated_last_name, updated_user_email, updated_preferred_payment, self.master.current_user_id))
            connection.commit()
            print("User information updated successfully!")
        except Error as e:
            print("Error updating user information:", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

                # Clear entry widgets after updating user information
                self.clear_entry_widgets()

    def clear_entry_widgets(self):
        self.first_name_entry.delete(0, 'end')
        self.last_name_entry.delete(0, 'end')
        self.user_email_entry.delete(0, 'end')
        self.preferred_payment_entry.delete(0, 'end')

class UserSettingsFrame(BaseFrame):
    def create_widgets(self):
        center_frame = tk.Frame(self, bg=self.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, image=self.logo_image, bg=self.colors['bg']).grid(row=0, pady=10)
        tk.Label(center_frame, text="User Settings Page", bg=self.colors['bg'], font=("Helvetica", 16)).grid(row=1, pady=10)

        # Display current user information
        tk.Label(center_frame, text="First Name:", bg=self.colors['bg']).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.first_name_var = tk.StringVar()
        tk.Entry(center_frame, textvariable=self.first_name_var, state="readonly").grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(center_frame, text="Last Name:", bg=self.colors['bg']).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.last_name_var = tk.StringVar()
        tk.Entry(center_frame, textvariable=self.last_name_var, state="readonly").grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(center_frame, text="User Role:", bg=self.colors['bg']).grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.user_role_var = tk.StringVar()
        tk.Entry(center_frame, textvariable=self.user_role_var, state="readonly").grid(row=4, column=1, padx=5, pady=5, sticky="w")

        tk.Label(center_frame, text="User Email:", bg=self.colors['bg']).grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.user_email_var = tk.StringVar()
        tk.Entry(center_frame, textvariable=self.user_email_var, state="readonly").grid(row=5, column=1, padx=5, pady=5, sticky="w")

        tk.Label(center_frame, text="Preferred Payment Method:", bg=self.colors['bg']).grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.preferred_payment_var = tk.StringVar()
        tk.Entry(center_frame, textvariable=self.preferred_payment_var, state="readonly").grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Update Settings Button
        update_settings_button = tk.Button(center_frame, text="Update User Information", command=lambda: self.master.show_frame(UpdateUserInfoFrame), bg=self.colors['button_bg'], fg=self.colors['button_fg'], font=("Helvetica", 14))
        update_settings_button.grid(row=7, columnspan=2, pady=20)

        # Buttons to navigate back and exit
        back_button = tk.Button(center_frame, text="Return to Dashboard", bg=self.colors['button_bg'], fg=self.colors['button_fg'],
                                font=("Helvetica", 14), activebackground=self.colors['button_active_bg'],
                                command=lambda: self.master.show_frame(DashboardFrame))
        back_button.grid(row=8, columnspan=2, pady=10)

        exit_button = tk.Button(self, text="Exit Application", bg=self.colors['exit_button_bg'], fg="white",
                                command=self.master.destroy, font=("Arial", 12))
        exit_button.place(relx=1.0, rely=0.0, anchor="ne", width=120, height=50)

        # Fetch and display user information from database
        self.fetch_and_display_user_info()

    def fetch_and_display_user_info(self):
        # Fetch user information from MySQL database
        # Here, you will connect to your MySQL database and fetch user information
        # For demonstration purposes, I'll assume you have retrieved user information from the database
        user_info = {
            "first_name": "John",
            "last_name": "Doe",
            "user_role": "Admin",
            "user_email": "john.doe@example.com",
            "preferred_payment_method": "Credit Card"
        }

        # Update entry widgets with fetched user information
        self.first_name_var.set(user_info["first_name"])
        self.last_name_var.set(user_info["last_name"])
        self.user_role_var.set(user_info["user_role"])
        self.user_email_var.set(user_info["user_email"])
        self.preferred_payment_var.set(user_info["preferred_payment_method"])

class UpdateUserInfoFrame(BaseFrame):
    def create_widgets(self):
        center_frame = tk.Frame(self, bg=self.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="Update User Information", bg=self.colors['bg'], font=("Helvetica", 16)).grid(row=0, columnspan=2, pady=10)

        # Display current user information
        tk.Label(center_frame, text="First Name:", bg=self.colors['bg']).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.first_name_var = tk.StringVar()
        self.first_name_entry = tk.Entry(center_frame, textvariable=self.first_name_var)
        self.first_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(center_frame, text="Last Name:", bg=self.colors['bg']).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.last_name_var = tk.StringVar()
        self.last_name_entry = tk.Entry(center_frame, textvariable=self.last_name_var)
        self.last_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(center_frame, text="User Role:", bg=self.colors['bg']).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.user_role_var = tk.StringVar()
        self.user_role_entry = tk.Entry(center_frame, textvariable=self.user_role_var, state="readonly")  # Disable user role entry
        self.user_role_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(center_frame, text="User Email:", bg=self.colors['bg']).grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.user_email_var = tk.StringVar()
        self.user_email_entry = tk.Entry(center_frame, textvariable=self.user_email_var)
        self.user_email_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        tk.Label(center_frame, text="Preferred Payment Method:", bg=self.colors['bg']).grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.preferred_payment_var = tk.StringVar()
        self.preferred_payment_entry = tk.Entry(center_frame, textvariable=self.preferred_payment_var)
        self.preferred_payment_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Fetch and display user information from database
        self.fetch_and_display_user_info()

        # Add update button
        update_button = tk.Button(center_frame, text="Update", command=self.update_user_info, bg=self.colors['button_bg'], fg=self.colors['button_fg'], font=("Helvetica", 14))
        update_button.grid(row=6, columnspan=2, pady=20)

        # Add back button
        back_button = tk.Button(center_frame, text="Back to User Settings", command=lambda: self.master.show_frame(UserSettingsFrame), bg=self.colors['button_bg'], fg=self.colors['button_fg'], font=("Helvetica", 14))
        back_button.grid(row=7, columnspan=2, pady=10)
        
        exit_button = tk.Button(self, text="Exit Application", bg=self.colors['exit_button_bg'], fg="white",
                                command=self.master.destroy, font=("Arial", 12))
        exit_button.place(relx=1.0, rely=0.0, anchor="ne", width=120, height=50)

    def fetch_and_display_user_info(self):
        # Fetch user information from MySQL database
        # Here, you will connect to your MySQL database and fetch user information
        # For demonstration purposes, I'll assume you have retrieved user information from the database
        user_info = {
            "first_name": "John",
            "last_name": "Doe",
            "user_role": "Admin",
            "user_email": "john.doe@example.com",
            "preferred_payment_method": "Credit Card"
        }

        # Update entry widgets with fetched user information
        self.first_name_var.set(user_info["first_name"])
        self.last_name_var.set(user_info["last_name"])
        self.user_role_var.set(user_info["user_role"])
        self.user_email_var.set(user_info["user_email"])
        self.preferred_payment_var.set(user_info["preferred_payment_method"])

    def update_user_info(self):
        # Retrieve updated user information from entry widgets
        updated_user_info = {
            "first_name": self.first_name_var.get(),
            "last_name": self.last_name_var.get(),
            "user_role": self.user_role_var.get(),
            "user_email": self.user_email_var.get(),
            "preferred_payment_method": self.preferred_payment_var.get()
        }


def connectToDatabase(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful.")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# This is the block of table creation statements
def createUserRoleTable(connection, cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS UserRole (UserRoleID int NOT NULL,RoleDescription varchar(50) UNIQUE,PRIMARY KEY (UserRoleID))")
    connection.commit()
    print("UserRole table created.")

def createUsersTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  Users (UserID int NOT NULL, FirstName varchar(100) NOT NULL, LastName varchar(100) NOT NULL, UserRoleID int, UserEmail varchar(100), PreferredPaymentMethod varchar(100), isDeleted BOOLEAN DEFAULT FALSE, PRIMARY KEY (UserID))")
    connection.commit()
    print("Users table created.")

def createDistributionCenterTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  DistributionCenter (SiteID int NOT NULL, DODAddressCode varchar(10), FacilityNo int NOT NULL, FacilityNoLong int, SiteName varchar(255), SitePhone varchar(100), ShippingAddress varchar(255), ShippingAddress2 varchar(255), ShippingAddress3 varchar(255), ShippingAddress4 varchar(255), ShippingCity varchar(255), ShippingState varchar(100), ShippingZip varchar(100), PRIMARY KEY (SiteID))")
    connection.commit()
    print("DistributionCenter table created.")

def createOrdersTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Orders (OrderID int NOT NULL, UserID int, SiteID int, OrderDetails varchar(255), TotalCost decimal(10,2), OrderStatus varchar(255) CHECK (OrderStatus IN ('Pending', 'Completed', 'Canceled')), PRIMARY KEY (OrderID))")
    connection.commit()
    print("Orders table created.")

def createAuthenticationTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  Authentication (AuthenticationID int NOT NULL, UserID int, HashedPassword varchar(100), LastPasswordChangeDate date, PasswordChangeRequired boolean DEFAULT FALSE, PRIMARY KEY (AuthenticationID))")
    connection.commit()
    print("Authentication table created.")

def createOrderDetailTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  OrderDetail (OrderDetailID int NOT NULL, OrderID int, ProductID int, Quantity int, Customized boolean, CustomizationID int, PRIMARY KEY (OrderDetailID))")
    connection.commit()
    print("OrderDetail table created.")

def createCustomizationTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  Customization (CustomizationID int NOT NULL, ItemDescription varchar(255), PRIMARY KEY (CustomizationID))")
    connection.commit()
    print("Customization table created.")

def createProductsTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  Products (ProductID int NOT NULL, ProductName varchar(255) NOT NULL UNIQUE, ProductColor varchar(100), ItemDescription varchar(255), Price decimal(5,2)  CHECK (Price >= 0), PRIMARY KEY (ProductID))")
    connection.commit()
    print("Products table created.")

def createInventoryTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  Inventory (InventoryID int NOT NULL, ProductID int, CurrentStockLevel int NOT NULL CHECK (CurrentStockLevel >= 0), PRIMARY KEY (InventoryID))")
    connection.commit()
    print("Inventory table created.")

def createAuditLogTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  AuditLog (LogID int NOT NULL, UserID int, ActivityType varchar(255), ActivityTimestamp date, AffectedRecordID int, ItemDescription varchar(255), PRIMARY KEY (LogID))")
    connection.commit()
    print("AuditLog table created.")

def createWarehouseNotificationTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  WarehouseNotification (NotificationID int NOT NULL, OrderID int, SiteID int, NotificationTimestamp datetime, PRIMARY KEY (NotificationID))")
    connection.commit()
    print("WarehouseNotification table created.")

def createPaymentNotificationTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  PaymentNotification (PaymentID int NOT NULL, OrderID int, Timestamp datetime, PRIMARY KEY (PaymentID))")
    connection.commit()
    print("PaymentNotification table created.")

def runAlterStatements(connection, cursor):
    cursor.execute("ALTER TABLE Users ADD FOREIGN KEY (UserRoleID) REFERENCES UserRole (UserRoleID);")
    cursor.execute("ALTER TABLE Authentication ADD FOREIGN KEY (UserID) REFERENCES Users (UserID);")
    cursor.execute("ALTER TABLE Orders ADD FOREIGN KEY (UserID) REFERENCES Users (UserID);")
    cursor.execute("ALTER TABLE Orders ADD FOREIGN KEY (SiteID) REFERENCES DistributionCenter (SiteID);")
    cursor.execute("ALTER TABLE OrderDetail ADD FOREIGN KEY (OrderID) REFERENCES Orders (OrderID);")
    cursor.execute("ALTER TABLE OrderDetail ADD FOREIGN KEY (ProductID) REFERENCES Products (ProductID);")
    cursor.execute("ALTER TABLE OrderDetail ADD FOREIGN KEY (CustomizationID) REFERENCES Customization (CustomizationID);")
    cursor.execute("ALTER TABLE Inventory ADD FOREIGN KEY (ProductID) REFERENCES Products (ProductID);")
    cursor.execute("ALTER TABLE AuditLog ADD FOREIGN KEY (UserID) REFERENCES Users (UserID);")
    cursor.execute("ALTER TABLE WarehouseNotification ADD FOREIGN KEY (OrderID) REFERENCES Orders (OrderID);")
    cursor.execute("ALTER TABLE WarehouseNotification ADD FOREIGN KEY (SiteID) REFERENCES DistributionCenter (SiteID);")
    cursor.execute("ALTER TABLE PaymentNotification ADD FOREIGN KEY (OrderID) REFERENCES Orders (OrderID);")
    connection.commit()
    print("Alter statements successful.")

# Initial Procedure creation
def createProcedureSoftDeleteUser(connection,cursor):
    softDeleteUser = """
    CREATE PROCEDURE IF NOT EXISTS softDeleteUser (IN deletedUserID INT)
    BEGIN
        UPDATE Users
        SET isDeleted = TRUE
        WHERE userID = deletedUserID;
    END
    """
    cursor.execute(softDeleteUser)
    connection.commit()
    print("softDeleteUser procedure created.")

def createProcedurePasswordChangeVerification(connection,cursor):
    passwordChangeVerification = """
    CREATE PROCEDURE IF NOT EXISTS passwordChangeVerification (IN PasswordChangeRequired BOOLEAN)
    BEGIN
        UPDATE Authentication
        SET PasswordChangeRequired = TRUE
        WHERE hashedPassword IS NULL;
    END
    """
    cursor.execute(passwordChangeVerification)
    connection.commit()
    print("passwordChangeVerification procedure created.")

def createViewAdminUsersView(connection,cursor):
    adminUsersView = """
    CREATE OR REPLACE VIEW adminUsersView AS
    SELECT u.userID AS userId, u.firstName AS firstName, u.lastName AS lastName, u.userEmail AS userEmail, u.preferredPaymentMethod AS preferredPaymentMethod, ur.roleDescription AS userRole
        FROM Users u
        JOIN UserRole ur ON u.userRoleID = ur.userRoleID
        WHERE u.isDeleted = FALSE;
    """
    cursor.execute(adminUsersView)
    connection.commit()
    print("adminUsersView view created.")

def createViewAdminInventoryView(connection,cursor):
    adminInventoryView = """
    CREATE OR REPLACE VIEW adminInventoryView AS
        SELECT p.productID AS productId, p.productName AS productName, p.productColor AS productColor, p.itemDescription AS itemDescription, p.price AS price, i.currentStockLevel AS currentStockLevel
        FROM Products p
        JOIN Inventory i ON p.productID = i.productID;
    """
    cursor.execute(adminInventoryView)
    connection.commit()
    print("adminInventoryView view created.")

def createViewUserProfiles(connection,cursor):
    userProfiles = """
    CREATE OR REPLACE VIEW userProfiles AS 
    SELECT users.userID AS userID, users.firstName AS firstName, users.lastName AS lastName, users.userEmail AS userEmail, users.preferredPaymentMethod AS preferredPaymentMethod, userRole.roleDescription AS userRole 
    FROM users 
    JOIN userRole ON users.userRoleID = userRole.userRoleID;
    """
    cursor.execute(userProfiles)
    connection.commit()
    print("userProfiles view created.")

def createViewProductDetailView(connection,cursor):
    productDetailView = """
    CREATE OR REPLACE VIEW productDetailView AS
    SELECT p.productID AS productId, 
           p.productName AS productName, 
           p.productColor AS productColor, 
           p.itemDescription AS itemDescription, 
           p.price AS price, 
           i.currentStockLevel AS currentStockLevel
    FROM Products p
    JOIN Inventory i ON p.productID = i.productID;
    """
    cursor.execute(productDetailView)
    connection.commit()
    print("productDetailView view created.")

def createViewDistributionCenterView(connection,cursor):
    distributionCenterView = """
    CREATE OR REPLACE VIEW distributionCenterView AS
    SELECT s.siteID AS siteId, s.dODAddressCode AS dODAddressCode, s.facilityNo AS facilityNo, s.siteName AS siteName, s.sitePhone AS sitePhone, s.shippingAddress AS shippingAddress, s.shippingCity AS shippingCity, s.shippingState AS shippingState, s.shippingZip AS shippingZip
    FROM DistributionCenter s;
    """
    cursor.execute(distributionCenterView)
    connection.commit()
    print("distributionCenterView view created.")

def createViewOrderView(connection,cursor):
    orderView = """
    CREATE OR REPLACE VIEW orderView AS
    SELECT o.orderID AS orderId, o.userID AS userId, u.firstName AS userFirstName, u.lastName AS userLastName, o.siteID AS siteId, s.siteName AS siteName, o.orderDetails AS orderDetails, o.totalCost AS totalCost, o.orderStatus AS orderStatus
    FROM Orders o
    JOIN Users u ON o.userID = u.userID
    JOIN DistributionCenter s ON o.siteID = s.siteID
    WHERE u.isDeleted = FALSE;
    """
    cursor.execute(orderView)
    connection.commit()
    print("orderView view created.")

def createViewWarehouseNotificationsView(connection,cursor):
    warehouseNotificationsView = """
    CREATE OR REPLACE VIEW warehouseNotificationsView AS 
    SELECT warehouseNotification.notificationID AS notificationID, orders.orderID AS orderID, users.firstName AS firstName, users.lastName AS lastName, warehouseNotification.notificationTimestamp AS notificationTimestamp, distributionCenter.siteName AS siteName FROM warehouseNotification 
    JOIN orders ON warehouseNotification.orderID = orders.orderID 
    JOIN users ON orders.userID = users.userID 
    JOIN distributionCenter ON warehouseNotification.siteID = distributionCenter.siteID;
    """
    cursor.execute(warehouseNotificationsView)
    connection.commit()
    print("warehouseNotificationsView view created.")


def createViewPaymentNotificationsView(connection,cursor):
    paymentNotificationsView = """
    CREATE OR REPLACE VIEW paymentNotificationsView AS 
    SELECT paymentNotification.paymentID AS paymentID, orders.orderID AS orderID, users.firstName AS firstName, users.lastName AS lastName, paymentNotification.timestamp AS timestamp 
    FROM paymentNotification 
    JOIN orders ON paymentNotification.orderID = orders.orderID 
    JOIN users ON orders.userID = users.userID;
    """
    cursor.execute(paymentNotificationsView)
    connection.commit()
    print("paymentNotificationsView view created.")

def createViewUserActivityLogs(connection,cursor):
    userActivityLogs = """
    CREATE OR REPLACE VIEW userActivityLogs AS 
    SELECT auditLog.logID AS logID, users.firstName AS firstName, users.lastName AS lastName, auditLog.activityType AS activityType, auditLog.activityTimestamp AS activityTimestamp, auditLog.itemDescription AS itemDescription 
    FROM auditLog 
    JOIN users ON auditLog.userID = users.userID;
    """
    cursor.execute(userActivityLogs)
    connection.commit()
    print("userActivityLogs view created.")

# Read all from user table
def readAllUsers(cursor):
    sql_query = ("SELECT * FROM users")
    cursor.execute(sql_query)
    print("This is a test to pull all data from users table.")
    print(cursor.fetchall())
    print("Test successful. Congrats, this works.")

if __name__ == "__main__":

    # Replace parameters with DB information
    host_name = "localhost"
    user_name = "root"
    user_password = "SoPAStudentDB!#!"
    db_name = "aafesorder"

    # Initialize database connection
    connection = connectToDatabase(host_name, user_name, user_password, db_name)

    # Initialize database cursor
    cursor = connection.cursor()

    # Create all tables and alter statements
    createUserRoleTable(connection, cursor)
    createUsersTable(connection, cursor)
    createDistributionCenterTable(connection, cursor)
    createOrdersTable(connection, cursor)
    createAuthenticationTable(connection, cursor)
    createOrderDetailTable(connection, cursor)
    createCustomizationTable(connection, cursor)
    createProductsTable(connection, cursor)
    createInventoryTable(connection, cursor)
    createAuditLogTable(connection, cursor)
    createWarehouseNotificationTable(connection, cursor)
    createPaymentNotificationTable(connection, cursor)
    runAlterStatements(connection, cursor)

    # Create procedures
    createProcedureSoftDeleteUser(connection, cursor)
    createProcedurePasswordChangeVerification(connection, cursor)

    # Create views
    createViewAdminUsersView(connection, cursor)
    createViewAdminInventoryView(connection, cursor)
    createViewUserProfiles(connection, cursor)
    createViewProductDetailView(connection, cursor)
    createViewDistributionCenterView(connection, cursor)
    createViewOrderView(connection, cursor)
    createViewPaymentNotificationsView(connection, cursor)
    createViewWarehouseNotificationsView(connection, cursor)
    createViewUserActivityLogs(connection, cursor)


    # Read user table
    readAllUsers(cursor)
    
    app = App()
    app.mainloop()

    # Closing connection when done
    if connection:
        connection.close()
