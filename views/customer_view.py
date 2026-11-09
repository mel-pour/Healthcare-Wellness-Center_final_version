import tkinter as tk
from tkinter import messagebox, ttk


class CustomerView:
    def __init__(self, root, customer_controller, back_callback):
        self.root = root
        self.__controller = customer_controller
        self.current_customer_id = None

        frame = tk.Frame(root, padx=20, pady=10)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Customer View", font=("Arial", 18, "bold")).pack(pady=(0, 12))

        search_frame = tk.Frame(frame)
        search_frame.pack(fill="x", pady=5)
        tk.Label(search_frame, text="Customer ID:").pack(side="left")
        self.customer_id_entry = tk.Entry(search_frame, width=12)
        self.customer_id_entry.pack(side="left", padx=8)
        tk.Button(search_frame, text="Search", command=self.search_customer).pack(side="left")

        self.info_frame = tk.LabelFrame(frame, text="Customer Information", padx=10, pady=8)
        self.info_frame.pack(fill="x", pady=10)
        self.name_label = self.__create_info_row("Name:")
        self.age_label = self.__create_info_row("Age:")
        self.gender_label = self.__create_info_row("Gender:")
        self.phone_label = self.__create_info_row("Phone:")
        self.balance_label = self.__create_info_row("Balance:")

        button_frame = tk.Frame(frame)
        button_frame.pack(pady=8)
        tk.Button(button_frame, text="Create Customer", command=self.show_create_form).pack(side="left", padx=5)
        tk.Button(button_frame, text="Add Balance", command=self.show_balance_form).pack(side="left", padx=5)

        tk.Button(frame, text="Back to Main Menu", command=back_callback).pack(pady=8)

    def search_customer(self):
        success, result = self.__controller.get_by_id(self.customer_id_entry.get())

        if success:
            self.current_customer_id = result.customer_id
            self.name_label.config(text=result.name)
            self.age_label.config(text=result.age)
            self.gender_label.config(text=result.gender)
            self.phone_label.config(text=result.phone_number)
            self.balance_label.config(text=result.balance)
        else:
            self.current_customer_id = None
            for label in (self.name_label, self.age_label, self.gender_label, self.phone_label, self.balance_label):
                label.config(text="-")
            messagebox.showerror("Customer Search Error", result, parent=self.root)

    def show_create_form(self):
        form = self.__create_form("Create Customer", "400x430")

        customer_id = self.__create_form_entry(form, "Customer ID:", 0)
        name = self.__create_form_entry(form, "Name:", 1)
        social_id = self.__create_form_entry(form, "Social ID:", 2)
        age = self.__create_form_entry(form, "Age:", 3)
        tk.Label(form, text="Gender:", width=16, anchor="w").grid(row=4, column=0, padx=12, pady=8)
        gender = ttk.Combobox(form, values=("Male", "Female"), state="readonly", width=22)
        gender.current(0)
        gender.grid(row=4, column=1, padx=12, pady=8)
        phone_number = self.__create_form_entry(form, "Phone Number:", 5)
        balance = self.__create_form_entry(form, "Initial Balance:", 6)
        balance.insert(0, "0.00")

        def save_click():
            success, message = self.__controller.save(customer_id.get(), name.get(), social_id.get(), age.get(),
                                                      gender.get(), phone_number.get(), balance.get())
            if success:
                messagebox.showinfo("Customer Save", message, parent=form)
                self.customer_id_entry.delete(0, tk.END)
                self.customer_id_entry.insert(0, customer_id.get())
                form.destroy()
                self.search_customer()
            else:
                messagebox.showerror("Customer Save Error", message, parent=form)

        tk.Button(form, text="Save Customer", width=18, command=save_click).grid(row=7, column=0, columnspan=2, pady=18)

    def show_balance_form(self):
        # The controller checks that a customer has been found first.
        success, result = self.__controller.get_by_id(self.current_customer_id)
        if not success:
            messagebox.showerror("Add Balance Error", result, parent=self.root)
            return

        form = self.__create_form("Add Balance", "320x180")

        tk.Label(form, text=f"Customer ID: {self.current_customer_id}", font=("Arial", 11, "bold")).pack(pady=(15, 10))
        tk.Label(form, text="Amount to add:").pack()
        amount = tk.Entry(form, width=20)
        amount.pack(pady=5)
        amount.focus_set()

        def save_click():
            success, message = self.__controller.add_balance(self.current_customer_id, amount.get())
            if success:
                self.search_customer()
                messagebox.showinfo("Add Balance", f"{message}\nNew balance: {self.balance_label['text']}", parent=form)
                form.destroy()
            else:
                messagebox.showerror("Add Balance Error", message, parent=form)

        tk.Button(form, text="Add Balance", width=15, command=save_click).pack(pady=10)

    def __create_info_row(self, text):
        row = tk.Frame(self.info_frame)
        row.pack(fill="x", pady=2)
        tk.Label(row, text=text, width=15, anchor="w", font=("Arial", 10, "bold")).pack(side="left")
        value_label = tk.Label(row, text="-", anchor="w")
        value_label.pack(side="left")
        return value_label

    def __create_form(self, title, size):
        form = tk.Toplevel(self.root)
        form.title(title)
        form.geometry(size)
        form.resizable(False, False)
        form.transient(self.root)
        form.grab_set()
        return form

    def __create_form_entry(self, form, text, row):
        tk.Label(form, text=text, width=16, anchor="w").grid(row=row, column=0, padx=12, pady=8)
        entry = tk.Entry(form, width=25)
        entry.grid(row=row, column=1, padx=12, pady=8)
        return entry
