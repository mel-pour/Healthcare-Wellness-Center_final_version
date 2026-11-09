import tkinter as tk
from tkinter import messagebox, ttk


class AppointmentView:
    def __init__(self, root, appointment_controller, back_callback):
        self.root = root
        self.__controller = appointment_controller
        self.offerings = []

        self.root.geometry("750x600")

        self.frame = tk.Frame(root, padx=20, pady=15)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Appointment View", font=("Arial", 18, "bold")).pack(pady=(0, 15))

        row = self.__create_row("Customer ID:")
        self.customer_id_entry = tk.Entry(row, width=20)
        self.customer_id_entry.pack(side="left")
        tk.Button(row, text="View Appointments", command=self.show_appointments).pack(side="left", padx=10)

        self.balance_label = tk.Label(self.frame, text="Customer: -- | ID: -- | Balance: --", font=("Arial", 11, "bold"))
        self.balance_label.pack(anchor="w", pady=5)

        self.appointment_id_entry = tk.Entry(self.__create_row("Appointment ID:"), width=20)
        self.appointment_id_entry.pack(side="left")

        self.offering_combo = ttk.Combobox(self.__create_row("Offering:"), state="readonly", width=40)
        self.offering_combo.pack(side="left")

        self.date_entry = tk.Entry(self.__create_row("Date (YYYY-MM-DD):"), width=20)
        self.date_entry.pack(side="left")

        self.time_entry = tk.Entry(self.__create_row("Start Time (HH:MM):"), width=20)
        self.time_entry.pack(side="left")

        button_frame = tk.Frame(self.frame)
        button_frame.pack(pady=12)
        tk.Button(button_frame, text="Book Appointment", command=self.book_click).pack(side="left", padx=5)
        tk.Button(button_frame, text="Clear", command=self.reset_form).pack(side="left", padx=5)
        tk.Button(button_frame, text="Cancel Appointment", command=self.cancel_click).pack(side="left", padx=5)

        tk.Label(self.frame, text="Customer Appointments", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 5))
        self.results = tk.Text(self.frame, height=10, width=85, state="disabled")
        self.results.pack(fill="both", expand=True)

        tk.Button(self.frame, text="Back to Main Menu", command=back_callback).pack(pady=10)

        self.show_offerings()

    def show_offerings(self):
        success, result = self.__controller.get_offerings()

        if not success:
            messagebox.showerror("Offering Error", result, parent=self.root)
            return

        self.offerings = result
        values = []
        for offering in self.offerings:
            duration = "N/A" if offering.duration is None else f"{offering.duration} min"
            values.append(f"{offering.offering_id} - {offering.name} (${offering.price}, {duration})")

        self.offering_combo["values"] = values
        if values:
            self.offering_combo.current(0)

    def book_click(self):
        # No selection is sent as empty text, and the controller reports it.
        offering_id = ""
        index = self.offering_combo.current()
        if index >= 0:
            offering_id = self.offerings[index].offering_id

        customer_id = self.customer_id_entry.get()
        success, message = self.__controller.book(self.appointment_id_entry.get(), customer_id, offering_id,
                                                  self.date_entry.get(), self.time_entry.get())
        if success:
            messagebox.showinfo("Appointment Booking", message, parent=self.root)
            self.reset_form()
            self.customer_id_entry.insert(0, customer_id)
            self.show_appointments()
        else:
            messagebox.showerror("Appointment Booking Error", message, parent=self.root)

    def cancel_click(self):
        appointment_id = self.appointment_id_entry.get()
        success, result = self.__controller.get_cancellation_details(appointment_id)

        if not success:
            messagebox.showerror("Appointment Cancel Error", result, parent=self.root)
            return

        price, fee, refund = result
        confirmed = messagebox.askyesno("Confirm Cancellation",
                                        f"Appointment ID: {appointment_id}\n"
                                        f"Original price: ${price}\n"
                                        f"Cancellation fee: ${fee}\n"
                                        f"Refund amount: ${refund}\n\n"
                                        "Are you sure you want to cancel this appointment?",
                                        parent=self.root)
        if not confirmed:
            return

        success, message = self.__controller.cancel(appointment_id)
        if success:
            messagebox.showinfo("Appointment Cancel", message, parent=self.root)
            if self.customer_id_entry.get().strip():
                self.show_appointments()
        else:
            messagebox.showerror("Appointment Cancel Error", message, parent=self.root)

    def show_appointments(self):
        customer_id = self.customer_id_entry.get()
        success, result = self.__controller.get_by_customer_id(customer_id)

        if not success:
            messagebox.showerror("Appointment Error", result, parent=self.root)
            return

        self.show_balance(customer_id)

        lines = []
        for appointment in result:
            lines.append(f"Appointment ID: {appointment.appointment_id}\n"
                         f"Offering: {self.get_offering_name(appointment.offering_id)}\n"
                         f"Date: {appointment.appointment_date}\n"
                         f"Time: {appointment.start_time.strftime('%H:%M')}\n"
                         f"Status: {appointment.status}\n"
                         f"Price: ${appointment.price_paid}\n"
                         f"{'-' * 45}")
        if not lines:
            lines.append("No appointments found for this customer.")

        self.show_results("\n".join(lines))

    def show_balance(self, customer_id):
        success, result = self.__controller.get_customer(customer_id)

        if success:
            self.balance_label.config(text=f"Customer: {result.name} | ID: {result.customer_id} | Balance: ${result.balance}")
        else:
            self.balance_label.config(text="Customer: unavailable | ID: -- | Balance: --")

    def get_offering_name(self, offering_id):
        for offering in self.offerings:
            if offering.offering_id == offering_id:
                return offering.name
        return f"Unknown offering (ID: {offering_id})"

    def show_results(self, text):
        self.results.config(state="normal")
        self.results.delete("1.0", tk.END)
        self.results.insert("1.0", text)
        self.results.config(state="disabled")

    def reset_form(self):
        self.appointment_id_entry.delete(0, tk.END)
        self.customer_id_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.offering_combo.set("")
        self.balance_label.config(text="Customer: -- | ID: -- | Balance: --")
        self.show_results("")

    def __create_row(self, text):
        row = tk.Frame(self.frame)
        row.pack(fill="x", pady=5)
        tk.Label(row, text=text, width=18, anchor="w").pack(side="left")
        return row
