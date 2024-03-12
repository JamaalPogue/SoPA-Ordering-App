import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk, messagebox
import hashlib
import mysql.connector


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





if __name__ == "__main__":
    app = App()
    app.mainloop()
