-- north_sussex_judo.sql

-- Create Database
CREATE DATABASE NorthSussexJudoDB;
GO

USE NorthSussexJudoDB;
GO

-- Create Tables
-- Example Athlete Table
CREATE TABLE Athletes (
    AthleteID INT PRIMARY KEY IDENTITY(1,1),
    AthleteName VARCHAR(255) NOT NULL,
    TrainingPlanID INT,
    CurrentWeight DECIMAL(5,2),
    CompetitionWeightCategory VARCHAR(50)
);
GO
--Example TrainingPlan Table
CREATE TABLE TrainingPlans (
    TrainingPlanID INT PRIMARY KEY IDENTITY(1,1),
    PlanName VARCHAR(50) NOT NULL,
    WeeklyFee DECIMAL(10,2) NOT NULL
    );
GO
        
--Example Competitions table
CREATE TABLE Competitions (
    CompetitionID INT PRIMARY KEY IDENTITY(1,1),
    CompetitionName VARCHAR(255) NOT NULL,
    CompetitionDate DATE NOT NULL,
    EntryFee DECIMAL(10,2) NOT NULL
);
GO

--Example PrivateCoaching table
CREATE TABLE PrivateCoaching (
    CoachingID INT PRIMARY KEY IDENTITY(1,1),
    AthleteID INT,
    CoachingHours INT,
    CoachingDate DATE,
    FOREIGN KEY(AthleteID) REFERENCES Athletes(AthleteID)
);
GO
--Example CompetitionAthletes table
CREATE TABLE CompetitionAthletes(
    CompetitionAthleteID INT PRIMARY KEY IDENTITY(1,1),
    CompetitionID INT,
    AthleteID INT,
    FOREIGN KEY (CompetitionID) REFERENCES Competitions(CompetitionID),
    FOREIGN KEY (AthleteID) REFERENCES Athletes(AthleteID)
);
GO
    
--Example User table
CREATE TABLE Users(
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Username VARCHAR(50) NOT NULL,
    Password VARCHAR(255) NOT NULL
);
GO

--Stored Procedure for addind an athlete to a competition
CREATE PROCEDURE AddAthleteToCompetition (
    @CompetitionID INT,
    @AthleteID INT
)
AS
BEGIN
    INSERT INTO CompetitionAthletes (CompetitionID, AthleteID)
    VALUES (@CompetitionID, @AthleteID)
END
GO

-- Seed Data for User Table
INSERT INTO Users (Username, Password) VALUES
('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918');
GO

-- Seed Data for TrainingPlans
INSERT INTO TrainingPlans (PlanName, WeeklyFee) VALUES
('Beginner', 25.00),
('Intermediate', 30.00),
('Elite', 35.00);
GO