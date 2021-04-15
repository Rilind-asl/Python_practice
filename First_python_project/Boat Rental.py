import sqlite3

from datetime import datetime

# DBbase to CRUD data.
class DBbase:
    _conn = None
    _cursor = None

    def __init__(self, db_name):
        self._db_name = db_name

    def connect(self):
        self._conn = sqlite3.connect(self._db_name)
        self._cursor = self._conn.cursor()

    def execute_script(self, sql_string):
        self._cursor.executescript(sql_string)

    def close_db(self):
        self._conn.close()

    def reset_database(self):
        return NotImplementedError()

    @property
    def get_cursor(self):
        return self._cursor

    @property
    def get_connection(self):
        return self._conn

# class used to CRUD the boat rental DB
class BoatInventory(DBbase):

    def __init__(self):
        super().__init__("BoatDB.sqlite")

    # function used add a new boat
    def add_new_boat(self, boat_name, price, qty, availability):
        try:
            super().connect()
            super().get_cursor.execute("""insert or ignore into Boats (boat_name, rental_price, quantity, availability) values (?, ?, ?, ?)""", (boat_name, price, qty, availability))
            super().get_connection.commit()
            super().close_db()
            print("added boat successfully")
        except Exception as e:
            print("An error occurred trying to add new boat.", e)

    # function used to update a boat in the dB
    def update_boat(self, id, boat_name, price, qty, availability):
        try:
            super().connect()
            super().get_cursor.execute("""update Boats set quantity = ?, rental_price = ?, boat_name = ?, availability = ? where id = ?""", (qty, price, boat_name, availability, id))
            super().get_connection.commit()
            super().close_db()
            print("Boat updated successfully")
        except Exception as e:
            print("An error occurred.", e)

    # function used to review boat data
    def review_boat(self, id=None, boat_name=None):
        try:
            super().connect()
            if id is not None:
                return super().get_cursor.execute("""SELECT * FROM Boats WHERE id = ?;""", (id,)).fetchone()
            elif boat_name is not None:
                return super().get_cursor.execute("""SELECT id FROM Boats WHERE name = ?;""", (boat_name,)).fetchone()
            else:
                return super().get_cursor.execute("""SELECT * FROM Boats;""").fetchall()
        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    # deleting a boat from database
    def delete_boat(self, id):
        try:
            super().connect()
            super().get_cursor.execute("""delete from Boats where id = ?""", (id,))
            super().get_connection.commit()
            super().close_db()
            print("deleted Boat successfully")
            return True
        except Exception as e:
            print("An error occurred.", e)
            return False

    # resetting the whole database
    def reset_database(self):
        sql = """
            DROP TABLE IF EXISTS Boats;
            
            CREATE TABLE Boats (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                boat_name TEXT,
                quantity INTEGER NOT NULL,
                rental_price varchar(20),
                availability INTEGER NOT NULL
            );
        
        """
        super().execute_script(sql)

# class used to create boat rental applications
class Application(DBbase):
    def __init__(self):
        super().__init__("BoatDB.sqlite")

    # function used to create new applications in dB
    def new_application(self, boat_id, fname, lname, ccnumber, date):
        try:
            super().connect()
            super().get_cursor.execute("""insert or ignore into Application (boat_id, customer_fname, customer_lname, credit_card_number, reservation_date) values (?,?,?,?,?);""", (boat_id, fname, lname, ccnumber, date))
            super().get_connection.commit()
            super().close_db()
            print("added Application successfully")
        except Exception as e:
            print("An error occurred in the add application function.", e)

    # function used to change the application
    def change_app(self, boat_id, fname, lname, ccnumber, date, id):
        try:
            super().connect()
            super().get_cursor.execute("""update Application set boat_id = ?, customer_fname = ?, customer_lname = ?, credit_card_number = ?, reservation_date = ? where id = ?""", (boat_id, fname, lname,ccnumber, date, id))
            super().get_connection.commit()
            super().close_db()
            print("Application updated successfully")
        except Exception as e:
            print("An error occurred.", e)

    # function used to get the application from dB
    def retrieve_app(self, id=None, fname=None, lname=None):
        try:
            super().connect()
            if id is not None:
                return super().get_cursor.execute("""SELECT * FROM Application WHERE id = ?;""", (id,)).fetchone()
            elif fname is not None:
                return super().get_cursor.execute("""SELECT id FROM Application WHERE customer_fname = ?;""", (fname,)).fetchone()
            elif lname is not None:
                return super().get_cursor.execute("""SELECT id FROM Application WHERE customer_lname = ?;""", (lname,)).fetchone()
            else:
                return super().get_cursor.execute("""SELECT * FROM Application;""").fetchall()
        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    # function used to remove an application
    def remove_app(self, app_id):
        try:
            super().connect()
            super().get_cursor.execute("""delete from Application where id = ?""", (app_id,))
            super().get_connection.commit()
            super().close_db()
            print("deleted Application successfully")
            return True
        except Exception as e:
            print("An error occurred.", e)
            return False

    # function used to reset dB
    def reset_database(self):
        sql = """
            DROP TABLE IF EXISTS Application;
            
            CREATE TABLE Application (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                boat_id INTEGER NOT NULL,
                customer_fname TEXT,
                customer_lname TEXT,
                credit_card_number INTEGER,
                reservation_date TEXT
            );
        
        """
        super().execute_script(sql)

# creating the boat and app objects and connecting to the database
boat = BoatInventory()
app = Application()
boat.connect()
app.connect()

# rental options interface
Rental_Options = {
    "Availability": "Check out all available boats",
    "Prices": "Check daily rental prices",
    "Apply": "Apply for a boat",
    "Update": "Update application",
    "Review": "Review application",
    "Return": "Return a rental",
    "Refresh": "Remove old records",
    "Delete": "Delete a specific application",
    "Exit": "To Exit"
}

# database interface so users can modify the database with these options
BoatDatabase = {
    "Add": "Add a new Boat",
    "Delete": "Delete a Boat",
    "Update": "Update a Boat",
    "Fetch": "Fetch database",
    "Done": "When Done"
}

# Checking if user wants to modify database fist
user_input = input("Do you want to modify the boats database: (Y/N) ")
if user_input.strip().lower() == "y":

    # keeps asking user what they want to change in the Db until 'done' is entered.
    while user_input.strip().lower() != "done":
        print("***Boat Database***")

        # prints out the options for the BoatDb dictionary
        for x in BoatDatabase.items():
            print(x)

        # grabs input and checks what the user wants to do
        user_input = input("Select an option: ")

        # if the user wants to add a new boat to the db it goes through this statement
        if user_input.lower().strip() == "add":
            print(boat.review_boat())
            availability = int(input("Availability 1 = True, 0 = False: "))
            boat_name = input("Type of Boat: ").lower()
            rental_price = int(input("Daily rental Price: "))
            qty = int(input("Quantity of boats available: "))
            boat.add_new_boat(boat_name, rental_price, qty, availability)
            print("Done\n")

        # if the user wants to delete a boat from the database it goes through this statement
        elif user_input.lower().strip() == "delete":
            print(boat.review_boat())
            id = int(input("Please enter id of the boat you want to delete: "))
            boat.delete_boat(id)
            print("Done\n")

        # if the user wants to update a boat it goes through this statement
        elif user_input.lower().strip() == "update":
            print(boat.review_boat())
            boat_id = int(input("Enter boat id for the boat you wish to update: "))
            boat_name = input("Update name: ")
            price = int(input("Update price: "))
            qty = int(input("Update quantity: "))
            availability = int(input("Update availability 1 = True, 0 = False: "))
            boat.update_boat(boat_id, boat_name, price, qty, availability)
            print(boat.review_boat())
            print("Done\n")

        # if the user wants to review the information in database it goes through this statement
        elif user_input.lower().strip() == "fetch":
            id = int(input("Please enter the id of the boat you want to fetch: "))
            print(boat.review_boat(id))
            print("Done\n")

        # if something else is input it will show invalid unless its 'done' in which case it will leave the original statement and move on to the next chunk of code.
        else:
            if user_input.lower().strip() == "done":
                print(boat.review_boat())
                print("Done\n")
                continue
            print("Invalid entry please try again\n")

# if user didn't want to modify the Db or if the user is done modifying the Db
if user_input.strip().lower() != "y":

    # Boat applications code starts now and doesn't end until 'exit' is entered
    while user_input.strip().lower() != "exit":
        print("***Boat Applications***")

        # prints out all the options in the rental dictionary
        for x in Rental_Options.items():
            print(x)

        # grabs user input from the dictionary options
        user_input = input("Select an option: ")
        if user_input.strip().lower() == "availability":
            print("*** AVAILABLE BOATS ****")

            # prints out all available boats depending on their availability give in the if statement 1 = True and 0 = False for availability
            for index in range(len(boat.review_boat())):
                if boat.review_boat()[index][4] == 1:
                    print(boat.review_boat()[index][1], "is available", "Boat ID:", boat.review_boat()[index][0])
            print("Done\n")

        # if the user wants to refresh the database and get rid of outdated information
        elif user_input.strip().lower() == "refresh":
            print("Refreshing the database, please wait one moment")
            print(type(app.retrieve_app()), app.retrieve_app())
            for item in app.retrieve_app():
                if item[1] == 0:
                    print("Found old record:", app.retrieve_app(item[0]), "it has been deleted.")
                    app.remove_app(item[0])
            print("\nThe database has been refreshed.\n")

        # if the user wants to apply for a boat rental they are asked for the following information
        elif user_input.strip().lower() == "apply":
            print("*** BOAT APPLICATION ****")
            boat_id = int(input("Enter the boat id you wish to rent: "))
            fname = input("Enter your first name: ").lower()
            lname = input("Enter your last name: ").lower()
            ccnumber = int(input("Enter your credit card number: "))

            # date is checked against today's date since you can't rent a boat in the past it must be today's date or a future date.
            date = input("Enter the date of rental: (MM/DD/YYYY) ")
            d = date.split("/")
            months = d[0]
            days = d[1]
            years = d[2]
            now = datetime.now()
            print(date, now.month, now.day, now.year)

            # while loop to check the date as mentioned above
            while int(years) < now.year or int(months) < now.month or int(days) < now.day:
                print("Please make sure your date is correct")
                date = input("Re-Enter the date of rental: (MM/DD/YYYY) ")
                d = d.split("/")
                months = d[0]
                days = d[1]
                years = d[2]

            # grab all the information about the boat
            id = boat.review_boat(boat_id)[0]
            boat_name = boat.review_boat(boat_id)[1]
            boat_qty = boat.review_boat(boat_id)[2]
            boat_price = boat.review_boat(boat_id)[3]
            boat_avail = boat.review_boat(boat_id)[4]

            # check if the boat quantity is above 0, in-case a user wants to borrow a boat that's unavailable
            if boat_qty > 0:
                if boat_qty == 1:
                    boat.update_boat(id, boat_name, boat_price, boat_qty-1, 0)
                else:
                    boat.update_boat(id, boat_name, boat_price, boat_qty-1, boat_avail)
                app.new_application(boat_id, fname, lname, ccnumber, date)
                print("")
                print("You are now renting the", boat_name, "for the day and your card will be charged: $" + boat_price, "US dollars daily\n")

            # if the boat is unavailable they will not be able to borrow this boat
            else:
                boat.update_boat(id, boat_name, boat_price, boat_qty, 0)
                print("Boat is currently unavailable please try a different boat.\n")

        # print out the prices for all available boats
        elif user_input.strip().lower() == "prices":
            print("*** PRICES FOR AVAILABLE BOATS ****")
            for index in range(len(boat.review_boat())):
                if boat.review_boat()[index][4] == 1:
                    print("The", boat.review_boat()[index][1], "daily price is:", boat.review_boat()[index][3])
            print("Done\n")

        # return a boat rental will go through this statement
        elif user_input.strip().lower() == "return":
            user_input = input("Please select a method of application searching:\n 'id' or 'first_name' or 'last_name' ")
            user_id = None

            # first set of if statements checks the boat by id, first, or last name
            if user_input.strip().lower() == "id":
                user_id = input("To review your application please enter your id: ")
                print("application tuple:", app.retrieve_app(user_id))
            elif user_input.strip().lower() == "first_name":
                fname = input("To review your application please enter your first name: ").lower()
                user_id = app.retrieve_app(id=None, fname=fname)[0]
                print("Application tuple: ", app.retrieve_app(user_id))
            elif user_input.strip().lower() == "last_name":
                lname = input("To review your application please enter your last name: ").lower()
                user_id = app.retrieve_app(id=None, fname=None, lname=lname)[0]
                print("Application tuple: ", app.retrieve_app(user_id))

            # grab all the information from the current application
            temp_app_id = app.retrieve_app(user_id)[0]
            temp_boat_id = app.retrieve_app(user_id)[1]
            temp_fname = app.retrieve_app(user_id)[2]
            temp_lname = app.retrieve_app(user_id)[3]
            temp_ccnumber = app.retrieve_app(user_id)[4]
            temp_date = app.retrieve_app(user_id)[5]

            # check if the user_id is not 0
            if user_id != 0:
                boat_id = app.retrieve_app(user_id)[1]
                app.change_app(0, temp_fname, temp_lname, temp_ccnumber, temp_date, temp_app_id)
                try:
                    temp_boat_id = boat.review_boat(boat_id)[0]
                    temp_boat_name = boat.review_boat(boat_id)[1]
                    temp_qty = boat.review_boat(boat_id)[2]
                    temp_price = boat.review_boat(boat_id)[3]
                    temp_availability = boat.review_boat(boat_id)[4]
                    boat.update_boat(temp_boat_id, temp_boat_name, temp_price, temp_qty+1, 1)
                    print("The", boat.review_boat(boat_id)[1], "has been returned\n")
                except Exception as e:
                    print("The client doesn't have a boat to return\n", " Refreshing records, one moment please...\n", "     ...records updated, please try again.\n")
                    app.remove_app(temp_app_id)
            else:
                print("No boat id found, please try again")

        # update the information about the give application
        elif user_input.strip().lower() == "update":
            user_input = input("Please select a method of application searching:\n 'id' or 'first_name' or 'last_name' ")
            if user_input.strip().lower() == "id":
                id = input("To review your application please enter your id: ")
                print("id:", app.retrieve_app(id))
            elif user_input.strip().lower() == "first_name":
                fname = input("To review your application please enter your first name: ").lower()
                id = app.retrieve_app(id=None, fname=fname)[0]
                print("Application details: ", app.retrieve_app(id))
            elif user_input.strip().lower() == "last_name":
                lname = input("To review your application please enter your last name: ").lower()
                id = app.retrieve_app(id=None, fname=None, lname=lname)[0]
                print("Application details: ", app.retrieve_app(id))

            # keep grabbing the boat id for a boat that is actually available
            boat_id = int(input("Please re-enter the boat id you want to rent: "))
            if boat_id != app.retrieve_app(id)[1]:
                temp_id = app.retrieve_app(id)[1]
                my_boat = boat.review_boat(temp_id)
                print(my_boat)
                my_id = int(my_boat[0])
                name = my_boat[1]
                qty = int(my_boat[2])
                p = int(my_boat[3])

                # check if the boat has quantity available
                if boat.review_boat(boat_id)[2] > 1:
                    boat.update_boat(id=boat_id, boat_name=boat.review_boat(boat_id)[1], qty=int(boat.review_boat(boat_id)[2])-1, price=int(boat.review_boat(boat_id)[3]), availability=1)
                    boat.update_boat(id=my_id, boat_name=name, price=p, qty=qty+1, availability=1)
                elif boat.review_boat(boat_id)[2] == 1:
                    boat.update_boat(id=boat_id, boat_name=boat.review_boat(boat_id)[1], qty=int(boat.review_boat(boat_id)[2])-1, price=int(boat.review_boat(boat_id)[3]), availability=0)
                    boat.update_boat(id=my_id, boat_name=name, price=p, qty=qty+1, availability=1)

                # if the boat has no availability it will tell the user they were unable find a boat the want to rent
                else:
                    boat_id = app.retrieve_app(id)[1]
                    print("Error boat not found, unable to change")

            # continue updating other information
            fname = input("Please re-enter your first name: ").lower()
            lname = input("Please re-enter your last name: ").lower()
            ccnumber = int(input("Please re-enter your credit card number: "))

            # checks the date against today's date.
            date = input("Please re-enter your reservation date: (MM/DD/YYY) ")
            d = date.split("/")
            months = d[0]
            days = d[1]
            years = d[2]
            now = datetime.now()
            print(date, now.month, now.day, now.year)

            # loop through until the date is equal to today or in the future.
            while int(years) < now.year or int(months) < now.month or int(days) < now.day:
                print("Please make sure your date is correct")
                date = input("Re-Enter the date of rental: (MM/DD/YYYY) ")
                d = date.split("/")
                months = d[0]
                days = d[1]
                years = d[2]

            id = int(input("Please enter an application id: "))

            app.change_app(boat_id, fname, lname, ccnumber, date, id)
            print("new application details:", app.retrieve_app(id))

        # allows the user to view their applications and information
        elif user_input.strip().lower() == "review":
            user_input = input("Please select a method of application searching:\n 'id' or 'first_name' or 'last_name' ")
            if user_input.strip().lower() == "id":
                id = input("To review your application please enter your id: ")
                print("id:", app.retrieve_app(id))
            elif user_input.strip().lower() == "first_name":
                fname = input("To review your application please enter your first name: ").lower()
                id = app.retrieve_app(id=None, fname=fname)[0]
                print("Application details: ", app.retrieve_app(id))
            elif user_input.strip().lower() == "last_name":
                lname = input("To review your application please enter your last name: ").lower()
                id = app.retrieve_app(id=None, fname=None, lname=lname)[0]
                print("Application details: ", app.retrieve_app(id))
        elif user_input.strip().lower() == "delete":
            app_id = int(input("Please enter your application id: "))
            my_app = app.retrieve_app(app_id)
            my_boat = boat.review_boat(my_app[1])
            print(my_boat)
            boat.update_boat(int(my_boat[0]),my_boat[1], int(my_boat[3]), int(my_boat[2])+1, 1)
            print(my_boat)
            app.remove_app(app_id)

        # checks if the user entered an invalid input or if the user entered 'exit'
        else:
            if user_input.strip().lower() == "exit":
                continue
            print("Invalid entry please try again\n")
