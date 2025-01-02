# north_sussex_judo.py
import pyodbc
import datetime
from tabulate import tabulate
from getpass import getpass
import hashlib

# Configuration for database connection
SERVER = 'your_server_name'  # Replace with your server name
DATABASE = 'NorthSussexJudoDB' # Replace if you used a different name
USERNAME = 'your_username' # Replace with your username
PASSWORD = 'your_password'  # Replace with your password

def db_connect():
    """Connects to the database."""
    try:
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}')
        return conn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database Error: Could not connect to the server. Check your configuration. {sqlstate}")
        return None


def authenticate_user():
    """Authenticates the user."""
    conn = db_connect()
    if conn is None:
        return False, None
    
    while True:
        username = input("Username: ")
        password = getpass("Password: ")

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT UserID FROM Users WHERE Username = ? AND Password = ?", (username, hashed_password))
            user = cursor.fetchone()
            if user:
                print("Authentication successful.\n")
                conn.close()
                return True, username
            else:
                print("Authentication failed. Please try again.")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Database Error: Authentication failed. {sqlstate}")
            conn.close()
            return False, None


def main_menu():
    """Displays the main menu."""
    print("\nNorth Sussex Judo System")
    print("-----------------------")
    print("1. Manage Athletes")
    print("2. Manage Training Plans")
    print("3. Manage Competitions")
    print("4. Manage Coaching")
    print("5. Generate Reports")
    print("6. Exit")

def manage_athletes(username):
    """Handles athlete management."""
    conn = db_connect()
    if conn is None:
        return

    while True:
        print("\nAthlete Management")
        print("-------------------")
        print("1. Add Athlete")
        print("2. View Athletes")
        print("3. Update Athlete")
        print("4. Delete Athlete")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                add_athlete(conn)
            elif choice == '2':
                view_athletes(conn)
            elif choice == '3':
                update_athlete(conn)
            elif choice == '4':
                delete_athlete(conn)
            elif choice == '5':
                conn.close()
                return
            else:
                print("Invalid choice, please try again.\n")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Database Error: Could not process. {sqlstate}\n")
            conn.close()
            return

def add_athlete(conn):
    """Adds a new athlete."""
    try:
        cursor = conn.cursor()
        name = input("Athlete name: ")
        view_training_plans(conn, False)
        training_plan = input("Choose Training Plan: ")
        weight = input("Current weight (kg): ")
        category = input("Competition weight category: ")
        
        cursor.execute("INSERT INTO Athletes (AthleteName, TrainingPlanID, CurrentWeight, CompetitionWeightCategory) VALUES (?, ?, ?, ?)", (name, training_plan, weight, category))
        conn.commit()
        print("Athlete added successfully.\n")
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database Error: Could not add athlete. {sqlstate}\n")

def view_athletes(conn):
    """Views all athletes."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                A.AthleteID,
                A.AthleteName,
                T.PlanName,
                A.CurrentWeight,
                A.CompetitionWeightCategory
            FROM
                Athletes A
            INNER JOIN
                TrainingPlans T ON A.TrainingPlanID = T.TrainingPlanID
        """)
        athletes = cursor.fetchall()
        headers = ["ID", "Name", "Training Plan", "Weight (kg)", "Category"]
        print(tabulate(athletes, headers=headers, tablefmt="grid"))
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database Error: Could not view athletes. {sqlstate}\n")


def update_athlete(conn):
    """Updates an athlete's details."""
    try:
        view_athletes(conn)
        athlete_id = input("Enter Athlete ID to update: ")

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Athletes WHERE AthleteID = ?", (athlete_id,))
        athlete = cursor.fetchone()
        
        if not athlete:
            print("Athlete not found.\n")
            return
        
        print("\nWhat do you want to update?\n")
        print("1. Name")
        print("2. Training Plan")
        print("3. Current Weight")
        print("4. Competition Weight Category")
        print("5. Return to Athlete Menu")

        update_choice = input("Enter your choice: ")

        if update_choice == '1':
            new_name = input("New Athlete Name: ")
            cursor.execute("UPDATE Athletes SET AthleteName = ? WHERE AthleteID = ?", (new_name, athlete_id))
        elif update_choice == '2':
            view_training_plans(conn, False)
            new_plan = input("New Training Plan: ")
            cursor.execute("UPDATE Athletes SET TrainingPlanID = ? WHERE AthleteID = ?", (new_plan, athlete_id))
        elif update_choice == '3':
             new_weight = input("New Weight (kg): ")
             cursor.execute("UPDATE Athletes SET CurrentWeight = ? WHERE AthleteID = ?", (new_weight, athlete_id))
        elif update_choice == '4':
            new_category = input("New Category: ")
            cursor.execute("UPDATE Athletes SET CompetitionWeightCategory = ? WHERE AthleteID = ?", (new_category, athlete_id))
        elif update_choice == '5':
            return
        else:
           print("Invalid choice, returning to Athlete Menu.\n")
           return
        conn.commit()
        print("Athlete updated successfully.\n")
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database Error: Could not update athlete. {sqlstate}\n")

def delete_athlete(conn):
    """Deletes an athlete."""
    try:
        view_athletes(conn)
        athlete_id = input("Enter Athlete ID to delete: ")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Athletes WHERE AthleteID = ?", (athlete_id,))
        conn.commit()
        print("Athlete deleted successfully.\n")
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database Error: Could not delete athlete. {sqlstate}\n")

def manage_training_plans(username):
    """Handles training plan management."""
    conn = db_connect()
    if conn is None:
        return
    while True:
        print("\nTraining Plan Management")
        print("------------------------")
        print("1. Add Training Plan")
        print("2. View Training Plans")
        print("3. Update Training Plan")
        print("4. Delete Training Plan")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")
        try:
            if choice == '1':
               add_training_plan(conn)
            elif choice == '2':
                view_training_plans(conn, True)
            elif choice == '3':
                update_training_plan(conn)
            elif choice == '4':
               delete_training_plan(conn)
            elif choice == '5':
                conn.close()
                return
            else:
                print("Invalid choice, please try again.\n")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Database Error: Could not process. {sqlstate}\n")
            conn.close()
            return


def add_training_plan(conn):
    """Adds a new training plan."""
    try:
        cursor = conn.cursor()
        name = input("Training Plan Name: ")
        weekly_fee = input("Weekly Fee: ")
        cursor.execute("INSERT INTO TrainingPlans (PlanName, WeeklyFee) VALUES (?, ?)", (name, weekly_fee))
        conn.commit()
        print("Training plan added successfully.\n")
    except pyodbc.Error as ex:
       sqlstate = ex.args[0]
       print(f"Database Error: Could not add training plan. {sqlstate}\n")

def view_training_plans(conn, display):
    """Views all training plans."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM TrainingPlans")
        plans = cursor.fetchall()
        if (display):
            headers = ["ID", "Name", "Weekly Fee"]
            print(tabulate(plans, headers=headers, tablefmt="grid"))
        else:
            for plan in plans:
                print(f'{plan[0]}. {plan[1]}')
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database Error: Could not view training plans. {sqlstate}\n")


def update_training_plan(conn):
     """Updates a training plan's details."""
     try:
        view_training_plans(conn, True)
        plan_id = input("Enter Training Plan ID to update: ")

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM TrainingPlans WHERE TrainingPlanID = ?", (plan_id,))
        plan = cursor.fetchone()
        
        if not plan:
            print("Training Plan not found.\n")
            return
        
        print("\nWhat do you want to update?\n")
        print("1. Name")
        print("2. Weekly Fee")
        print("3. Return to Training Plan Menu")

        update_choice = input("Enter your choice: ")

        if update_choice == '1':
            new_name = input("New Training Plan Name: ")
            cursor.execute("UPDATE TrainingPlans SET PlanName = ? WHERE TrainingPlanID = ?", (new_name, plan_id))
        elif update_choice == '2':
            new_fee = input("New Weekly Fee: ")
            cursor.execute("UPDATE TrainingPlans SET WeeklyFee = ? WHERE TrainingPlanID = ?", (new_fee, plan_id))
        elif update_choice == '3':
            return
        else:
           print("Invalid choice, returning to Training Plan Menu.\n")
           return
        conn.commit()
        print("Training Plan updated successfully.\n")
     except pyodbc.Error as ex:
       sqlstate = ex.args[0]
       print(f"Database Error: Could not update training plan. {sqlstate}\n")


def delete_training_plan(conn):
    """Deletes a training plan."""
    try:
        view_training_plans(conn, True)
        plan_id = input("Enter Training Plan ID to delete: ")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM TrainingPlans WHERE TrainingPlanID = ?", (plan_id,))
        conn.commit()
        print("Training plan deleted successfully.\n")
    except pyodbc.Error as ex:
       sqlstate = ex.args[0]
       print(f"Database Error: Could not delete training plan. {sqlstate}\n")


def manage_competitions(username):
    """Handles competition management."""
    conn = db_connect()
    if conn is None:
        return
    while True:
        print("\nCompetition Management")
        print("----------------------")
        print("1. Add Competition")
        print("2. View Competitions")
        print("3. Add Athletes to Competition")
        print("4. Update Competition")
        print("5. Delete Competition")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                add_competition(conn)
            elif choice == '2':
                view_competitions(conn)
            elif choice == '3':
                add_athletes_to_competition(conn)
            elif choice == '4':
                update_competition(conn)
            elif choice == '5':
                delete_competition(conn)
            elif choice == '6':
                conn.close()
                return
            else:
                print("Invalid choice, please try again.\n")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Database Error: Could not process. {sqlstate}\n")
            conn.close()
            return


def add_competition(conn):
    """Adds a new competition."""
    try:
        cursor = conn.cursor()
        name = input("Competition name: ")
        date_str = input("Competition date (YYYY-MM-DD): ")
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        entry_fee = input("Entry fee: ")
        cursor.execute("INSERT INTO Competitions (CompetitionName, CompetitionDate, EntryFee) VALUES (?, ?, ?)", (name, date, entry_fee))
        conn.commit()
        print("Competition added successfully.\n")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.\n")
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database Error: Could not add competition. {sqlstate}\n")

def view_competitions(conn):
    """Views all competitions."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Competitions")
        competitions = cursor.fetchall()
        headers = ["ID", "Name", "Date", "Entry Fee"]
        print(tabulate(competitions, headers=headers, tablefmt="grid"))
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database Error: Could not view competitions. {sqlstate}\n")

def add_athletes_to_competition(conn):
    """Adds athletes to a competition."""
    try:
        view_competitions(conn)
        competition_id = input("Enter Competition ID: ")
        view_athletes(conn)
        while True:
          athlete_id = input("Enter Athlete ID to add (or type 'done'): ")
          if athlete_id.lower() == 'done':
            break
          
          cursor = conn.cursor()
          cursor.execute("SELECT * FROM Athletes WHERE AthleteID = ?", (athlete_id,))
          athlete = cursor.fetchone()
          if not athlete:
                print(f"Athlete ID:{athlete_id} not found.\n")
                continue
          try:
            cursor.execute("exec AddAthleteToCompetition ?, ?", (competition_id, athlete_id))
            conn.commit()
            print(f"Athlete ID:{athlete_id} added to competition ID:{competition_id}.\n")
          except pyodbc.Error as ex:
              sqlstate = ex.args[0]
              print(f"Database Error: Could not add athlete to competition. {sqlstate}\n")

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database Error: Could not add athletes to competition. {sqlstate}\n")
        
def update_competition(conn):
    """Updates a competition's details."""
    try:
        view_competitions(conn)
        competition_id = input("Enter Competition ID to update: ")

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Competitions WHERE CompetitionID = ?", (competition_id,))
        competition = cursor.fetchone()
        
        if not competition:
            print("Competition not found.\n")
            return
        
        print("\nWhat do you want to update?\n")
        print("1. Name")
        print("2. Date")
        print("3. Entry Fee")
        print("4. Return to Competition Menu")

        update_choice = input("Enter your choice: ")

        if update_choice == '1':
            new_name = input("New Competition Name: ")
            cursor.execute("UPDATE Competitions SET CompetitionName = ? WHERE CompetitionID = ?", (new_name, competition_id))
        elif update_choice == '2':
            new_date_str = input("New Competition Date (YYYY-MM-DD): ")
            new_date = datetime.datetime.strptime(new_date_str, "%Y-%m-%d").date()
            cursor.execute("UPDATE Competitions SET CompetitionDate = ? WHERE CompetitionID = ?", (new_date, competition_id))
        elif update_choice == '3':
            new_fee = input("New Entry Fee: ")
            cursor.execute("UPDATE Competitions SET EntryFee = ? WHERE CompetitionID = ?", (new_fee, competition_id))
        elif update_choice == '4':
            return
        else:
           print("Invalid choice, returning to Competition Menu.\n")
           return
        conn.commit()
        print("Competition updated successfully.\n")
    except ValueError:
         print("Invalid date format. Please use YYYY-MM-DD.\n")
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database Error: Could not update competition. {sqlstate}\n")


def delete_competition(conn):
    """Deletes a competition."""
    try:
        view_competitions(conn)
        competition_id = input("Enter Competition ID to delete: ")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Competitions WHERE CompetitionID = ?", (competition_id,))
        conn.commit()
        print("Competition deleted successfully.\n")
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database Error: Could not delete competition. {sqlstate}\n")


def manage_coaching(username):
    """Handles private coaching management."""
    conn = db_connect()
    if conn is None:
        return
    while True:
        print("\nPrivate Coaching Management")
        print("--------------------------")
        print("1. Add Coaching Hours")
        print("2. View Coaching Hours")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")
        try:
            if choice == '1':
               add_coaching_hours(conn)
            elif choice == '2':
               view_coaching_hours(conn)
            elif choice == '3':
                conn.close()
                return
            else:
                print("Invalid choice, please try again.\n")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Database Error: Could not process. {sqlstate}\n")
            conn.close()
            return


def add_coaching_hours(conn):
    """Adds private coaching hours for an athlete."""
    try:
        view_athletes(conn)
        athlete_id = input("Enter Athlete ID: ")
        hours = input("Enter coaching hours: ")
        date_str = input("Enter date for coaching (YYYY-MM-DD): ")
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO PrivateCoaching (AthleteID, CoachingHours, CoachingDate) VALUES (?, ?, ?)", (athlete_id, hours, date))
        conn.commit()
        print("Coaching hours added successfully.\n")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.\n")
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database Error: Could not add coaching hours. {sqlstate}\n")

def view_coaching_hours(conn):
    """Views all coaching hours for each athlete."""
    try:
        view_athletes(conn)
        athlete_id = input("Enter Athlete ID to view coaching hours: ")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
              C.CoachingID,
              A.AthleteName,
              C.CoachingHours,
              C.CoachingDate
           FROM PrivateCoaching C
           INNER JOIN Athletes A ON A.AthleteID = C.AthleteID
           WHERE C.AthleteID = ?
            """,(athlete_id,))
        coaching_hours = cursor.fetchall()
        headers = ["ID", "Athlete Name", "Coaching Hours", "Date"]
        print(tabulate(coaching_hours, headers=headers, tablefmt="grid"))
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database Error: Could not view coaching hours. {sqlstate}\n")


def generate_reports(username):
    """Handles report generation."""
    conn = db_connect()
    if conn is None:
        return
    while True:
        print("\nReport Generation")
        print("-----------------")
        print("1. Generate Monthly Report for an Athlete")
        print("2. Back to Main Menu")

        choice = input("Enter your choice: ")

        try:
          if choice == '1':
            generate_monthly_report(conn)
          elif choice == '2':
             conn.close()
             return
          else:
             print("Invalid choice, please try again.\n")
        except pyodbc.Error as ex:
          sqlstate = ex.args[0]
          print(f"Database Error: Could not process. {sqlstate}\n")
          conn.close()
          return


def generate_monthly_report(conn):
    """Generates and displays a monthly report for an athlete."""
    try:
      view_athletes(conn)
      athlete_id = input("Enter Athlete ID: ")
      month_str = input("Enter month (YYYY-MM): ")
      report_date = datetime.datetime.strptime(month_str, "%Y-%m").date()
      report_date = report_date.replace(day=1)
      
      cursor = conn.cursor()

      # Fetch athlete details
      cursor.execute("SELECT AthleteName, CurrentWeight, CompetitionWeightCategory FROM Athletes WHERE AthleteID = ?", (athlete_id,))
      athlete_data = cursor.fetchone()
      
      if not athlete_data:
          print("Athlete not found.\n")
          return
      
      athlete_name, current_weight, competition_weight_category = athlete_data
      
      #Fetch training plan
      cursor.execute("SELECT T.PlanName, T.WeeklyFee FROM Athletes A INNER JOIN TrainingPlans T ON A.TrainingPlanID = T.TrainingPlanID WHERE A.AthleteID = ?", (athlete_id,))
      training_plan_data = cursor.fetchone()
      training_plan_name, weekly_fee = training_plan_data
      
      # Calculate training costs (assuming 4 weeks per month)
      training_cost = weekly_fee * 4
      
      #Fetch competitions for the month
      cursor.execute("""
            SELECT 
                C.CompetitionName,
                C.EntryFee
            FROM
                Competitions C
            INNER JOIN
                CompetitionAthletes CA ON C.CompetitionID = CA.CompetitionID
            WHERE 
                CA.AthleteID = ? AND
                YEAR(C.CompetitionDate) = ? AND
                MONTH(C.CompetitionDate) = ?
            """,(athlete_id, report_date.year, report_date.month))
      competitions = cursor.fetchall()
      total_competition_cost = sum(fee for _, fee in competitions)
      
      #Fetch Coaching hours
      cursor.execute("""
         SELECT
            SUM(CoachingHours)
        FROM PrivateCoaching
        WHERE 
            AthleteID = ? AND
            YEAR(CoachingDate) = ? AND
            MONTH(CoachingDate) = ?
        """,(athlete_id, report_date.year, report_date.month))
      coaching_hours = cursor.fetchone()
      coaching_cost = (coaching_hours[0] or 0) * 9.5 #Assuming coaching fee is £9.50
      

      
      total_cost = training_cost + total_competition_cost + coaching_cost

      print(f"\nReport for: {athlete_name}")
      print(f"----------------------------")
      print(f"Training Plan: {training_plan_name}")
      print(f"Training Cost: £{training_cost:.2f}")
      
      if competitions:
        print("\nCompetitions:")
        for name, fee in competitions:
          print(f"- {name}: £{fee:.2f}")
      else:
        print("\nNo Competitions for this Month.")
      
      print(f"Private Coaching Cost: £{coaching_cost:.2f}")
      
      print(f"----------------------------")
      print(f"Total Cost for the Month: £{total_cost:.2f}")
      print(f"Current Weight: {current_weight} kg")
      print(f"Competition Weight Category: {competition_weight_category}")
      
      if float(current_weight) > float(competition_weight_category):
          print(f"Current Weight is above the Competition Weight Category.\n")
      else:
          print(f"Current Weight is within the Competition Weight Category.\n")

    except ValueError:
        print("Invalid date format. Please use YYYY-MM.\n")
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database Error: Could not generate the report. {sqlstate}\n")

def main():
    """Main function."""
    print("Welcome to the North Sussex Judo System!")
    auth_success, username = authenticate_user()

    if not auth_success:
       print("Authentication failed. Exiting.")
       return

    while True:
        main_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            manage_athletes(username)
        elif choice == '2':
           manage_training_plans(username)
        elif choice == '3':
           manage_competitions(username)
        elif choice == '4':
           manage_coaching(username)
        elif choice == '5':
          generate_reports(username)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.\n")


if __name__ == "__main__":
    main()