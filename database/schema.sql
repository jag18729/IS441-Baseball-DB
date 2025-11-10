-- IS441 Baseball Database Project
-- SQL DDL Script for Microsoft Access
-- Creates 7 tables for MLB player scouting database
-- Date: November 8, 2025

-- ============================================
-- Table 1: Conference (League)
-- ============================================
CREATE TABLE Conference (
    Conference_ID INT PRIMARY KEY,
    Conference_Name VARCHAR(50) NOT NULL UNIQUE,
    Description VARCHAR(255)
);

-- ============================================
-- Table 2: Division
-- ============================================
CREATE TABLE Division (
    Division_ID INT PRIMARY KEY,
    Division_Name VARCHAR(50) NOT NULL,
    Conference_ID INT NOT NULL,
    FOREIGN KEY (Conference_ID) REFERENCES Conference(Conference_ID)
);

-- ============================================
-- Table 3: Team
-- ============================================
CREATE TABLE Team (
    Team_ID INT PRIMARY KEY,
    Team_Name VARCHAR(100) NOT NULL,
    Team_Location VARCHAR(100) NOT NULL,
    Team_Abbreviation VARCHAR(5) NOT NULL UNIQUE,
    Division_ID INT NOT NULL,
    FOREIGN KEY (Division_ID) REFERENCES Division(Division_ID)
);

-- ============================================
-- Table 4: Position
-- ============================================
CREATE TABLE Position (
    Position_ID INT PRIMARY KEY,
    Position_Name VARCHAR(50) NOT NULL UNIQUE,
    Position_Type VARCHAR(20) NOT NULL
);

-- Add constraint for Position_Type (Pitcher or Fielder only)
ALTER TABLE Position ADD CONSTRAINT CHK_Position_Type
    CHECK (Position_Type IN ('Pitcher', 'Fielder'));

-- ============================================
-- Table 5: Player
-- ============================================
CREATE TABLE Player (
    Player_ID INT PRIMARY KEY,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    Full_Name VARCHAR(100) NOT NULL,
    Jersey_Number VARCHAR(5),
    Date_of_Birth DATE,
    Birth_Place VARCHAR(100),
    Height VARCHAR(20),
    Weight VARCHAR(20),
    Bats_Throws VARCHAR(20),
    College VARCHAR(100),
    Debut_Year INT,
    Active_Status BIT NOT NULL DEFAULT 1,
    Draft_Info VARCHAR(100),
    Team_ID INT NOT NULL,
    Position_ID INT NOT NULL,
    FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID),
    FOREIGN KEY (Position_ID) REFERENCES Position(Position_ID)
);

-- ============================================
-- Table 6: Game
-- ============================================
CREATE TABLE Game (
    Game_ID INT PRIMARY KEY,
    Game_Date DATETIME NOT NULL,
    Season INT NOT NULL,
    Home_Team_ID INT NOT NULL,
    Away_Team_ID INT NOT NULL,
    Venue VARCHAR(100),
    Attendance INT,
    Postseason_Flag BIT NOT NULL DEFAULT 0,
    Game_Status VARCHAR(50),
    FOREIGN KEY (Home_Team_ID) REFERENCES Team(Team_ID),
    FOREIGN KEY (Away_Team_ID) REFERENCES Team(Team_ID),
    CHECK (Home_Team_ID <> Away_Team_ID)
);

-- ============================================
-- Table 7: Game_Statistics
-- ============================================
CREATE TABLE Game_Statistics (
    Game_Stats_ID INT IDENTITY(1,1) PRIMARY KEY,
    Game_ID INT NOT NULL,
    Team_ID INT NOT NULL,
    Is_Home_Team BIT NOT NULL,
    Runs INT NOT NULL CHECK (Runs >= 0),
    Hits INT NOT NULL CHECK (Hits >= 0),
    Errors INT NOT NULL CHECK (Errors >= 0),
    Inning_Scores TEXT,
    FOREIGN KEY (Game_ID) REFERENCES Game(Game_ID),
    FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID)
);

-- ============================================
-- Indexes for Performance
-- ============================================

-- Player table indexes
CREATE INDEX IDX_Player_Team ON Player(Team_ID);
CREATE INDEX IDX_Player_Position ON Player(Position_ID);
CREATE INDEX IDX_Player_Active ON Player(Active_Status);
CREATE INDEX IDX_Player_Name ON Player(Last_Name, First_Name);

-- Game table indexes
CREATE INDEX IDX_Game_Season ON Game(Season);
CREATE INDEX IDX_Game_Date ON Game(Game_Date);
CREATE INDEX IDX_Game_Home_Team ON Game(Home_Team_ID);
CREATE INDEX IDX_Game_Away_Team ON Game(Away_Team_ID);

-- Game_Statistics table indexes
CREATE INDEX IDX_GameStats_Game ON Game_Statistics(Game_ID);
CREATE INDEX IDX_GameStats_Team ON Game_Statistics(Team_ID);

-- ============================================
-- Sample Static Data (Conferences & Divisions)
-- ============================================

-- Insert Conferences
INSERT INTO Conference (Conference_ID, Conference_Name, Description) VALUES
(1, 'American League', 'American League (AL) - Designated Hitter rule'),
(2, 'National League', 'National League (NL) - Pitchers must bat');

-- Insert Divisions
INSERT INTO Division (Division_ID, Division_Name, Conference_ID) VALUES
(1, 'East', 1),      -- AL East
(2, 'Central', 1),   -- AL Central
(3, 'West', 1),      -- AL West
(4, 'East', 2),      -- NL East
(5, 'Central', 2),   -- NL Central
(6, 'West', 2);      -- NL West

-- ============================================
-- Sample Position Data
-- ============================================

INSERT INTO Position (Position_ID, Position_Name, Position_Type) VALUES
-- Pitchers
(1, 'Starting Pitcher', 'Pitcher'),
(2, 'Relief Pitcher', 'Pitcher'),
(3, 'Closer', 'Pitcher'),

-- Infielders
(4, 'Catcher', 'Fielder'),
(5, 'First Baseman', 'Fielder'),
(6, 'Second Baseman', 'Fielder'),
(7, 'Third Baseman', 'Fielder'),
(8, 'Shortstop', 'Fielder'),

-- Outfielders
(9, 'Left Fielder', 'Fielder'),
(10, 'Center Fielder', 'Fielder'),
(11, 'Right Fielder', 'Fielder'),

-- Utility
(12, 'Designated Hitter', 'Fielder'),
(13, 'Utility Player', 'Fielder');

-- ============================================
-- Comments / Notes
-- ============================================

-- Data Sources:
-- 1. Conference & Division: Static MLB structure
-- 2. Position: Standard MLB positions
-- 3. Team: Loaded from Ball Don't Lie API /teams endpoint
-- 4. Player: Loaded from Ball Don't Lie API /players endpoint
-- 5. Game: Loaded from Ball Don't Lie API /games endpoint (season=2024)
-- 6. Game_Statistics: Derived from Game API data (home_team_data, away_team_data)

-- Data Import Order:
-- 1. Conference (already inserted above)
-- 2. Division (already inserted above)
-- 3. Position (already inserted above)
-- 4. Team (from API CSV)
-- 5. Player (from API CSV)
-- 6. Game (from API CSV)
-- 7. Game_Statistics (from API CSV)

-- Referential Integrity:
-- All foreign keys enforce relationships
-- Cascade delete is NOT enabled to preserve historical data
-- Updates should be done carefully to maintain data integrity

-- ============================================
-- End of DDL Script
-- ============================================
