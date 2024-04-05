import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime, date
import sqlite3


class ReservationBar:
    def __init__(self, master, it=None):
        self.it = it
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.X, padx=10, pady=5)

        # Title is on TOP
        self.title_label = tk.Label(self.frame, text="Z Hotel Reservation Management System",
                            font=("Courier New", 20, "bold"), fg="#274b6c")
        self.title_label.pack(side=tk.TOP, padx=5, pady=10)

        # Use separate frames to organize the widgets in rows
        self.first_line_frame = tk.Frame(self.frame)
        self.first_line_frame.pack(fill=tk.X)

        self.second_line_frame = tk.Frame(self.frame)
        self.second_line_frame.pack(fill=tk.X)

        self.third_line_frame = tk.Frame(self.frame)
        self.third_line_frame.pack(fill=tk.X)

        # First line
        # Store today's date
        self.reservation_date = datetime.now().strftime("%Y-%m-%d")

        # Date Calender Default Setting
        today_date = date.today()

        # Checkin Date
        self.create_label_with_necessary(self.first_line_frame, "Checkin Date")
        self.checkin_date_entry = DateEntry(self.first_line_frame, date_pattern='yyyy-MM-dd', mindate=today_date)
        self.checkin_date_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # Checkout Date
        self.create_label_with_necessary(self.first_line_frame, "Checkout Date")
        self.checkout_date_entry = DateEntry(self.first_line_frame, date_pattern='yyyy-MM-dd', mindate=today_date)
        self.checkout_date_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # Room Type Options
        self.create_label_with_necessary(self.first_line_frame, "Room Type")
        self.room_type_entry = ttk.Combobox(self.first_line_frame, values=["Twin Room", "Queen Room", "Premium Suit"],
                                            width=15)
        self.room_type_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.room_type_entry.bind('<<ComboboxSelected>>', self.update_room_numbers)

        # Room Number
        self.create_label_with_necessary(self.first_line_frame, "Room Number")
        self.room_number_entry = ttk.Combobox(self.first_line_frame, width=10)
        self.room_number_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # Second line
        # First Name
        self.create_label_with_necessary(self.second_line_frame, "First Name")
        self.first_name_entry = tk.Entry(self.second_line_frame, width=20)
        self.first_name_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # Last Name
        self.create_label_with_necessary(self.second_line_frame, "Last Name")
        self.last_name_entry = tk.Entry(self.second_line_frame, width=20)
        self.last_name_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # Number of Guest
        self.create_label_with_necessary(self.second_line_frame, "Number of Guests")
        self.number_of_guests_entry = ttk.Combobox(self.second_line_frame, values=list(range(1, 6)), width=10)
        self.number_of_guests_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # Email
        self.create_label_with_necessary(self.second_line_frame, "Email")
        self.email_entry = tk.Entry(self.second_line_frame, width=30)
        self.email_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # Third line
        # Phone Number
        self.create_label_with_necessary(self.third_line_frame, "Phone Number")
        validate_phone_number = (master.register(self.validate_phone), '%P')
        self.phone_number_entry = tk.Entry(self.third_line_frame, validate="key", validatecommand=validate_phone_number)
        self.phone_number_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # Payment Method
        self.create_label_with_necessary(self.third_line_frame, "Payment Method")
        self.payment_method_entry = ttk.Combobox(self.third_line_frame, values=["Credit", "Debit", "Cash"], width=10)
        self.payment_method_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # Special Requirements (is not necessary entry)
        special_requirements_label = tk.Label(self.third_line_frame, text="Special Requirements")
        special_requirements_label.pack(side=tk.LEFT)
        self.special_requirements_entry = tk.Entry(self.third_line_frame, width=60)
        self.special_requirements_entry.pack(side=tk.LEFT, padx=10, pady=5)

        # Add Booking Button: Initialize the state to Disabled
        self.add_booking_button = tk.Button(self.third_line_frame, text="Add Booking",
                                            command=self.add_booking_to_database, state=tk.DISABLED)
        self.add_booking_button.pack(side=tk.RIGHT, padx=5)
        Tooltip(self.add_booking_button, "Please fill in all *necessary fields; "
                                         "Phone number should be 10 digits.")

        self.refresh_available_rooms()
        
        # Call update_button_state
        # Combobox and DateEntry widgets use：ComboboxSelected
        self.checkin_date_entry.bind('<<DateEntrySelected>>', self.refresh_available_rooms)
        self.checkout_date_entry.bind('<<DateEntrySelected>>', self.update_button_state)
        self.room_type_entry.bind('<<ComboboxSelected>>', self.update_room_numbers)
        self.room_number_entry.bind('<<ComboboxSelected>>', self.update_button_state)
        self.number_of_guests_entry.bind('<<ComboboxSelected>>', self.update_button_state)
        self.payment_method_entry.bind('<<ComboboxSelected>>', self.update_button_state)

        # Regular entry widget use: KeyRelease
        self.first_name_entry.bind('<KeyRelease>', self.update_button_state)
        self.last_name_entry.bind('<KeyRelease>', self.update_button_state)
        self.email_entry.bind('<KeyRelease>', self.update_button_state)
        self.phone_number_entry.bind('<KeyRelease>', self.update_button_state)
        self.special_requirements_entry.bind('<KeyRelease>', self.update_button_state)


    def update_button_state(self, event=None):
        # Check if all fields are filled
        if (self.checkin_date_entry.get() and self.checkout_date_entry.get() and
                self.room_type_entry.get() and self.room_number_entry.get() and
                self.first_name_entry.get() and self.last_name_entry.get() and
                self.number_of_guests_entry.get() and self.email_entry.get() and
                len(self.phone_number_entry.get()) == 10 and self.payment_method_entry.get()):
            self.add_booking_button['state'] = tk.NORMAL
        else:
            self.add_booking_button['state'] = tk.DISABLED

    def validate_phone(self, input):
        if input == "":
            return True
        # Only accept numeric characters, and its length should be 10
        return input.isdigit() and len(input) <= 10

    def update_room_numbers(self, event=None):
        self.refresh_available_rooms()
        selected_room_type = self.room_type_entry.get()
        available_numbers = self.available_room_types_and_numbers.get(selected_room_type, [])
        self.room_number_entry['values'] = available_numbers
        self.room_number_entry.set('')

    def schedule_room_refresh(self):
        self.frame.after(1000, self.refresh_available_rooms)

    def refresh_available_rooms(self, event=None):
        checkin_date = self.checkin_date_entry.get() if self.checkin_date_entry.get() else datetime.now().strftime('%Y-%m-%d')

        #get all the room types and room numbers from the database
        self.all_room_types_and_numbers = {
            101: "Twin Room", 102: "Queen Room", 103: "Twin Room", 104: "Queen Room",
            105: "Twin Room", 106: "Queen Room", 107: "Twin Room", 108: "Queen Room",
            109: "Twin Room", 201: "Twin Room", 202: "Premium Suit", 203: "Twin Room",
            204: "Queen Room", 205: "Twin Room", 206: "Queen Room", 207: "Twin Room",
            208: "Queen Room", 209: "Premium Suit", 301: "Twin Room", 302: "Premium Suit",
            303: "Twin Room", 304: "Queen Room", 305: "Twin Room", 306: "Queen Room",
            307: "Twin Room", 308: "Queen Room", 309: "Premium Suit"
        }

        #get rooms that are already booked
        booked_rooms = self.fetch_booked_rooms_on_date(checkin_date)
        booked_room_numbers = {info[1] for info in booked_rooms}
        self.available_room_types_and_numbers = {}

        #get rooms that are not booked
        for room_number, room_type in self.all_room_types_and_numbers.items():
            if room_number not in booked_room_numbers:
                # If the room type has not yet been added to the dictionary, initialize an empty list first
                if room_type not in self.available_room_types_and_numbers:
                    self.available_room_types_and_numbers[room_type] = []
                self.available_room_types_and_numbers[room_type].append(room_number)

        #update the list
        self.room_type_entry['values'] = list(self.available_room_types_and_numbers.keys())


    # ADD STAR SIGN
    def create_label_with_necessary(self, parent, text):
        label_with_necessary = tk.Label(parent, text="*" + text, fg="black")
        label_with_necessary.pack(side=tk.LEFT, padx=5)


    def fetch_booked_rooms_on_date(self, checkin_date):
        conn = None
        try:
            conn = sqlite3.connect('hotel_booking.db')
            c = conn.cursor()
            query = '''SELECT room_type, room_number FROM reservations WHERE checkin_date = ?'''
            c.execute(query, (checkin_date,))
            return c.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.close()

    def add_booking_to_database(self):
        # create a unique id
        timestamp = int(datetime.now().timestamp())
        reservation_id = f"24{timestamp}"

        # Collecting data from Entry widgets
        reservation_date = datetime.now().strftime("%Y-%m-%d")
        checkin_date = self.checkin_date_entry.get()
        checkout_date = self.checkout_date_entry.get()
        room_type = self.room_type_entry.get()
        room_number = self.room_number_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        number_of_guests = self.number_of_guests_entry.get()
        email = self.email_entry.get()
        phone_number = self.phone_number_entry.get()
        payment_method = self.payment_method_entry.get()
        special_requirements = self.special_requirements_entry.get()

        # Connect to the database and insert data
        try:
            conn = sqlite3.connect('hotel_booking.db')
            c = conn.cursor()

            insert_sql = '''INSERT INTO reservations (reservation_id, reservation_date, checkin_date, checkout_date, room_type, 
                                    room_number, first_name, last_name, number_of_guests, email, phone_number, 
                                    payment_method, special_requirements)  
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

            c.execute(insert_sql, (reservation_id, reservation_date, checkin_date, checkout_date, room_type,
                                   room_number, first_name, last_name, number_of_guests, email, phone_number,
                                   payment_method, special_requirements))

            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Insertion error: {e}")
        finally:
            if conn:
                conn.close()

        self.clear_entry_fields()

        # Refresh the information in the table
        if self.it:
            self.it.refresh_table_view()


    def clear_entry_fields(self):
        # Clear entry fields for regular Entry widgets
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_number_entry.delete(0, tk.END)
        self.special_requirements_entry.delete(0, tk.END)

        # Clear entry fields for ComboboxSelected
        self.room_type_entry.set('')
        self.room_number_entry.set('')
        self.number_of_guests_entry.set('')
        self.payment_method_entry.set('')

        # Reset DateEntry fields to today's date
        today = datetime.now()
        self.checkin_date_entry.set_date(today)
        self.checkout_date_entry.set_date(today)


# TOOLTIP WHEN MOUSE OVER THE BOOKING BUTTON
class Tooltip:
    def __init__(self, widget, text='Widget info'):
        self.waittime = 100  # Milliseconds
        self.wraplength = 130  # Pixels
        self.widget = widget
        self.text = text
        self.tipwindow = None  # Initialize tipwindow here
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        self.schedule()

    def close(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
        self.tipwindow = None

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = getattr(self, 'id', None)
        if id:
            self.widget.after_cancel(id)
        self.id = None

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() - 30
        y += self.widget.winfo_rooty() + 20

        # Creates a toplevel window
        self.tipwindow = tw = tk.Toplevel(self.widget)

        # Leaves only the label and removes the app window
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=10)

