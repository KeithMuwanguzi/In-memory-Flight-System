# Abstract class for Transport
from abc import ABC, abstractmethod
import re

# Abstraction: Creating a Transport class (Base Class)
class Transport(ABC):
    def __init__(self, airline, flight_number, departure, destination, date, time, seats):
        self.airline = airline
        self.flight_number = flight_number
        self.departure = departure
        self.destination = destination
        self.date = date
        self.time = time
        self._seats = seats  # Encapsulation: Private attribute for seats

    @abstractmethod
    def get_details(self):
        pass

    # Encapsulation: Getter and Setter for seats
    @property
    def seats(self):
        return self._seats

    @seats.setter
    def seats(self, value):
        if value >= 0:
            self._seats = value
        else:
            print("Seats cannot be negative.")

    def __str__(self):
        return (f"{self.flight_number} from {self.departure} to {self.destination} on {self.date} "
                f"at {self.time} - Seats available: {self.seats}")

# Inheritance: Flight class inherits from Transport
class Flight(Transport):
    def __init__(self, airline, flight_number, departure, destination, date, time, seats, gate, airport):
        super().__init__(airline, flight_number, departure, destination, date, time, seats)
        self.gate = gate
        self.airport = airport

    # Polymorphism: Overriding get_details for Flights
    def get_details(self):
        return (f"Flight {self.flight_number} - {self.departure} to {self.destination} on {self.date} "
                f"at {self.time} - Seats available: {self.seats} - Gate: {self.gate}, {self.airport}")


# Another Transport subclass - Bus
class Bus(Transport):
    def __init__(self, bus_number, departure, destination, date, time, seats, route):
        super().__init__("Air Uganda", bus_number, departure, destination, date, time, seats)
        self.route = route

    # Polymorphism: Overriding get_details for Bus
    def get_details(self):
        return (f"Bus {self.flight_number} - {self.departure} to {self.destination} on {self.date} "
                f"at {self.time} - Seats available: {self.seats} - Route: {self.route}")


# Person class (Base Class for User and Passenger)
class Person:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self._password = password  # Encapsulation: private attribute

    # Encapsulation: Getter and Setter for password
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if len(value) >= 8:
            self._password = value
        else:
            print("Password must be at least 8 characters.")

    def __str__(self):
        return f"Name: {self.name}, Email: {self.email}"

# User class inherits from Person
class User(Person):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)
        self.bookings = []

    def search_flights(self, transports, departure, destination):
        return [t for t in transports if t.departure == departure and t.destination == destination]

    def book_flight(self, transport, passenger_name):
        if transport.seats > 0:
            transport.seats -= 1
            booking = Booking(transport, passenger_name)
            self.bookings.append(booking)
            print(f"Booking successful: {booking.booking_id}")
        else:
            print("No seats available.")

    def view_bookings(self):
        if not self.bookings:
            print("No bookings found.")
            return
        for booking in self.bookings:
            print(f"Booking ID: {booking.booking_id}, Flight: {booking.transport}, Passenger: {booking.passenger_name}")

# Booking class
class Booking:
    def __init__(self, transport, passenger_name):
        self.transport = transport
        self.passenger_name = passenger_name
        self.booking_id = f"BK-{hash(self)}"


def is_valid_email(email):
    # Simple regex for validating an email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def main():
    # Print the welcome message first
    print("WELCOME! AND THANK YOU FOR CHOOSING AIR UGANDA.\n")

    # Define transport (flights and buses)
    transports = [
        Flight("Air Uganda", "UG001", "Kampala", "Nairobi", "2024-11-28", "6:00am", 100, "Gate A", "Entebbe International Airport"),
        Flight("Air Uganda", "UG002", "Kampala", "London", "2024-11-28", "8:00am", 50, "Gate A", "Entebbe International Airport"),
        Bus("BUS001", "Kampala", "Jinja", "2024-11-29", "10:00am", 60, "Kampala-Jinja Road"),
        Flight("Air Uganda", "UG003", "Kampala", "Johannesburg", "2024-11-28", "12:00pm", 70, "Gate B", "Entebbe International Airport"),
    ]

    # Get user information
    while True:
        user_name = input("Enter your name: ")
        if user_name != '' and len(user_name) >= 6:
            break
        else:
            print("Enter a valid username")
    
    while True:
        user_email = input("Enter your email address: ")
        if is_valid_email(user_email):
            break
        else:
            print("Invalid email format. Please try again.")

    while True:
        user_password = input("Enter your password: ")
        if len(user_password) >= 8:
            break
        else:
            print("Password must be at least 8 characters. Please try again.")

    user = User(user_name, user_email, user_password)

    while True:
        # Show available transports (polymorphism in action)
        print("\nAvailable Transports:")
        for transport in transports:
            print(transport.get_details())

        departure = input("\nEnter departure city: ")
        destination = input("Enter destination city: ")

        # Search for matching transports
        available_transports = user.search_flights(transports, departure, destination)

        if available_transports:
            print("\nAvailable Transports:")
            for transport in available_transports:
                print(transport.get_details())

            transport_choice = input("Select a transport number to book: ")
            selected_transport = next((t for t in available_transports if t.flight_number == transport_choice), None)

            if selected_transport:
                passenger_name = input("Enter passenger name: ")
                user.book_flight(selected_transport, passenger_name)
            else:
                print("Invalid transport selection.")
        else:
            print("No available transports for the selected route.")

        # Ask if the user wants to book another transport
        more_booking = input("Do you want to book another transport? (yes/no): ").strip().lower()
        if more_booking != 'yes':
            break

    # View all bookings
    user.view_bookings()

if __name__ == "__main__":
    main()