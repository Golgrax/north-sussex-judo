# PROGRAMMING & DATABASE DESIGN & DEVELOPMENT


# North Sussex Judo System

This repository contains the code and database schema for the North Sussex Judo System, a cost management application designed to track athlete information, training plans, competitions, and private coaching hours.

## Files

### `requirements.txt`

This file lists the Python dependencies required to run the application:

-   `pyodbc`: Used for connecting to a Microsoft SQL Server database.
-   `tabulate`: Used for generating nicely formatted tables for console output.

### `north_sussex_judo.py`

This is the main Python application file. It contains the following functionalities:

1.  **Database Connection:** Connects to the SQL Server database using the provided configuration.
2.  **User Authentication:** Implements a basic username/password authentication system using SHA256 hashing for passwords stored in the `Users` table.
3.  **Main Menu:** Presents a text-based menu system for navigating the application.
4.  **Athlete Management:**
    -   Adds, views, updates, and deletes athletes using CRUD operations on the `Athletes` table.
    -  Links athletes to training plans using foreign key relationships with `TrainingPlans` table.
5.  **Training Plan Management:**
    -   Adds, views, updates, and deletes training plans using CRUD operations on the `TrainingPlans` table.
6.  **Competition Management:**
    -   Adds, views, updates, and deletes competitions using CRUD operations on the `Competitions` table.
    -   Allows adding athletes to a competition using stored procedure `AddAthleteToCompetition`.
    -   Links athletes to competitions using foreign key relationships with `CompetitionAthletes` table.
7.  **Private Coaching Management:**
    -   Adds and views coaching hours for an athlete using CRUD operations on the `PrivateCoaching` table.
    - Links athlete to private coaching using foreign key relationships with `Athletes` table.
8.  **Report Generation:**
    - Generates a monthly report for a specific athlete, calculating training costs, competition fees, and private coaching costs, also advises if the current weight is over the competition weight category.

### `north_sussex_judo.sql`

This SQL file contains the schema for the North Sussex Judo database. It includes the following:

1.  **Database Creation:** Creates the `NorthSussexJudoDB` database.
2.  **Table Creation:**
    -   `Athletes`: Stores information about athletes (ID, name, training plan ID, current weight, competition weight category).
    -   `TrainingPlans`: Stores details about training plans (ID, name, weekly fee).
    -   `Competitions`: Stores information about competitions (ID, name, date, entry fee).
    -   `PrivateCoaching`: Tracks private coaching hours for athletes (ID, athlete ID, hours, date).
    -  `CompetitionAthletes`: Tracks athletes participating in competitions (ID, competition ID, athlete ID)
    -   `Users`: Stores user credentials (ID, username, hashed password).
3.  **Stored Procedure:**
    -  `AddAthleteToCompetition`: adds an athlete to a competition using CompetitionID and AthleteID
4.  **Seed Data:**
    -   Inserts an initial admin user into the `Users` table and 3 different training plan into the `TrainingPlans` table.

## System Analysis with Vocational Scenario
Based on the vocational scenario, here is an analysis of the system:

### User Management
- The system has a basic user authentication system, ensuring that only authorised users can interact with the system. The system uses a username and password and hashes password to ensure that security of user's credentials.
### Core Requirements Fulfillment:
- **Athlete Management:** The system effectively allows for the registration of athletes, including their name, weight, training plan, and competition weight category, which is a core requirement from the brief.
- **Training Plan Management:** The system allows for the addition of different training plans and weekly fees, which can be assigned to athletes.
- **Competition Management:** The system allows the user to add competitions with a name, date, and entry fee. Athletes can be assigned to a competition which covers the transaction to allow submission of interested athletes in batches under the name of the organization.
- **Private Coaching:** The system allows the user to add private coaching hours, allowing an arbitrary number of coaching hours for each athlete subject to the limits of private coaching
- **Reporting:** The system generates monthly reports for athletes, including training costs, competition fees, private coaching cost, and weight comparison. The report also advises if the current weight of the athlete is over the weight category.

### Implementation of CRUD Modules:
- The application uses CRUD operations throughout each module (Athlete, Training Plan, and Competition Management). Each module allows the user to add, view, update and delete records.

### Transactional Processes:
- **Adding Athletes to Competitions:** The system uses a stored procedure (`AddAthleteToCompetition`) to add athletes to competitions, ensuring the correct and efficient link to the CompetitionAthletes table
- **Private Coaching Hours:** The system allows the user to add an arbitrary number of coaching hours for athletes

### Data Validation:
- The system has basic data validation. The SQL database has NOT NULL constraints to ensure each required field is filled in, for example `AthleteName` in `Athletes` table. Additionally date validation has been added when entering the competition date. Further validation could be added to ensure incorrect values are not being inputted by the user. For example the competition date could be compared to the current date to ensure the date is not inputted as a past date.

### Database Design:
-  The database design is normalised and well-structured, with clear primary and foreign keys to maintain referential integrity. Tables are interrelated to ensure data integrity. For example, the `Athletes` table references `TrainingPlans` through the foreign key relationship `TrainingPlanID`, this will ensure that a TrainingPlanID inputted into the Athletes table is a valid training plan.

### Areas of improvement
- Add a user interface for easy navigation. A web based UI could be implemented to allow for easy navigation.
- Ensure data validation is more robust.
- More exception handling could be implemented to prevent the application crashing.

## How to run the application

1.  **Install Dependencies:**
    ```
    pip install -r requirements.txt
    ```
2.  **Set up the database:**
    -   Create a new database on your SQL Server instance named `NorthSussexJudoDB`.
    -   Run the SQL script `north_sussex_judo.sql` on this database.
3.  **Configure the connection parameters:**
    -   In `north_sussex_judo.py`, update the `SERVER`, `DATABASE`, `USERNAME`, and `PASSWORD` variables to match your SQL Server configuration.
4.  **Run the application:**
    ```
    python north_sussex_judo.py
    ```
5.  **Follow the on-screen prompts to interact with the menu system.**

## Further Documentation

Please refer to the code and comments in the python files and SQL script for detailed information about the implementation of the system.
