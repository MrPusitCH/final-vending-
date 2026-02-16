import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, PhotoImage, Frame

class VendingMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("Vending Machine")
        self.root.geometry("1400x1100")
        self.root.config(bg="#cfe2f3")

        self.balance = 0
        self.selected_drink = None
        self.selected_type = "Hot"
        self.purchase_history = []  # List to store purchase history
        self.total_revenue = 0  # Variable to store total revenue
        self.customer_data = {}  # Dictionary to store customer phone, points, and coupons
        self.current_phone = None  # Variable to store the current phone number
        self.coupon_used = False  # Variable to track coupon status

        self.points_per_purchase = 1  # Points earned per purchase
        self.points_needed_for_coupon = 4  # Points needed for a free coupon

        # Load logo image
        self.logo_image = tk.PhotoImage(file="LOGO.png")  # Replace with your logo path
        self.logo_label = tk.Label(self.root, image=self.logo_image, bg="#cfe2f3")
        self.logo_label.pack(pady=20)

        self.drink_images = {
            "Iced Coffee": tk.PhotoImage(file="Drinks/IcedCoffee.png"),
            "Matcha Latte": tk.PhotoImage(file="Drinks/matcha_latte.png"),
            "Thai Tea": tk.PhotoImage(file="Drinks/ThaiTea.png"),
            "Espresso": tk.PhotoImage(file="Drinks/Espresso.png"),
            "Cappuccino": tk.PhotoImage(file="Drinks/Cappuccino.png"),
            "Latte": tk.PhotoImage(file="Drinks/Latte.png"),
            "Green Tea": tk.PhotoImage(file="Drinks/GreenTea.png"),
            "Black Tea": tk.PhotoImage(file="Drinks/BlackTea.png"),
            "Herbal Tea": tk.PhotoImage(file="Drinks/HerbalTea.png"),
            "Chocolate Milk": tk.PhotoImage(file="Drinks/ChocolateMilk.png"),
            "Strawberry Milk": tk.PhotoImage(file="Drinks/StrawberryMilk.png"),
            "Chocolate Shake": tk.PhotoImage(file="Drinks/ChocolateShake.png"),
            "Caramel Latte": tk.PhotoImage(file="Drinks/CaramelLatte.png"),
            "Vanilla Protein Shake": tk.PhotoImage(file="Drinks/VanillaProteinShake.png"),
            "Chocolate Protein Shake": tk.PhotoImage(file="Drinks/ChocolateProteinShake.png"),
            "Cola": tk.PhotoImage(file="Drinks/Cola.png"),
            "Lemonade": tk.PhotoImage(file="Drinks/Lemonade.png"),
            "Orange Soda": tk.PhotoImage(file="Drinks/OrangeSoda.png"),
            "Water": tk.PhotoImage(file="Drinks/Water.png"),
            "Juice": tk.PhotoImage(file="Drinks/Juice.png")
        }

        # Drink categories and their items
        self.drinks = {
            "Recommended Drinks": {
                "Iced Coffee": 30,
                "Matcha Latte": 35,
                "Thai Tea": 25
            },
            "Coffee": {
                "Espresso": 20,
                "Cappuccino": 40,
                "Latte": 35
            },
            "Tea": {
                "Green Tea": 25,
                "Black Tea": 20,
                "Herbal Tea": 30
            },
            "Milk": {
                "Chocolate Milk": 25,
                "Strawberry Milk": 30
            },
            "Cocoa and Caramel": {
                "Chocolate Shake": 35,
                "Caramel Latte": 40
            },
            "Protein Shakes": {
                "Vanilla Protein Shake": 50,
                "Chocolate Protein Shake": 55
            },
            "Soda": {
                "Cola": 25,
                "Lemonade": 20,
                "Orange Soda": 20
            },
            "Others": {
                "Water": 10,
                "Juice": 25
            }
        }
        
        self.create_widgets()

    def create_widgets(self):
        # Display Screen
        display_frame = tk.Frame(self.root, bg="#cfe2f3", bd=5)
        display_frame.pack(pady=20)
        self.display_label = tk.Label(display_frame, text="Welcome! Please select a drink", font=("Arial", 18), bg="#fff", fg="#000")
        self.display_label.pack(fill=tk.BOTH, expand=True)

        # Menu Categories
        self.category_var = tk.StringVar(value="Recommended Drinks")
        category_frame = tk.Frame(self.root, bg="#cfe2f3")
        category_frame.pack(pady=10)

        categories = ["Recommended Drinks", "Coffee", "Tea", "Milk", "Cocoa and Caramel", "Protein Shakes", "Soda", "Others"]
        for category in categories:
            category_button = tk.Radiobutton(category_frame, text=category, variable=self.category_var, value=category, font=("Arial", 12), bg="#cfe2f3", command=self.update_drink_buttons)
            category_button.pack(side=tk.LEFT, padx=10)

        # Buttons for selecting drinks
        self.button_frame = tk.Frame(self.root, bg="#cfe2f3")
        self.button_frame.pack(pady=20)

        self.update_drink_buttons()

        # Drink Type Selection Bar
        type_frame = tk.Frame(self.root, bg="#cfe2f3")
        type_frame.pack(pady=10)

        type_options = ["Hot", "Cold", "Blended"]
        for option in type_options:
            type_button = tk.Button(type_frame, text=option, font=("Arial", 14), bg="#f0ad4e", command=lambda t=option: self.select_drink_type(t))
            type_button.pack(side=tk.LEFT, padx=10)

        # Insert Money Section
        money_frame = tk.Frame(self.root, bg="#cfe2f3")
        money_frame.pack(pady=10)
        tk.Label(money_frame, text="Insert Money:", font=("Arial", 18), bg="#cfe2f3").grid(row=0, column=0, padx=10)

        self.money_entry = tk.Entry(money_frame, font=("Arial", 18), width=10)
        self.money_entry.grid(row=0, column=1, padx=10)

        insert_button = tk.Button(money_frame, text="Insert", font=("Arial", 16), bg="#28a745", fg="white", command=self.insert_money)
        insert_button.grid(row=0, column=2, padx=10)

        self.balance_label = tk.Label(money_frame, text=f"Balance: {self.balance:.2f} THB", font=("Arial", 18), bg="#cfe2f3", fg="#000")
        self.balance_label.grid(row=0, column=3, padx=10)

        # Purchase Button and Check Points Button
        action_frame = tk.Frame(self.root, bg="#cfe2f3")
        action_frame.pack(pady=11)

        purchase_button = tk.Button(action_frame, text="Purchase", font=("Arial", 20), bg="#ff5733", fg="white", width=10, command=self.purchase_drink)
        purchase_button.pack(side=tk.LEFT, padx=10)

        self.points_button = tk.Button(action_frame, text="Check Points", font=("Arial", 16), bg="#ffc107", fg="black", width=12, command=self.check_points)
        self.points_button.pack(side=tk.LEFT, padx=10)

        # Use Coupon Button
        self.coupon_button = tk.Button(action_frame, text="Use Coupon (50% off)", font=("Arial", 14), bg="#007bff", fg="white", width=19, command=self.use_coupon)
        self.coupon_button.pack(side=tk.LEFT, padx=10)

        # Exit Button
        exit_button = tk.Button(self.root, text="Exit", font=("Arial", 12), bg="#dc3545", fg="white", command=self.root.quit)
        exit_button.place(x=1300, y=20)

        # Admin Button
        admin_button = tk.Button(self.root, text="Admin", font=("Arial", 12), bg="#007bff", fg="white", command=self.open_admin_mode)
        admin_button.place(x=1200, y=20)

    def update_drink_buttons(self):
        """Update drink buttons based on selected category."""
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        selected_category = self.category_var.get()
        drinks = self.drinks[selected_category]

        row = 0
        column = 0

        for drink in drinks.keys():
            # Update drink name with selected type
            drink_name = f"{drink} ({self.selected_type})"
            if drink in self.drink_images:  # Check if the image exists
                drink_button = tk.Button(self.button_frame, image=self.drink_images[drink], compound=tk.TOP, text=drink_name, font=("Arial", 12), command=lambda d=drink: self.select_drink(d))
                drink_button.grid(row=row, column=column, padx=10, pady=10)
            else:
                drink_button = tk.Button(self.button_frame, text=drink_name, font=("Arial", 12), command=lambda d=drink: self.select_drink(d))
                drink_button.grid(row=row, column=column, padx=10, pady=10)

            column += 1
            if column > 2:  # Move to next row after 3 buttons
                column = 0
                row += 1

    def select_drink_type(self, drink_type):
        """Select the drink type (Hot, Cold, Blended)."""
        self.selected_type = drink_type
        self.update_drink_buttons()

    def select_drink(self, drink):
        """Select a drink."""
        self.selected_drink = drink
        price = self.drinks[self.category_var.get()][drink]
        
        # Apply discount if coupon is used
        if self.coupon_used:
            price *= 0.5
        
        self.display_label.config(text=f"Selected: {drink} ({self.selected_type}) | Price: {price:.2f} THB")

    def insert_money(self):
        """Insert money into the vending machine."""
        try:
            amount = float(self.money_entry.get())
            if amount <= 0:
                raise ValueError("Please insert a valid amount.")
            self.balance += amount
            self.balance_label.config(text=f"Balance: {self.balance:.2f} THB")
            self.money_entry.delete(0, tk.END)
            messagebox.showinfo("Money Inserted", f"Inserted: {amount:.2f} THB")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def purchase_drink(self):
        """Purchase the selected drink."""
        if not self.selected_drink:
            messagebox.showwarning("No Selection", "Please select a drink.")
            return

        # Get the price of the selected drink
        price = self.drinks[self.category_var.get()][self.selected_drink]

        # Check if coupon is used
        if self.coupon_used:
            price *= 0.5  # Apply 50% discount

        if self.balance < price:
            messagebox.showwarning("Insufficient Balance", f"Please insert at least {price:.2f} THB.")
            return

        # Prompt for phone number every time
        self.current_phone = self.get_customer_phone()

        if self.current_phone:
            # Subtract the price from balance and update revenue
            self.balance -= price
            self.total_revenue += price
            self.purchase_history.append((self.selected_drink, price))  # Add purchase to history
            self.update_customer_data()  # Update customer points

            # Show success messages
            messagebox.showinfo("Purchase Successful", f"Purchased: {self.selected_drink} | Price: {price:.2f} THB | Remaining Balance: {self.balance:.2f} THB | Earned Points: {self.points_per_purchase}")

            self.balance_label.config(text=f"Balance: {self.balance:.2f} THB")
            
            # Reset the selection after purchase
            self.selected_drink = None
            self.coupon_used = False  # Reset coupon status after purchase

            # Update the display label after the purchase
            self.display_label.config(text="Welcome! Please select a drink")

    def update_customer_data(self):
        """Update customer points based on purchases."""
        if self.current_phone:
            if self.current_phone not in self.customer_data:
                self.customer_data[self.current_phone] = {"points": 0, "coupons": 0}
            
            # Update points and check for coupons
            self.customer_data[self.current_phone]["points"] += self.points_per_purchase
            
            if self.customer_data[self.current_phone]["points"] >= self.points_needed_for_coupon:
                self.customer_data[self.current_phone]["coupons"] += 1
                messagebox.showinfo("Coupon Earned", "Congratulations! You earned a coupon for a 50% off")
                self.customer_data[self.current_phone]["points"] -= self.points_needed_for_coupon

    def get_customer_phone(self):
        """Prompt user for phone number and return it."""
        phone = simpledialog.askstring("Customer Phone", "Please enter your phone number:")
        return phone

    def check_points(self):
        """Check customer points."""
        if self.current_phone and self.current_phone in self.customer_data:
            points = self.customer_data[self.current_phone]["points"]
            coupons = self.customer_data[self.current_phone]["coupons"]
            messagebox.showinfo("Customer Points", f"Phone: {self.current_phone}\nPoints: {points}\nCoupons: {coupons}")
        else:
            messagebox.showinfo("No Data", "No data found for this phone number.")

    def use_coupon(self):
        """Use a coupon to get a discount."""
        if self.current_phone in self.customer_data and self.customer_data[self.current_phone]["coupons"] > 0:
            self.coupon_used = True  # Set coupon status
            self.customer_data[self.current_phone]["coupons"] -= 1  # Deduct one coupon
            messagebox.showinfo("Coupon Used", "Coupon applied! You will get 50% off on your next drink purchase.")
            
            # Update the display if a drink is selected
            if self.selected_drink:
                price = self.drinks[self.category_var.get()][self.selected_drink] * 0.5
                self.display_label.config(text=f"Selected: {self.selected_drink} ({self.selected_type}) | Price: {price:.2f} THB (50% off)")
        else:
            messagebox.showwarning("No Coupon", "You do not have any coupons to use.")

    def open_admin_mode(self):
        """Open admin mode for reporting."""
        admin_window = tk.Toplevel(self.root)
        admin_window.title("Admin Mode")
        admin_window.geometry("600x400")
        admin_window.config(bg="#343a40")

        # Add title label
        title_label = tk.Label(admin_window, text="Admin Dashboard", font=("Arial", 24), bg="#343a40", fg="white")
        title_label.pack(pady=10)

        # Frame for revenue and sales count
        revenue_frame = tk.Frame(admin_window, bg="#343a40", bd=2, relief=tk.RIDGE)
        revenue_frame.pack(pady=10)

        total_sales = len(self.purchase_history)  # Count of total sales
        total_revenue = sum(price for _, price in self.purchase_history)  # Total revenue calculation

        total_sales_label = tk.Label(revenue_frame, text=f"Total Sales Count: {total_sales}", font=("Arial", 16), bg="#343a40", fg="white")
        total_sales_label.pack(pady=5)

        total_revenue_label = tk.Label(revenue_frame, text=f"Total Revenue: {total_revenue:.2f} THB", font=("Arial", 16), bg="#343a40", fg="white")
        total_revenue_label.pack(pady=5)

        report_text = scrolledtext.ScrolledText(admin_window, wrap=tk.WORD, width=70, height=20, font=("Arial", 12), bg="#ffffff")
        report_text.pack(pady=20)

        report_text.insert(tk.END, "Purchase History:\n")
        
        for drink, price in self.purchase_history:
            report_text.insert(tk.END, f"{drink}: {price:.2f} THB\n")

        exit_button = tk.Button(admin_window, text="Exit", command=admin_window.destroy, font=("Arial", 14), bg="#dc3545", fg="white")
        exit_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = VendingMachine(root)
    root.mainloop()