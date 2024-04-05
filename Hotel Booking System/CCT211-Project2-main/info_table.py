import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3


class InfoTable:
    def __init__(self, master):

        # Main frame that contains everything
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame for the table and scrollbars
        self.tree_frame = tk.Frame(self.main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Frame for the delete button
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Vertical scrollbar
        self.tree_scroll_y = tk.Scrollbar(self.tree_frame, orient=tk.VERTICAL)
        self.tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Horizontal scrollbar
        self.tree_scroll_x = tk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL)
        self.tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview widget
        self.tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll_y.set,
                                 xscrollcommand=self.tree_scroll_x.set,
                                 selectmode="browse")
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Configuring the scrollbars
        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)

        # Create Columns
        self.tree['columns'] = ("Reservation ID","Reservation Date", "Checkin Date", "Checkout Date", "Room Type", "Room Number",
                                "First Name", "Last Name", "Number of Guests", "Email", "Phone Number",
                                "Payment Method", "Special Requirements")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Reservation ID", anchor=tk.W, width=10)
        self.tree.column("Reservation Date", anchor=tk.CENTER, width=120)
        self.tree.column("Checkin Date", anchor=tk.CENTER, width=120)
        self.tree.column("Checkout Date", anchor=tk.CENTER, width=120)
        self.tree.column("Room Type", anchor=tk.CENTER, width=120)
        self.tree.column("Room Number", anchor=tk.CENTER, width=60)
        self.tree.column("First Name", anchor=tk.CENTER, width=120)
        self.tree.column("Last Name", anchor=tk.CENTER, width=120)
        self.tree.column("Number of Guests", anchor=tk.CENTER, width=60)
        self.tree.column("Email", anchor=tk.W, width=160)
        self.tree.column("Phone Number", anchor=tk.CENTER, width=120)
        self.tree.column("Payment Method", anchor=tk.CENTER, width=60)
        self.tree.column("Special Requirements", anchor=tk.W, width=200)

        self.tree.heading("#0", text="", anchor=tk.CENTER)
        self.tree.heading("Reservation ID", text="#", anchor=tk.CENTER)
        self.tree.heading("Reservation Date", text="Reservation Date", anchor=tk.CENTER)
        self.tree.heading("Checkin Date", text="Checkin", anchor=tk.CENTER)
        self.tree.heading("Checkout Date", text="Checkout", anchor=tk.CENTER)
        self.tree.heading("Room Type", text="Room Type", anchor=tk.CENTER)
        self.tree.heading("Room Number", text="Room", anchor=tk.CENTER)
        self.tree.heading("First Name", text="First Name", anchor=tk.CENTER)
        self.tree.heading("Last Name", text="Last Name", anchor=tk.CENTER)
        self.tree.heading("Number of Guests", text="Guests", anchor=tk.CENTER)
        self.tree.heading("Email", text="Email", anchor=tk.CENTER)
        self.tree.heading("Phone Number", text="Phone Number", anchor=tk.CENTER)
        self.tree.heading("Payment Method", text="Payment", anchor=tk.CENTER)
        self.tree.heading("Special Requirements", text="Notes", anchor=tk.CENTER)

        self.load_data_from_db()

        # Add a delete Button, able to delete selected data row
        self.delete_button = tk.Button(self.button_frame, text="Delete Selected", command=self.delete_selected_entry)
        self.delete_button.pack(side=tk.BOTTOM, pady=5)

    def load_data_from_db(self):
        """Load reservation data from the SQLite database and populate the Treeview."""
        try:
            conn = sqlite3.connect('hotel_booking.db')
            c = conn.cursor()
            c.execute('SELECT * FROM reservations')
            rows = c.fetchall()
            if rows:
                print(f"{len(rows)} rows fetched from the database.")
            else:
                print("No data fetched. The database might be empty or not connected properly.")

            for row in rows:
                print(f"Inserting row: {row}")
                self.tree.insert("", 0, values=row)  # O means Insert at the beginning
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    def refresh_table_view(self):

        # Clear existing entries in the table view.
        for entry in self.tree.get_children():
            self.tree.delete(entry)

        # Query the database for the latest reservation data.
        conn = sqlite3.connect('hotel_booking.db')
        c = conn.cursor()
        c.execute(
            "SELECT reservation_id, reservation_date, checkin_date, checkout_date, room_type, room_number, first_name, last_name, "
            "number_of_guests, email, phone_number, payment_method, special_requirements FROM reservations")
        rows = c.fetchall()

        # Repopulate the table view with the latest data.
        for row in rows:
            self.tree.insert("", 0, values=row)



    # DELETE THE INFORMATION FROM DATABASE

    def delete_selected_entry(self):
        selected_item = self.tree.selection()
        if selected_item:  # Check if something is selected
            reservation_id = self.tree.item(selected_item[0])['values'][0]  # reservation_id is a unique attribute
            confirm = tk.messagebox.askyesno("Confirm Delete", "Are you sure you want to delete it?")
            if confirm:
                try:
                    conn = sqlite3.connect('hotel_booking.db')
                    c = conn.cursor()
                    # Execute delete operation (the row of room_number)
                    c.execute('DELETE FROM reservations WHERE reservation_id = ?', (reservation_id,))
                    conn.commit()
                    self.tree.delete(selected_item[0])  # Delete
                    print("Entry deleted successfully.")
                except sqlite3.Error as e:
                    print(f"Database error: {e}")
                finally:
                    if conn:
                        conn.close()
