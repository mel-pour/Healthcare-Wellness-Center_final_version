import tkinter as tk

from views.appointment_view import AppointmentView
from views.customer_view import CustomerView
from views.offering_view import OfferingView


class MainView:
    def __init__(self, root, customer_controller, appointment_controller, offering_controller):
        self.root = root
        self.__customer_controller = customer_controller
        self.__appointment_controller = appointment_controller
        self.__offering_controller = offering_controller

        self.root.title("Healthcare & Wellness Center")
        self.root.resizable(False, False)
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_window()
        self.root.geometry("600x500")

        frame = tk.Frame(self.root, padx=30, pady=30)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Healthcare & Wellness Center", font=("Arial", 20, "bold")).pack(pady=(20, 15))
        tk.Label(frame, text="Welcome! Please choose an option.", font=("Arial", 12)).pack(pady=(0, 20))

        self.__create_button(frame, "Customer View", self.open_customer_view)
        self.__create_button(frame, "Appointment View", self.open_appointment_view)
        self.__create_button(frame, "Offering Management", self.open_offering_view)

    def open_customer_view(self):
        self.clear_window()
        CustomerView(self.root, self.__customer_controller, self.show_main_menu)

    def open_appointment_view(self):
        self.clear_window()
        AppointmentView(self.root, self.__appointment_controller, self.show_main_menu)

    def open_offering_view(self):
        self.clear_window()
        OfferingView(self.root, self.__offering_controller, self.show_main_menu)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def __create_button(self, frame, text, command):
        tk.Button(frame, text=text, font=("Arial", 12), width=22, height=2, command=command).pack(pady=6)
