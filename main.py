import tkinter as tk

from data_access.text_file_storage import TextFileStorage
from data_access.customer_data_access import CustomerDataAccess
from data_access.offering_data_access import OfferingDataAccess
from data_access.appointment_data_access import AppointmentDataAccess

from services.customer_service import CustomerService
from services.offering_service import OfferingService
from services.appointment_service import AppointmentService

from controllers.customer_controller import CustomerController
from controllers.appointment_controller import AppointmentController
from controllers.offering_controller import OfferingController

from views.main_view import MainView


def main():
    # Data access
    storage = TextFileStorage()

    customer_data_access = CustomerDataAccess(storage)
    offering_data_access = OfferingDataAccess(storage)
    appointment_data_access = AppointmentDataAccess(storage)

    # Services
    customer_service = CustomerService(customer_data_access)
    offering_service = OfferingService(offering_data_access)

    appointment_service = AppointmentService(
        appointment_data_access,
        customer_data_access,
        offering_data_access
    )

    # Controllers
    customer_controller = CustomerController(customer_service)

    appointment_controller = AppointmentController(
        appointment_service
    )

    offering_controller = OfferingController(offering_service)

    # View
    root = tk.Tk()

    MainView(
        root,
        customer_controller,
        appointment_controller,
        offering_controller
    )

    root.mainloop()


if __name__ == "__main__":
    main()