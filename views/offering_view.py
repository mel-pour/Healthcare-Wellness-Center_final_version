import tkinter as tk
from tkinter import messagebox, ttk


class OfferingView:
    def __init__(self, root, offering_controller, back_callback):
        self.root = root
        self.__controller = offering_controller

        self.root.geometry("600x550")

        self.frame = tk.Frame(root, padx=20, pady=15)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Offering Management", font=("Arial", 18, "bold")).pack(pady=(0, 15))

        self.id_entry = self.__create_entry("Offering ID:")
        self.name_entry = self.__create_entry("Name:")

        row = tk.Frame(self.frame)
        row.pack(fill="x", pady=4)
        tk.Label(row, text="Type:", width=35, anchor="w").pack(side="left")
        self.type_combo = ttk.Combobox(row, values=("service", "facility"), state="readonly", width=22)
        self.type_combo.current(0)
        self.type_combo.pack(side="left")

        self.price_entry = self.__create_entry("Price:")
        self.duration_entry = self.__create_entry("Duration (minutes, optional for facilities):")

        tk.Button(self.frame, text="Create Offering", command=self.save_click).pack(pady=15)

        tk.Label(self.frame, text="Existing Offerings", font=("Arial", 12, "bold")).pack(anchor="w")
        self.offerings_list = tk.Listbox(self.frame, height=8, width=65)
        self.offerings_list.pack(fill="both", expand=True, pady=5)

        tk.Button(self.frame, text="Back to Main Menu", command=back_callback).pack(pady=10)

        self.show_offerings()

    def save_click(self):
        success, message = self.__controller.save(self.id_entry.get(), self.name_entry.get(), self.type_combo.get(),
                                                  self.price_entry.get(), self.duration_entry.get())
        if success:
            messagebox.showinfo("Offering Save", message, parent=self.root)
            self.reset_form()
            self.show_offerings()
        else:
            messagebox.showerror("Offering Save Error", message, parent=self.root)

    def show_offerings(self):
        success, result = self.__controller.get_all()

        if not success:
            messagebox.showerror("Offering Error", result, parent=self.root)
            return

        self.offerings_list.delete(0, tk.END)
        for offering in result:
            duration = "N/A" if offering.duration is None else f"{offering.duration} min"
            self.offerings_list.insert(tk.END, f"ID: {offering.offering_id} | {offering.name} | "
                                               f"Type: {offering.offering_type} | Price: ${offering.price} | "
                                               f"Duration: {duration}")

    def reset_form(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.type_combo.current(0)
        self.price_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def __create_entry(self, text):
        row = tk.Frame(self.frame)
        row.pack(fill="x", pady=4)
        tk.Label(row, text=text, width=35, anchor="w").pack(side="left")
        entry = tk.Entry(row, width=25)
        entry.pack(side="left")
        return entry
