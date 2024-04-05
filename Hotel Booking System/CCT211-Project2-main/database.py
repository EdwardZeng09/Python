import sqlite3

def create_and_populate_db():
    conn = sqlite3.connect('hotel_booking.db')
    c = conn.cursor()

    # Drop the existing table to start fresh
    c.execute('DROP TABLE IF EXISTS reservations')

    # Create table with the correct order of columns as per your listing
    c.execute('''CREATE TABLE IF NOT EXISTS reservations
                 (reservation_id INTEGER,
                  reservation_date TEXT,
                  checkin_date TEXT,
                  checkout_date TEXT,
                  room_type TEXT,
                  room_number INTEGER,
                  first_name TEXT,
                  last_name TEXT,
                  number_of_guests INTEGER,
                  email TEXT,
                  phone_number INTEGER,
                  payment_method TEXT,
                  special_requirements TEXT)''')

    # Insert Data with the new order
    reservations = [
        ('241708710612', '2024-01-01', '2024-01-05', '2024-01-08', 'Queen Room', 104, 'Dale', 'Harvey', 1, 'daleharvey123@jerys.com', 9961117865, 'debit', 'Early check-in if possible.'),
        ('243017699723', '2024-01-03', '2024-01-04', '2024-01-10', 'Twin Room', 105, 'Penny', 'Harper', 1, 'pennyharper@uhooi.com', 9852122586, 'debit', 'Add an extra bed.'),
        ('242764459132', '2024-01-27', '2024-01-28', '2024-02-11', 'Queen Room', 106, 'Andrew', 'Cruz', 1, 'andrewcruz@fhkac.com', 5636853312, 'credit', 'No peanuts in the minibar, please.'),
        ('241982330234', '2024-01-30', '2024-01-31', '2024-02-02', 'Twin Room', 107, 'Luke', 'Jones', 2, 'lukejones@xxdj.com', 5729572000, 'credit', 'Early check-in if possible.'),
        ('245646706656', '2024-02-05', '2024-02-05', '2024-02-07', 'Queen Room', 108, 'Ryan', 'Whitney', 2, 'ryanwhitney@rmhns.com', 5779003675, 'credit', ''),
        ('240497440836', '2024-02-14', '2024-02-15', '2024-03-06', 'Twin Room', 109, 'Douglas', 'Miller', 4, 'douglasmiller985@yttps.com', 6578389982, 'debit', 'Early check-in if possible.'),
        ('245292255078', '2024-02-15', '2024-02-16', '2024-02-18', 'Queen Room', 206, 'Karen', 'Sanchez', 1, 'karensanchez@hhuyod.com', 9807896688, 'debit', 'High floor request.'),
        ('246286165953', '2024-02-25', '2024-02-26', '2024-03-01', 'Twin Room', 201, 'Shannon', 'Lynch', 3, 'shannolych@bjyx.com', 9059955238, 'debit', ''),
        ('249163753565', '2024-03-03', '2024-03-05', '2024-03-08', 'Queen Room', 204, 'James', 'Hardin', 4, 'jameshardin@hakfh.com', 7685995903, 'cash', 'High floor request.'),
        ('242422474117', '2024-03-09', '2024-03-10', '2024-03-25', 'Twin Room', 303, 'Michael', 'Campbell', 2, 'michaelcampbell@hfiw.com', 3783982002, 'credit', 'Early check-in if possible.'),
        ('248559730890', '2024-03-10', '2024-03-12', '2024-03-15', 'Twin Room', 301, 'Taylor', 'Broewn', 3, 'talorbroewn98@fhska.com', 5673392095, 'credit', 'Extra pillows.'),
        ('243017699043', '2024-03-12', '2024-03-15', '2024-03-18', 'Twin Room', 205, 'Quinn', 'Miller', 1, 'quinnmiller850@bdkm.com', 9068302112, 'credit', 'Late checkout if possible.'),
        ('245646706335', '2024-03-14', '2024-03-18', '2024-03-23', 'Premium Suit', 202, 'Sean', 'Wang', 2, 'seanwang95@lsfy.com', 8059051005, 'debit', 'n/a'),
        ('245233334012', '2024-03-23', '2024-03-25', '2024-03-28', 'Queen Room', 306, 'Eden', 'Bae', 2, 'edenbae0905@zsww.com', 9057090101, 'debit', 'Extra bottles of water.'),
        ('244234165111', '2024-03-28', '2024-03-31', '2024-04-03', 'Premium Suit', 302, 'Avery', 'Martinez', 2, 'averymartinez@dhiqfh.com', 587295895, 'credit', 'Extra towels.'),
        ('241708710612', '2024-03-30', '2024-04-05', '2024-04-11', 'Queen Room', 104, 'Dale', 'Harvey', 1, 'daleharvey123@jerys.com', 9961117865, 'debit', 'Early check-in if possible.'),
        ('243017699723', '2024-04-01', '2024-04-07', '2024-04-10', 'Twin Room', 305, 'Penny', 'Harper', 1, 'pennyharper@uhooi.com', 9852122586, 'debit', 'Add an extra bed.'),
        ('241225502343', '2024-04-02', '2024-04-08', '2024-04-09', 'Queen Room', 106, 'Andrew', 'Cruz', 1, 'andrewcruz@fhkac.com', 5636853312, 'credit', 'No peanuts in the minibar, please.'),
        ('241932330454', '2024-04-03', '2024-04-09', '2024-04-12', 'Twin Room', 207, 'Luke', 'Jones', 2, 'lukejones@xxdj.com', 5729572000, 'credit', 'Early check-in if possible.'),
        ('245645893786', '2024-04-04', '2024-04-10', '2024-04-11', 'Queen Room', 108, 'Ryan', 'Whitney', 2, 'ryanwhitney@rmhns.com', 5779003675, 'credit', ''),
        ('241223893658', '2024-04-05', '2024-04-09', '2024-04-17', 'Queen Room', 204, 'Shengyi', 'Feng', 2, 'verseaufsy@gmail.com', 6787103675, 'cash', 'Late check-in if possible.'),
        ('242542474217', '2024-04-05', '2024-04-12', '2024-04-15', 'Premium Suit', 202, 'Michael', 'Nixon', 3, 'michaelnixon@utoronto.ca', 3783982002, 'credit', 'Celebrate Summer Vocation'),
    ]
    c.executemany('INSERT INTO reservations VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', reservations)

    conn.commit()
    conn.close()

create_and_populate_db()
