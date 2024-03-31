import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk, messagebox
import hashlib
import mysql.connector
from mysql.connector import Error


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
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
        # Centered frame for widgets
        center_frame = tk.Frame(self, bg=self.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, image=self.logo_image, bg=self.colors['bg']).grid(row=0, columnspan=2, pady=10)
        tk.Label(center_frame, text="Username", bg=self.colors['bg'], font=("Helvetica", 14)).grid(row=1, column=0, pady=10, sticky="e")
        self.username_entry = tk.Entry(center_frame, font=("Helvetica", 14))
        self.username_entry.grid(row=1, column=1, pady=10, sticky="ew")
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
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if both username and password are blank
        if not username and not password:
            # Allow login for blank username and password
            self.master.show_frame(DashboardFrame)
            return

        # Connect to the MySQL database
        try:
            connection = mysql.connector.connect(
                host="your_host",
                user="your_username",
                password="your_password",
                database="your_database"
            )
            cursor = connection.cursor()

            # Hash the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Execute the query to check if the credentials are valid
            query = "SELECT * FROM YourTableName WHERE Username = %s AND HashedPassword = %s"
            cursor.execute(query, (username, hashed_password))
            result = cursor.fetchone()

            if result:
                # Credentials are valid, navigate to DashboardFrame
                self.master.show_frame(DashboardFrame)
            else:
                # Invalid credentials, display an error message box
                messagebox.showerror("Login Attempt Failed", "Invalid username or password.")

        except mysql.connector.Error as error:
            # Handle any errors that occur during database connection or query execution
            print("Error:", error)

        finally:
            # Close the database connection
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

        # Placeholder for the function's implementation
        # Implement the logic to update user information in the database
        print("Updated User Information:", updated_user_info)







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
    cursor.execute("CREATE TABLE IF NOT EXISTS UserRole (UserRoleID int NOT NULL AUTO_INCREMENT,RoleDescription varchar(50) UNIQUE,PRIMARY KEY (UserRoleID))")
    connection.commit()
    print("UserRole table created.")

def createUsersTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  Users (UserID int NOT NULL AUTO_INCREMENT, FirstName varchar(100) NOT NULL, LastName varchar(100) NOT NULL, UserRoleID int, UserEmail varchar(100), PreferredPaymentMethod varchar(100), isDeleted BOOLEAN DEFAULT FALSE, PRIMARY KEY (UserID))")
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
        "CREATE TABLE IF NOT EXISTS  Products (ProductID int NOT NULL, ProductName varchar(255) NOT NULL UNIQUE, ProductColor varchar(100), ItemDescription varchar(255), ProductImage blob, Price decimal(5,2)  CHECK (Price >= 0), PRIMARY KEY (ProductID))")
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
    sql_query = ("SELECT * FROM Users")
    cursor.execute(sql_query)
    print("This is a test to pull all data from users table.")
    print(cursor.fetchall())
    print("Test successful. Congrats, this works.")


def insertProducts(connection, cursor):
    insertIntoProducts = """
    REPLACE INTO Products (ProductID, ProductName, ProductColor, ItemDescription, Price)
    VALUES (100, 'Bubba 40oz Radiant Stainless Steel Rubberized Water Bottle, Cobalt', 'Cobalt', "Hanging with friends at a music festival or heading to the beach? Bring the bubba 40 oz. Radiant Stainless Steel Rubberized Water Bottle with Straw along for the fun. The leakproof lid is easy to open with just the push of a button so you can hydrate quickly without the mess. Plus, your favorite drinks stay cold for 12 hours thanks to the vacuum-insulated stainless steel. When you're done drinking, close the cap to help protect the spout and straw from dirt and grime and slide the button to lock it in place. A comfortable, pivotal carry handle lets you easily carry even a full bottle with you while walking along the beach or checking out the festival grounds. Size: 40 oz. Model: 2166196.", 30.99),
    (101, 'Bubba 40oz Radiant Stainless Steel Rubberized Water Bottle, Licorice', 'Licorice', "Hanging with friends at a music festival or heading to the beach? Bring the bubba 40 oz. Radiant Stainless Steel Rubberized Water Bottle with Straw along for the fun. The leakproof lid is easy to open with just the push of a button so you can hydrate quickly without the mess. Plus, your favorite drinks stay cold for 12 hours thanks to the vacuum-insulated stainless steel. When you're done drinking, close the cap to help protect the spout and straw from dirt and grime and slide the button to lock it in place. A comfortable, pivotal carry handle lets you easily carry even a full bottle with you while walking along the beach or checking out the festival grounds. Size: 40 oz. Model: 2166196.", 30.99),
    (102, 'Bubba Hero Mug', 'Black', "Save your workday from cold coffee with the Bubba 18oz Hero Vacuum-Insulated Stainless Steel Travel Mug. Your drink stays hot up to 6 hours or cold up to 24 thanks to vacuum-insulated stainless steel, perfect in case you get stuck in a meeting and can't get back to your beverage. Sip from the leak-proof lid just by flipping up the locking flap, and snap it shut when you're finished to lock in the heat. A silicone base keeps the travel mug from sliding across your desk. When you're on the move, grab the comfortable handle and go! With the Hero Dual-Wall Vacuum-Insulated Stainless Steel Travel Mug, you're ready to get a handle on your day. Model: 2145787.", 25.99),
    (103, 'Bubba Radiant Stainless Steel Rubberized Water Bottle with Straw 32 oz.', 'Blue', "Hanging with friends at a music festival or heading to the beach? Bring the Bubba Radiant Stainless Steel Rubberized Water Bottle with Straw, 32 oz., along for the fun. The leakproof lid is easy to open with just the push of a button so you can hydrate quickly without the mess. Plus, your favorite drinks stay cold for 12 hours thanks to the vacuum-insulated stainless steel. When you’re done drinking, close the cap to help protect the spout and straw from dirt and grime and slide the button to lock it in place. A comfortable, pivotable carry handle lets you easily carry the bottle with you while walking along the beach or checking out the festival grounds. Model: 2166132.", 26.99),
    (104, "Bubba Flo Refresh Crystle Ice Kid's Water Bottle 16 oz.", '', "Teach your kids good hydration habits with the bubba Flo Kids 16 oz. Water Bottle with Silicone Sleeve. It features a leak-proof lid and a handy button lock to prevent accidental openings, keeping the inside of your car safe from spills. With a high-flow chug lid, kids can quickly hydrate without missing their turn on the monkey bars. A built-in spout cover keeps out dirt and germs.", 11.99),
    (105, 'Bubba 32 oz. Radiant Stainless Steel Rubberized Water Bottle, Licorice', 'Licorice', "Hanging with friends at a music festival or heading to the beach? Bring the bubba 32 oz. Radiant Stainless Steel Rubberized Water Bottle with Straw along for the fun. The leakproof lid is easy to open with just the push of a button so you can hydrate quickly without the mess. Plus, your favorite drinks stay cold for 12 hours thanks to the vacuum-insulated stainless steel. When you're done drinking, close the cap to help protect the spout and straw from dirt and grime and slide the button to lock it in place. A comfortable, pivotal carry handle lets you easily carry the bottle with you while walking along the beach or checking out the festival grounds. Size: 32 oz. Model: 2166127.", 26.99);
    """
    cursor.execute(insertIntoProducts)
    connection.commit()
    print("Sample product data created.")

def insertDistributionCenter(connection, cursor):
    insertIntoDistributionCenter = """
    INSERT IGNORE INTO DistributionCenter (SiteID, DODAddressCode, FacilityNo, FacilityNoLong, SiteName, SitePhone, ShippingAddress,ShippingAddress2, ShippingAddress3, ShippingAddress4, ShippingCity, ShippingState, ShippingZip)
    VALUES (101, 'K885', '1010204', '3468142200', 'LRK LAKESIDE EXP/GAS', '501-988-4888', 'LAKESIDE EXPRESS', 'BLDG 1996 CHIEF WILLIAMS', '', '', 'LITTLE ROCK', 'AR', '720990000');
    """
    cursor.execute(insertIntoDistributionCenter)
    connection.commit()
    print("Sample distribution center data created.")

def insertUsers(connection, cursor):
    insertIntoUsers = """
    INSERT IGNORE INTO Users (UserID, FirstName, LastName, UserRoleID, UserEmail, PreferredPaymentMethod, isDeleted)
    VALUES (10210, 'Johnny', 'Donuts', 1, 'jd@email.com', 'Paypal', FALSE);
    """
    cursor.execute(insertIntoUsers)
    connection.commit()
    print("Sample user data created.")

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

    # Insert sample user into DB
    insertUsers(connection, cursor)

    # Inserting products into DB
    insertProducts(connection, cursor)

    # Insert sample warehouse DB
    insertDistributionCenter(connection, cursor)



    # Read user table
    readAllUsers(cursor)

    app = App()
    app.mainloop()

    # Closing connection when done
    if connection:
        connection.close()
