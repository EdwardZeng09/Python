import tkinter as tk
import sqlite3
from tkinter import messagebox
from datetime import datetime


def get_room_reservations():
    '''
    Get room reservation info
    '''
    conn = sqlite3.connect('hotel_booking.db')
    c = conn.cursor()
    c.execute("SELECT room_type, room_number, checkin_date, checkout_date FROM reservations")
    reservations = c.fetchall()
    conn.close()

    # Process reservations into a more usable format
    room_reservations = {}
    for room_type, room, checkin, checkout in reservations:
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d').date()
        checkout_date = datetime.strptime(checkout, '%Y-%m-%d').date()
        if room not in room_reservations:
            room_reservations[room] = []
        # Append a tuple with all the data
        room_reservations[room].append((room_type, checkin_date, checkout_date))
    return room_reservations

class RoomBox:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create a canvas to place the room blocks
        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create the room number labels
        self.room_numbers = []
        for i in range(101, 110):
            self.room_numbers.append(i)
        for i in range(201, 210):
            self.room_numbers.append(i)
        for i in range(301, 310):
            self.room_numbers.append(i)
        self.rooms = {
            101: "Twin Room", 102: "Queen Room", 103: "Twin Room", 104: "Queen Room",
            105: "Twin Room", 106: "Queen Room", 107: "Twin Room", 108: "Queen Room",
            109: "Twin Room", 201: "Twin Room", 202: "Premium Suit", 203: "Twin Room",
            204: "Queen Room", 205: "Twin Room", 206: "Queen Room", 207: "Twin Room",
            208: "Queen Room", 209: "Premium Suit", 301: "Twin Room", 302: "Premium Suit",
            303: "Twin Room", 304: "Queen Room", 305: "Twin Room", 306: "Queen Room",
            307: "Twin Room", 308: "Queen Room", 309: "Premium Suit"
        }
        self.room_labels = []
        self.room_rectangles = []
        self.reservations = {}
        self.today = datetime.today().date()
        # the initial room blocks
        self.update_room_boxes()
        self.root.after(1000, self.refresh_room_boxes)
        # Bind the canvas resize event
        self.canvas.bind("<Configure>", self.on_resize)
    def update_room_boxes(self):
        # Clear previous room labels and rectangles
        for label in self.room_labels:
            self.canvas.delete(label)
        for rectangle in self.room_rectangles:
            self.canvas.delete(rectangle)

        self.room_labels.clear()
        self.room_rectangles.clear()
        self.reservations = get_room_reservations()

        # Determine the size of the canvas
        canvas_width = self.canvas.winfo_width()
        num_rooms = len(self.room_numbers)  # Adjust the room height dynamically based on the number of rooms
        rooms_per_row = 9  # Assume 6 rooms per row
        num_rows = (num_rooms + rooms_per_row - 1) // rooms_per_row  # Calculate required rows
        room_width = canvas_width // rooms_per_row
        canvas_height = self.canvas.winfo_height()
        room_height = canvas_height // num_rows  # Dynamically calculate room height based on the number of rows

        for index, room_number in enumerate(self.room_numbers):
            x1 = (index % rooms_per_row) * room_width
            y1 = (index // rooms_per_row) * room_height
            x2 = x1 + room_width
            y2 = y1 + room_height
            # Determine room color based on reservation status
            room_color = 'lightgrey'  # Default color: available today
            if room_number in self.reservations:
                for room_type, checkin, checkout in self.reservations[room_number]:
                    if self.today >= checkin and self.today <= checkout:
                        room_color = '#274b6c'  # Occupied today (priority)
                    elif self.today < checkin:
                        room_color = '#f5ecc4'  # Reserved in the future
            # Create rectangle and text for each room
            rectangle = self.canvas.create_rectangle(x1, y1, x2, y2, outline="White", fill=room_color, width=10, tags="room")
            label = self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=f'Room {room_number}')
            self.room_labels.append(label)
            self.room_rectangles.append(rectangle)
            # Add click event
            self.canvas.tag_bind(rectangle, "<Button-1>", lambda event, room=room_number: self.show_room_info(room))

    def refresh_room_boxes(self):
        '''
        Update room information
        '''
        self.update_room_boxes()
        # Reschedule the update
        self.root.after(1000, self.refresh_room_boxes)
    def on_resize(self, event):
        # Redraw room blocks with new sizes
        self.update_room_boxes()


    # Room Info MessageBox (Able to click the room box)
    def show_room_info(self, room_number):
        reservations = self.reservations.get(room_number, [])
        room_type = self.rooms.get(room_number)
        # If there are no reservations, set a default message and room type
        dates_reserved = ""
        for type, checkin, checkout in reservations:
            if self.today <= checkin: # Only show today or future date
                if dates_reserved:  # If the string is not empty, add a comma before adding more dates
                    dates_reserved += ", "
                dates_reserved += f"{checkin.strftime('%Y-%m-%d')} to {checkout.strftime('%Y-%m-%d')}"

        # Display room info in a message box
        messagebox.showinfo(
            f"Room {room_number}",
            f"Type: {room_type}\nReserved dates: {dates_reserved}"
        )
