import tkinter as tk
from tkinter import Canvas, Scrollbar, Frame, PhotoImage, messagebox, simpledialog, ttk, OptionMenu, StringVar, DoubleVar
import uuid
import smtplib
import decimal
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib
import mysql.connector
from mysql.connector import Error
import csv
import datetime

class PaymentForm(simpledialog.Dialog):
    def __init__(self, parent, title, total_cost):
        self.total_cost = total_cost
        super().__init__(parent, title)

    def body(self, frame):
        # Display total cost
        tk.Label(frame, text=f"Total Cost: ${self.total_cost:.2f}", font=("Arial", 14)).grid(row=0, columnspan=2, pady=(10, 20), sticky="nsew")

        # Payment method selection
        tk.Label(frame, text="Select Payment Method:", font=("Arial", 12)).grid(row=1, columnspan=2, sticky="w")

        self.payment_method_var = tk.StringVar(value="Card")
        payment_methods = ["Card", "PayPal", "Apple Pay", "Google Pay"]
        for idx, method in enumerate(payment_methods):
            tk.Radiobutton(frame, text=method, variable=self.payment_method_var, value=method,
                           font=("Arial", 10), command=self.update_payment_method).grid(row=2+idx, columnspan=2, sticky="w")

        self.payment_details_frame = tk.Frame(frame)
        self.payment_details_frame.grid(row=6, columnspan=2, sticky="ew")
        self.update_payment_method()

    def update_payment_method(self):
        # Clear current widgets in payment_details_frame
        for widget in self.payment_details_frame.winfo_children():
            widget.destroy()

        method = self.payment_method_var.get()
        if method == "Card":
            self.card_details()
        elif method == "PayPal":
            self.paypal_details()
        # Extend for other methods

    def card_details(self):
        # Card Number
        tk.Label(self.payment_details_frame, text="Card Number:", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
        self.card_number_entry = tk.Entry(self.payment_details_frame, font=("Arial", 12))
        self.card_number_entry.grid(row=0, column=1, padx=5, pady=5)

        # Expiry Date
        tk.Label(self.payment_details_frame, text="Expiry Date (MM/YY):", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
        self.card_expiry_entry = tk.Entry(self.payment_details_frame, font=("Arial", 12))
        self.card_expiry_entry.grid(row=1, column=1, padx=5, pady=5)

        # CVV
        tk.Label(self.payment_details_frame, text="CVV:", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
        self.card_cvv_entry = tk.Entry(self.payment_details_frame, font=("Arial", 12))
        self.card_cvv_entry.grid(row=2, column=1, padx=5, pady=5)

        # Cardholder Name
        tk.Label(self.payment_details_frame, text="Cardholder Name:", font=("Arial", 12)).grid(row=3, column=0, sticky="w")
        self.cardholder_name_entry = tk.Entry(self.payment_details_frame, font=("Arial", 12))
        self.cardholder_name_entry.grid(row=3, column=1, padx=5, pady=5)

    def paypal_details(self):
        # PayPal Email
        tk.Label(self.payment_details_frame, text="PayPal Email:", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
        self.paypal_email_entry = tk.Entry(self.payment_details_frame, font=("Arial", 12))
        self.paypal_email_entry.grid(row=0, column=1, padx=5, pady=5)

    def apply(self):
        payment_method = self.payment_method_var.get()
        details = ""
        if payment_method == "Card":
            details = f"Card Number: {self.card_number_entry.get()}, " \
                    f"Expiry: {self.card_expiry_entry.get()}, " \
                    f"CVV: {self.card_cvv_entry.get()}, " \
                    f"Name: {self.cardholder_name_entry.get()}"
            # Validate card details
            if not self.validate_card_details():
                messagebox.showerror("Invalid Card Details", "Please enter valid card details.")
                return
        elif payment_method == "PayPal":
            details = f"PayPal Email: {self.paypal_email_entry.get()}"
        
        # Simulate payment always being accepted
        payment_success = True
        
        if payment_success:
            # Set a flag indicating successful payment
            self.payment_success = True
            messagebox.showinfo("Payment Processed", f"Your payment through {payment_method} has been processed.\nDetails: {details}")
        else:
            # Set a flag indicating payment failure
            self.payment_success = False
            messagebox.showerror("Payment Failed", "Payment failed. Please try again.")

    def validate_card_details(self):
        # Validate card details
        card_number = self.card_number_entry.get()
        card_expiry = self.card_expiry_entry.get()
        card_cvv = self.card_cvv_entry.get()
        cardholder_name = self.cardholder_name_entry.get()

        # Basic validation
        if len(card_number) != 16:
            return False
        if len(card_expiry) != 5:
            return False
        if len(card_cvv) != 3:
            return False
        if not cardholder_name:
            return False

        return True

class CartManager:
    def __init__(self):
        self.items = {}
        self.product_details = {}  # To store price, color, and customization details
        self.observers = []  # List to hold references to observer functions

    def add_observer(self, observer_func):
        """Registers a function to be called for updates."""
        self.observers.append(observer_func)

    def notify_observers(self):
        """Notifies all registered observers of changes."""
        for observer in self.observers:
            observer()


    def add_item(self, product_id, product_name, quantity, price, color, customization, customized=False):
        itemQty = checkItemQuantity(connection, cursor, product_id)  # This will check the quantity of the item in inventory
        if itemQty == 0: # If there is none in inventory, skip the process.
            print("Item is out of stock.")
            messagebox.showerror("Out Of Stock", "Item is out of stock at the warehouse. Please choose a different product.")
        else:
            if product_id not in self.items:
              self.items[product_id] = {'product_name': product_name, 'quantity': 0, 'price': price, 'color': color, 'customization': customization, 'customized': customized}
            self.items[product_id]['quantity'] += quantity
            if product_id in self.items:
                if self.items[product_id] >= itemQty:
                    print("Maximum Order Reached.")
                    messagebox.showerror("Maximum Order Reached", "You have added the maximum available quantity of this item.")
                else:
                    self.items[product_id] += quantity
            else:
                self.items[product_id] = quantity
        if price is not None:
            self.product_prices[product_id] = price


        
        self.notify_observers()



    def remove_item(self, product_id, quantity=1):
        if product_id in self.items:
            self.items[product_id]['quantity'] -= quantity
            if self.items[product_id]['quantity'] <= 0:
                del self.items[product_id]
        self.notify_observers()  # Call to notify observers about the change

    def clear_cart(self):
        self.items = {}
        self.notify_observers()  # Call to notify observers about the change

    def remove_item_completely(self, product_id):
        if product_id in self.items:
            del self.items[product_id]
        self.notify_observers()  # Call to notify observers about the change

    def calculate_total_cost(self):
        total_cost = 0
        for product_id, details in self.items.items():
            total_cost += details['price'] * details['quantity']
        return round(total_cost, 2) #Two decimal places

    def get_cart_contents(self):
        return self.items

    def get_product_prices(self):
        return {pid: details['price'] for pid, details in self.items.items()}

class BaseFrame(tk.Frame):
    def __init__(self, master, colors, logo, login_manager=None):
        super().__init__(master, bg=colors['bg'])
        self.grid(sticky="nsew")
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        self.logo_image = logo
        self.colors = colors
        self.login_manager = login_manager  # Assign the login_manager object
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
                                 command=self.login)  # Ensure this calls the login method correctly
        login_button.grid(row=3, columnspan=2, pady=20)
        exit_button = tk.Button(self, text="Exit Application", bg=self.colors['exit_button_bg'], fg="white",
                                command=self.master.destroy, font=("Arial", 12))
        exit_button.place(relx=1.0, rely=0.0, anchor="ne", width=120, height=50)

    def authenticate_user(self, username, password):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="SoPAStudentDB!#!",
                database="AAFESOrder",
            )
            cursor = connection.cursor()

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            query = """
            SELECT u.UserID
            FROM Authentication a
            JOIN Users u ON a.UserID = u.UserID
            WHERE u.UserEmail = %s AND a.HashedPassword = %s
            """
            cursor.execute(query, (username, hashed_password))
            result = cursor.fetchone()

            if result:
                # Credentials are valid, return the user_id
                return result[0]

        except mysql.connector.Error as error:
            print("Error:", error)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        # If authentication fails, return None
        return None

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if both username and password are blank
        if not username and not password:
            # Allow login for blank username and password
            self.master.show_frame(DashboardFrame)
            return

        # Authenticate user
        user_id = self.authenticate_user(username, password)

        if user_id:
            # Set current_user_id in the App class
            self.master.current_user_id = user_id
            self.master.show_frame(DashboardFrame)
        else:
            # Invalid credentials, display an error message box
            messagebox.showerror("Login Attempt Failed", "Invalid username or password.")

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
    def __init__(self, master, colors, logo_image, login_manager=None):
        super().__init__(master, colors, logo_image, login_manager)
        self.items = {}

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

    def add_item(self, product_id, quantity=1):
        if product_id in self.items:
            self.items[product_id] += quantity
        else:
            self.items[product_id] = quantity

    def remove_item(self, product_id, quantity=1):
        if product_id in self.items:
            self.items[product_id] -= quantity
            if self.items[product_id] <= 0:
                del self.items[product_id]

    def get_cart_contents(self):
        return self.items

    def clear_cart(self):
        self.items = {}
        
    def remove_item_completely(self, product_id):
        if product_id in self.items:
            del self.items[product_id]

class WaterBottleFrame(tk.Frame):
    def __init__(self, parent, colors, db_info, cart_manager, logo_image):
        super().__init__(parent)
        self.colors = colors
        self.db_info = db_info
        self.cart_manager = cart_manager
        self.logo_image = logo_image
        self.images = {}
        self.create_widgets()

    def create_widgets(self):
        self.display_products()
        back_button = tk.Button(self, text="Back to Product Order", bg=self.colors['button_bg'], fg=self.colors['button_fg'],
                                font=("Helvetica", 14), activebackground=self.colors['button_active_bg'],
                                command=lambda: self.master.show_frame(ProductOrderFrame))
        back_button.grid(row=0, column=0, pady=10, sticky="w")
        exit_button = tk.Button(self, text="Exit Application", bg=self.colors['exit_button_bg'], fg="white",
                                command=self.master.destroy, font=("Arial", 12))
        exit_button.place(relx=1.0, rely=0.0, anchor="ne", width=120, height=50)

    def display_products(self):
        water_bottle_products = [
            (101, 'Bubba 40oz Water Bottle', 'Leakproof lid, cold for 12 hours, vacuum-insulated.', 30.99, 'BubbaLicorice.png', ['Blue', 'Green']),
            (102, 'Bubba Hero Mug', 'Hot up to 6 hours or cold up to 24, leak-proof.', 25.99, 'BubbaHero.png', ['Blue', 'Green']),
            (103, 'Bubba Radiant Water Bottle 32 oz.', 'Leakproof, vacuum-insulated stainless steel, 32 oz.', 26.99, 'BubbaRadiant.png', ['Blue', 'Green']),
            (104, 'Bubba Flo Kids Water Bottle 16 oz.', 'Leak-proof lid, high-flow chug lid, 16 oz.', 11.99, 'BubbaFlo.png', ['Blue', 'Green']),
            (105, 'Bubba 32 oz. Water Bottle, Licorice', 'Leakproof, cold for 12 hours, vacuum-insulated, 32 oz.', 26.99, 'BubbaLicorice.png', ['Blue', 'Green'])
        ]

        row = 1
        for product_id, name, description, base_price, image_filename, colors in water_bottle_products:
            try:
                image = PhotoImage(file=f"./Images/{image_filename}").subsample(9, 9)
                self.images[product_id] = image
                label_image = tk.Label(self, image=image)
                label_image.grid(row=row, column=0, padx=5, pady=2)
            except Exception as e:
                print(f"Error loading image {image_filename}: {e}")
                continue

            # Product title and description
            label_text = f"{name}: {description}"
            label_description = tk.Label(self, text=label_text, wraplength=200, justify="left")
            label_description.grid(row=row, column=1, padx=5, pady=2)

            # Dropdown for color selection
            color_var = tk.StringVar(value=colors[0])  # default color
            color_menu = tk.OptionMenu(self, color_var, *colors)
            color_menu.grid(row=row, column=2, padx=5, pady=2)

            # Price label and customization dropdown
            price_var = tk.DoubleVar(value=base_price)  # Store the base price initially
            price_label = tk.Label(self, text=f"Price: ${price_var.get():.2f}")
            price_label.grid(row=row, column=4, sticky="w", padx=5, pady=2)

            customization_options = ['None', 'Patriotic (General)', 'Space Force', 'Marines', 'Coast Guard', 'Army', 'Navy', 'Army National Guard', 'Air Force']
            customization_var = tk.StringVar(value='None')
            customization_menu = tk.OptionMenu(self, customization_var, *customization_options,
                                               command=lambda choice, var=price_var, lbl=price_label: self.update_price(choice, var, lbl, base_price))
            customization_menu.grid(row=row, column=3, padx=5, pady=2)

            add_to_cart_button = tk.Button(self, text="Add to Cart", bg=self.colors['button_bg'], fg=self.colors['button_fg'],
                                           command=lambda pid=product_id, pname=name, p=price_var, c=color_var, cm=customization_var: self.add_to_cart(pid, pname, p.get(), c.get(), cm.get()))
            add_to_cart_button.grid(row=row, column=5, padx=5, pady=2)



            row += 1

    def update_price(self, customization, price_var, price_label, base_price):
        if customization == 'Patriotic (General)':
            new_price = base_price + 2
        elif customization in ['Space Force', 'Marines', 'Coast Guard', 'Army', 'Navy', 'Army National Guard', 'Air Force']:
            new_price = base_price + 5
        else:
            new_price = base_price
        price_var.set(new_price)
        price_label.config(text=f"Price: ${new_price:.2f}")  # Update the label text

    def add_to_cart(self, product_id, product_name, price, color, customization):
        # Convert price to float to ensure consistent data type
        price = float(price) if isinstance(price, decimal.Decimal) else price
        self.cart_manager.add_item(product_id, product_name, 1, price, color, customization, customized=(customization != 'None'))
        messagebox.showinfo("Success", f"Added {product_name} with customization '{customization}' and color '{color}' to cart at price ${price:.2f}.")

class YogaMatFrame(tk.Frame):
    def __init__(self, parent, colors, db_info, cart_manager, logo_image):
        super().__init__(parent)
        self.colors = colors
        self.db_info = db_info
        self.cart_manager = cart_manager
        self.logo_image = logo_image
        self.images = {}
        self.create_widgets()

    def create_widgets(self):
        self.display_products()
        back_button = tk.Button(self, text="Back to Product Order", bg=self.colors['button_bg'], fg=self.colors['button_fg'],
                                font=("Helvetica", 14), activebackground=self.colors['button_active_bg'],
                                command=lambda: self.master.show_frame(ProductOrderFrame))
        back_button.grid(row=0, column=0, pady=10, sticky="w")
        exit_button = tk.Button(self, text="Exit Application", bg=self.colors['exit_button_bg'], fg="white",
                                command=self.master.destroy, font=("Arial", 12))
        exit_button.place(relx=1.0, rely=0.0, anchor="ne", width=120, height=50)

    def display_products(self):
        yoga_mat_products = [
            (201, 'GoFit Double Thick Yoga Mat', 'Excellent nonslip surface ideal for yoga practice.', 39.99, 'GoFitDoubleThick.png', ['Blue', 'Green']),
            (202, 'GoFit Yoga Mat', 'Provides comfort and protection for Yoga poses.', 24.99, 'GoFitYogaMat.png', ['Blue', 'Green']),
            (203, 'GoFit Pattern Yoga Mat', 'Non-slip surface, includes yoga pose wall chart.', 21.49, 'GoFitPatternMat.png', ['Blue', 'Green']),
            (204, 'GoFit Summit Yoga Mat', 'Professional grade mat, extra-cushioned surface.', 69.99, 'GoFitSummitYogaMat.png', ['Blue', 'Green']),
            (205, 'GoFit Yoga Kit', 'Everything needed for a complete Yoga workout.', 25.50, 'GoFitYogaKit.png', ['Blue', 'Green'])
        ]

        row = 1
        column = 0  # Start placing items in the left column
        for idx, (product_id, name, description, base_price, image_filename, colors) in enumerate(yoga_mat_products):
            if idx == 3:  # Switch to the right column after the first three items
                column = 1
                row = 1

            try:
                image = PhotoImage(file=f"./Images/{image_filename}").subsample(9, 9)
                self.images[product_id] = image
                label_image = tk.Label(self, image=image)
                label_image.grid(row=row, column=column*6, padx=5, pady=2, sticky="w")
            except Exception as e:
                print(f"Error loading image {image_filename}: {e}")
                continue

            label_text = f"{name}: {description}"
            label_description = tk.Label(self, text=label_text, wraplength=200, justify="left")
            label_description.grid(row=row, column=1+column*6, padx=5, pady=2, sticky="w")

            color_var = StringVar(value=colors[0])
            color_menu = OptionMenu(self, color_var, *colors)
            color_menu.grid(row=row, column=2+column*6, padx=5, pady=2)

            price_var = DoubleVar(value=base_price)
            price_label = tk.Label(self, text=f"Price: ${price_var.get():.2f}")
            price_label.grid(row=row, column=4+column*6, sticky="w", padx=5, pady=2)

            customization_options = ['None', 'Patriotic (General)', 'Space Force', 'Marines', 'Coast Guard', 'Army', 'Navy', 'Army National Guard', 'Air Force']
            customization_var = StringVar(value='None')
            customization_menu = OptionMenu(self, customization_var, *customization_options,
                                            command=lambda event=None, c_var=customization_var, p_var=price_var, p_label=price_label, base=base_price: self.update_price(c_var, p_var, p_label, base))
            customization_menu.grid(row=row, column=3+column*6, padx=5, pady=2)

            add_to_cart_button = tk.Button(self, text="Add to Cart", bg=self.colors['button_bg'], fg=self.colors['button_fg'],
                                           command=lambda pid=product_id, pname=name, p=price_var, c=color_var, cm=customization_var: self.add_to_cart(pid, pname, p.get(), c.get(), cm.get()))
            add_to_cart_button.grid(row=row, column=5+column*6, padx=5, pady=2)


            row += 1

    def update_price(self, customization_var, price_var, price_label, base_price):
        selected_customization = customization_var.get()
        if selected_customization == 'Patriotic (General)':
            new_price = base_price + 2
        elif selected_customization in ['Space Force', 'Marines', 'Coast Guard', 'Army', 'Navy', 'Army National Guard', 'Air Force']:
            new_price = base_price + 5
        else:
            new_price = base_price

        price_var.set(new_price)
        price_label.config(text=f"Price: ${new_price:.2f}")

    def add_to_cart(self, product_id, product_name, price, color, customization):
        self.cart_manager.add_item(product_id, product_name, 1, float(price), color, customization, customized=(customization != 'None'))
        messagebox.showinfo("Success", f"Added {product_name} with customization '{customization}' and color '{color}' to cart at price ${price:.2f}.")

class CartFrame(tk.Frame):
    def __init__(self, parent, colors, db_info, cart_manager, logo_image):
        super().__init__(parent)
        self.colors = colors
        self.db_info = db_info
        self.cart_manager = cart_manager
        self.logo_image = logo_image
        self.cart_manager.add_observer(self.update_cart_display)  # Register as observer to the cart manager
        self.create_widgets()
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def create_widgets(self):
        self.cart_items_frame = tk.Frame(self)
        self.cart_items_frame.grid(row=1, column=1, columnspan=2, sticky="nsew")

        tk.Label(self.cart_items_frame, text="Your Cart:", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")

        add_more_button = tk.Button(self, text="Add More to Order", bg=self.colors['button_bg'], fg=self.colors['button_fg'],
                                    font=("Helvetica", 14), activebackground=self.colors['button_active_bg'],
                                    command=self.add_more_to_order, width=20)
        add_more_button.grid(row=2, column=1, padx=20, pady=10, sticky="sew")
        
        submit_order_button = tk.Button(self, text="Submit Order", bg=self.colors['button_bg'], fg=self.colors['button_fg'],
                                        font=("Helvetica", 14), activebackground=self.colors['button_active_bg'],
                                        command=self.submit_order, width=20)
        submit_order_button.grid(row=3, column=1, padx=20, pady=10, sticky="sew")

        exit_button = tk.Button(self, text="Exit Application", bg=self.colors['exit_button_bg'], fg="white",
                                command=self.master.destroy, font=("Arial", 12))
        exit_button.place(relx=1.0, rely=0.0, anchor="ne", width=120, height=50)

        self.update_cart_display()

    def update_cart_display(self):
        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()

        tk.Label(self.cart_items_frame, text="Your Cart:", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")
    
        cart_contents = self.cart_manager.get_cart_contents()
        if cart_contents:
            index = 1
            for product_id, details in cart_contents.items():
                product_name = details['product_name']
                quantity = details['quantity']
                price = float(details['price'])
                total_price = price * quantity
                tk.Label(self.cart_items_frame, text=f"{product_name} - Quantity: {quantity} - ${total_price:.2f}", font=("Helvetica", 12)).grid(row=index, column=0, sticky="w")
                index += 1
        else:
            tk.Label(self.cart_items_frame, text="Your cart is empty.", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w")

    def submit_order(self):
        user_id = self.master.current_user_id
        if not user_id:
            messagebox.showerror("User Not Logged In", "Please log in to submit an order.")
            return

        total_cost = self.cart_manager.calculate_total_cost()
        if total_cost > 0:
            payment_dialog = PaymentForm(self, "Payment Information", total_cost)
            if hasattr(payment_dialog, 'payment_success') and payment_dialog.payment_success:
                try:

                    # if user_email:
                    #     self.send_confirmation_email(user_email, order_id)
                    # else:
                    #     messagebox.showwarning("Warning", "No email found for user. Order submitted, but confirmation email not sent.")
                    # updateInventoryAfterPurchase(self, user_id)
                    order_id = self.place_order_in_database(user_id, total_cost)

                    self.cart_manager.clear_cart()
                    messagebox.showinfo("Order Submitted", "Thank you for your order. Your order has been successfully processed.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to insert order: {e}")
            else:
                messagebox.showinfo("Payment Cancelled", "Payment was cancelled. Order has not been submitted.")
        else:
            messagebox.showinfo("Cart Empty", "Your cart is empty.")

    def place_order_in_database(self, user_id, total_cost):
        connection = mysql.connector.connect(host=self.db_info['host'], user=self.db_info['user'], passwd=self.db_info['passwd'], database=self.db_info['database'])
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT MAX(OrderID) FROM Orders")
            max_id_result = cursor.fetchone()
            next_id = 1 if max_id_result is None or max_id_result[0] is None else max_id_result[0] + 1

            
            order_details = str(self.cart_manager.get_cart_contents())
            total_cost = self.cart_manager.calculate_total_cost()
   


            for item_id, details in self.cart_manager.get_cart_contents().items():
                cursor.execute("SELECT CurrentStockLevel FROM Inventory WHERE ProductID = %s", (item_id,))
                stock_level_result = cursor.fetchone()
                if stock_level_result is None:
                    raise Exception(f"No inventory record found for product ID {item_id}.")
                stock_level = stock_level_result[0]

                if details['quantity'] > stock_level:
                    raise Exception(f"Insufficient stock for {details['product_name']}.")

                cursor.execute("UPDATE Inventory SET CurrentStockLevel = CurrentStockLevel - %s WHERE ProductID = %s",
                               (details['quantity'], item_id))

            # Use the next OrderID for the new order
            cursor.execute("INSERT INTO Orders (OrderID, UserID, OrderDetails, TotalCost, OrderStatus) VALUES (%s, %s, %s, %s, 'Pending')", 
                        (next_id, user_id, order_details, total_cost))
            
            order_id = next_id  # Use next_id as the order_id
            
            
            # Logging order in AuditLog table
            cursor.execute(
                "INSERT INTO AuditLog (UserID, ActivityType, AffectedRecordID, ItemDescription) VALUES (%s, %s, %s, %s)",
                (user_id, 'Order Placed', next_id, order_details))
            
            for item_id, details in self.cart_manager.get_cart_contents().items():
                cursor.execute("INSERT INTO OrderDetail (OrderID, ProductID, Quantity, Customized, CustomizationID) VALUES (%s, %s, %s, %s, %s)",
                               (next_id, item_id, details['quantity'], details['customized'], details.get('customization_id', None)))


            connection.commit()
        except Exception as e:

            print(f"Database insert error: {e}")
            return None




    #def send_confirmation_email(self, recipient_email, order_id):
        #sender_email = "southblance@example.com"  # Change this to your company's email address
        #smtp_server = "your_company_smtp_server.com"  # Change this to your company's SMTP server address

        #message = MIMEMultipart("alternative")
        #message["Subject"] = "Order Confirmation"
        #message["From"] = sender_email
        #message["To"] = recipient_email
#
        #text = f"Thank you for your order. Your order ID is {order_id}."
        #html = f"""\
        #<html>
        #  <body>
        #    <p>Thank you for your order. Your order ID is {order_id}.</p>
        #  </body>
        #</html>
        #"""

        #part1 = MIMEText(text, "plain")
        #part2 = MIMEText(html, "html")

        #message.attach(part1)
        #message.attach(part2)

        # Adjust the SMTP connection to use your company's SMTP server
        #with smtplib.SMTP(smtp_server) as server:
            #server.sendmail(sender_email, recipient_email, message.as_string())

    def fetch_product_details(self, product_id):
        product_details = None
        try:
            connection = mysql.connector.connect(
                host=self.db_info['host'],
                user=self.db_info['user'],
                passwd=self.db_info['passwd'],
                database=self.db_info['database']
            )
            cursor = connection.cursor(dictionary=True)
            query = "SELECT ProductName, Price FROM Products WHERE ProductID = %s"
            cursor.execute(query, (product_id,))
            product_details = cursor.fetchone()
        except mysql.connector.Error as error:
            print(f"Error fetching product details: {error}")

            connection.rollback()  # Rollback in case of any error
            raise e

        finally:
            cursor.close()
            connection.close()
        return next_id


    def add_more_to_order(self):
        self.master.show_frame(ProductOrderFrame)

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

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initialization of app attributes...
        self.attributes('-fullscreen', False)
        self.db_info = {
            'host': "localhost",
            'user': "root",
            'passwd': "SoPAStudentDB!#!",
            'database': "AAFESOrder",
        }
        self.cart_manager = CartManager()
        self.bind("<Escape>", lambda e: self.attributes('-fullscreen', False))
        self.logo_image = PhotoImage(file="logo.png")  # Ensure correct path is used
        self.colors = {
            'bg': '#FFFFFF',
            'button_bg': '#005a34',
            'button_fg': '#FFFFFF',
            'button_active_bg': '#004225',
            'exit_button_bg': '#007848',
        }

        self.frames = {}
        frame_classes = [LoginFrame, DashboardFrame, UserSettingsFrame, UpdateUserInfoFrame, WaterBottleFrame, YogaMatFrame, CartFrame, ProductOrderFrame]

        for F in frame_classes:
            frame = None
            if F in [WaterBottleFrame, CartFrame, YogaMatFrame]:  # These frames need db_info, cart_manager, logo_image, and colors
                frame = F(self, self.colors, self.db_info, self.cart_manager, self.logo_image)
            elif F in [ProductOrderFrame]:  # Adjusting ProductOrderFrame initialization
                frame = F(self, self.colors, self.logo_image, None)  # Assuming ProductOrderFrame follows BaseFrame's init signature
            elif F in [LoginFrame, DashboardFrame, UserSettingsFrame, UpdateUserInfoFrame]:  # These frames need the logo_image and colors
                frame = F(self, self.colors, self.logo_image)
            else:
                frame = F(self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginFrame)
        
        # Set minimum screen size
        self.minsize(width=800, height=600)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()
        
    def show_frame(self, context):
        print(f"Switching to frame: {context}")  # Debugging line
        frame = self.frames[context]
        frame.tkraise()






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
        "CREATE TABLE IF NOT EXISTS  DistributionCenter (SiteID int NOT NULL AUTO_INCREMENT, DODAddressCode varchar(10), FacilityNo int NOT NULL, FacilityNoLong int, SiteName varchar(255), SitePhone varchar(100), ShippingAddress varchar(255), ShippingAddress2 varchar(255), ShippingAddress3 varchar(255), ShippingAddress4 varchar(255), ShippingCity varchar(255), ShippingState varchar(100), ShippingZip varchar(100), PRIMARY KEY (SiteID))")
    connection.commit()
    print("DistributionCenter table created.")

def createOrdersTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Orders (OrderID int NOT NULL, UserID int, SiteID int, OrderDetails varchar(255), TotalCost decimal(10,2), OrderStatus varchar(255) CHECK (OrderStatus IN ('Pending', 'Completed', 'Canceled')), PRIMARY KEY (OrderID))")
    connection.commit()
    print("Orders table created.")

def createAuthenticationTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  Authentication (AuthenticationID int NOT NULL AUTO_INCREMENT, UserID int, HashedPassword varchar(100), LastPasswordChangeDate date, PasswordChangeRequired boolean DEFAULT FALSE, PRIMARY KEY (AuthenticationID))")
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
        "CREATE TABLE IF NOT EXISTS  Products (ProductID int NOT NULL, ProductName varchar(255) NOT NULL UNIQUE, ItemDescription blob, ProductImage blob, Price decimal(5,2)  CHECK (Price >= 0), PRIMARY KEY (ProductID))")
    connection.commit()
    print("Products table created.")

def createInventoryTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  Inventory (InventoryID int NOT NULL AUTO_INCREMENT, ProductID int, CurrentStockLevel int NOT NULL CHECK (CurrentStockLevel >= 0), PRIMARY KEY (InventoryID))")
    connection.commit()
    print("Inventory table created.")

def createAuditLogTable(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  AuditLog (LogID int NOT NULL AUTO_INCREMENT, UserID int, ActivityType varchar(255), ActivityTimestamp datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, AffectedRecordID int, ItemDescription blob, PRIMARY KEY (LogID))")
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

def createColorList(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS  ColorList (ColorListID int NOT NULL, ColorName varchar(255), PRIMARY KEY (ColorListID))")
    connection.commit()
    print("ColorList table created.")

def createProductColors(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS ProductColors (ProductColorID int NOT NULL, ColorListID int, ProductID int, PRIMARY KEY(ProductColorID))")
    connection.commit()
    print("ProductColors table created.")

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
    cursor.execute("ALTER TABLE ProductColors ADD FOREIGN KEY (ProductID) REFERENCES Products (ProductID);")
    cursor.execute("ALTER TABLE ProductColors ADD FOREIGN KEY (ColorListID) REFERENCES ColorList (ColorListID);")
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
        SELECT p.productID AS productId, p.productName AS productName, p.itemDescription AS itemDescription, p.price AS price, i.currentStockLevel AS currentStockLevel
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

def insertOrUpdateProducts(connection, cursor):
    # Define product details as a list of tuples
    product_details = [
        (101, 'Bubba 40oz Water Bottle', 'Leakproof lid, cold for 12 hours, vacuum-insulated.', 30.99),
        (102, 'Bubba Hero Mug', 'Hot up to 6 hours or cold up to 24, leak-proof.', 25.99),
        (103, 'Bubba Radiant Water Bottle 32 oz.', 'Leakproof, vacuum-insulated stainless steel, 32 oz.', 26.99),
        (104, 'Bubba Flo Kids Water Bottle 16 oz.', 'Leak-proof lid, high-flow chug lid, 16 oz.', 11.99),
        (105, 'Bubba 32 oz. Water Bottle, Licorice', 'Leakproof, cold for 12 hours, vacuum-insulated, 32 oz.', 26.99),
        (201, 'GoFit Double Thick Yoga Mat', 'Excellent nonslip surface ideal for yoga practice.', 39.99),
        (202, 'GoFit Yoga Mat', 'Provides comfort and protection for Yoga poses.', 24.99),
        (203, 'GoFit Pattern Yoga Mat', 'Non-slip surface, includes yoga pose wall chart.', 21.49),
        (204, 'GoFit Summit Yoga Mat', 'Professional grade mat, extra-cushioned surface.', 69.99),
        (205, 'GoFit Yoga Kit', 'Everything needed for a complete Yoga workout.', 25.50),
        (206, 'GoFit Deluxe Pilates Foam Mat', 'Professional grade, soft, durable design.', 27.99),
    ]

    for product_id, name, description, price in product_details:
        # Check if the product exists
        cursor.execute("SELECT COUNT(*) FROM Products WHERE ProductID = %s", (product_id,))
        if cursor.fetchone()[0] == 0:
            # Product does not exist, so insert
            cursor.execute(
                "INSERT INTO Products (ProductID, ProductName, ItemDescription, Price) VALUES (%s, %s, %s, %s)",
                (product_id, name, description, price)
            )
        else:
            # Product exists, so update
            cursor.execute(
                "UPDATE Products SET ProductName=%s, ItemDescription=%s, Price=%s WHERE ProductID=%s",
                (name, description, price, product_id)
            )
    connection.commit()
    print("Products inserted/updated successfully.")



def insertColorList(connection, cursor):
    insertIntoColorList = """
    INSERT INTO ColorList (ColorListID, ColorName)
    VALUES 
        (1, 'Cobalt'),
        (2, 'Licorice'),
        (3, 'Black'),
        (4, 'Blue'),
        (5, 'Green'),
        (6, 'Purple'),
        (7, 'Gray'),
        (8, 'Crystyle Ice')
    ON DUPLICATE KEY UPDATE 
        ColorName = VALUES(ColorName);
    """
    cursor.execute(insertIntoColorList)
    connection.commit()
    print("Color List filled.")

def insertProductColors(connection, cursor):
    insertIntoProductColors = """
    INSERT INTO ProductColors (ProductColorID, ColorListID, ProductID)
    VALUES 
        (1, 1, 101),
        (2, 2, 101),
        (3, 3, 102),
        (4, 8, 104),
        (5, 2, 105),
        (6, 6, 201),
        (7, 7, 202),
        (8, 5, 203),
        (9, 6, 203),
        (10, 6, 204),
        (11, 4, 205),
        (12, 4, 206)
    ON DUPLICATE KEY UPDATE 
        ColorListID = VALUES(ColorListID),
        ProductID = VALUES(ProductID);
    """
    cursor.execute(insertIntoProductColors)
    connection.commit()
    print("Product colors linked.")


# This will insert all users into the database. This will use all employees listed on the South Balance website. All other data is dummy information.
# UserRoleID is omitted.
def insertUsers(connection, cursor):
    checkIfExists = """
            SELECT COUNT(*) FROM Users WHERE FirstName = %s AND LastName = %s;
        """
    insertIntoUsers = """
        REPLACE INTO Users (FirstName, LastName, UserEmail, PreferredPaymentMethod, isDeleted) 
        VALUES (%s, %s, %s, %s, %s);
    """

    try:
        with open('./DataImport/UserList.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row if your CSV has headers

            for row in reader:
                # Check if the user already exists
                cursor.execute(checkIfExists, (row[1], row[2]))
                exists = cursor.fetchone()[0]
                if exists == 0:  # If the user does not exist, then insert
                    data_tuple = (row[1], row[2], row[3], row[4], row[5])
                    cursor.execute(insertIntoUsers, data_tuple)

        connection.commit()
        print("User Data inserted successfully.")

    except Exception as e:
        print("An error occurred:", e)
        connection.rollback()


def insertDistributionCenter(connection, cursor):
    insert_query = """
            REPLACE INTO DistributionCenter (DODAddressCode, FacilityNo, SiteName, SitePhone, ShippingAddress, ShippingAddress2, ShippingAddress3, ShippingAddress4, ShippingCity, ShippingState, ShippingZip) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

    try:
        with open('./DataImport/AAFES_DISTRIBUTION_CENTERS.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row if your CSV has headers

            for row in reader:
                # FacilityNoLong will not work for some reason. Omitting for now.
                data_tuple = (row[0], row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
                cursor.execute(insert_query, data_tuple)

        connection.commit()
        print("Distribution Center Data inserted successfully.")

    except Exception as e:
        print("An error occurred:", e)
        connection.rollback()

def createDatabase(connection, cursor):
    createNewDatabase = """
        DROP TABLE IF EXISTS aafesorder;
        CREATE DATABASE aafesorder;
    """
    cursor.execute(createNewDatabase)
    connection.commit()
    print("Database created.")

def updateInventoryQuantity(connection, cursor):
    insert_query = """
                REPLACE INTO Inventory (InventoryID, ProductID, CurrentStockLevel) 
                VALUES (%s, %s, %s);
                """

    try:
        with open('./DataImport/INVENTORYLEVELS.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row if your CSV has headers

            for row in reader:
                data_tuple = (row[0], row[1], row[2])
                cursor.execute(insert_query, data_tuple)

        connection.commit()
        print("Inventory levels updated successfully.")

    except Exception as e:
        print("An error occurred:", e)
        connection.rollback()


def updateAuthenticationList(connection, cursor):
    insert_query = """
                REPLACE INTO Authentication (UserID, HashedPassword) 
                VALUES (%s, %s);
                """

    try:
        with open('./DataImport/AUTHENTICATIONLIST.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row if your CSV has headers

            for row in reader:
                data_tuple = (row[0], row[1])
                cursor.execute(insert_query, data_tuple)

        connection.commit()
        print("Authentication updated successfully.")

    except Exception as e:
        print("An error occurred:", e)
        connection.rollback()

def insertUserRole(connection, cursor):
    insert_query = """
                REPLACE INTO UserRole (UserRoleID, RoleDescription) 
                VALUES (%s, %s);
                """

    try:
        with open('./DataImport/UserRole.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row if your CSV has headers

            for row in reader:
                data_tuple = (row[0], row[1])
                cursor.execute(insert_query, data_tuple)

        connection.commit()
        print("User Role List updated successfully.")

    except Exception as e:
        print("An error occurred:", e)
        connection.rollback()


def checkItemQuantity(connection, cursor, product_id):
    try:
        check_query = """
        SELECT CurrentStockLevel FROM Inventory WHERE ProductID = %s;
        """
        cursor.execute(check_query, (product_id,))
        itemQty = cursor.fetchone()[0]
        print("Quantity of item with ProductID", product_id, "is:", itemQty)
        return itemQty
    except Exception as e:
        print("An error occurred:", str(e))
        return None

def reduceInventoryQuantity(connection, cursor, product_id, itemQty):
    try:
        update_query = """
        UPDATE Inventory 
        SET CurrentStockLevel = CurrentStockLevel - %s
        WHERE ProductID = %s;
        """
        cursor.execute(update_query, (itemQty, product_id))
        connection.commit()

        # Fetching the updated quantity to confirm and print
        cursor.execute("SELECT CurrentStockLevel FROM Inventory WHERE ProductID = %s;", (product_id,))
        updated_qty = cursor.fetchone()[0]  # Assuming fetchone() returns a tuple
        print(f"The updated quantity of item with ProductID {product_id} is: {updated_qty}")

    except Exception as e:
        print("An error occurred:", str(e))
        return None


def updateInventoryAfterPurchase(self, user_id):
    # I do not know why this is not working. I will come back to this after I take a nap and cry a lot.

    try:
        for row in self.cart_manager.get_cart_contents():
            self.items = {}
            productid = self.items[product_id]
            print("Quantity of item with ProductID", productid, "is:")
            print("Cart contents after adding items:", self.cart_manager.get_cart_contents())
        #     reduceInventoryQuantity(connection, cursor, product_id, itemQty)
        # connection.commit()  # Commit the changes after all updates are done
    except Exception as e:
        connection.rollback()  # Rollback if any exception occurs
        print(f"Inventory correction error: {e}")
        return None
    finally:
        cursor.close()  # Ensure the cursor is closed after operation

def activityLogging(connection, cursor):
    try:
        update_query = """
        INSERT INTO auditLog (UserID, ActivityType, ActivityTimestamp, AffectedRecordID, ItemDescription) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(update_query)
        connection.commit()
    except Exception as e:
        print("An error occurred:", str(e))
        return None


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

    # Create database
    # createDatabase(connection, cursor)

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
    createColorList(connection, cursor)
    createProductColors(connection, cursor)
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

    # Insert users into DB
    insertUsers(connection, cursor)

    # Inserting products into DB and link colors
    insertOrUpdateProducts(connection, cursor)
    insertColorList(connection, cursor)
    insertProductColors(connection, cursor)

    # Insert warehouse DB list from CSV
    insertDistributionCenter(connection, cursor)

    # Update Inventory levels
    updateInventoryQuantity(connection, cursor)

    # Update Authentication table
    # updateAuthenticationList(connection, cursor) #Temp disable for testing purposes

    # Update User Role List
    insertUserRole(connection, cursor)

    app = App()
    app.mainloop()

    # Closing connection when done
    if connection:
        connection.close()
