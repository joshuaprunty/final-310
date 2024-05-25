-- **************************************************************
-- **************************************************************
-- SETUP
CREATE DATABASE IF NOT EXISTS prizepicks;
--
USE prizepicks;
--
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS lines;
-- **************************************************************




-- **************************************************************
-- **************************************************************
-- PLAYERS TABLE
CREATE TABLE players
(
    player_id    int not null AUTO_INCREMENT,
    player_name  varchar(64) not null,
    team_id      int not null,
    player_pos   varchar(64) not null,
    PRIMARY KEY  (player_id),
    UNIQUE       (player_name)
);
-- ID Starting Value
ALTER TABLE players AUTO_INCREMENT = 1001;  -- starting value
-- **************************************************************




-- **************************************************************
-- **************************************************************
-- TEAMS TABLE
CREATE TABLE teams
(
    team_id          int not null AUTO_INCREMENT,
    team_name        varchar(64) not null,
    team_color_code  varchar(64) not null,
    PRIMARY KEY      (team_id),
    UNIQUE           (team_name)
);
-- ID Starting Value
ALTER TABLE teams AUTO_INCREMENT = 1001;  -- starting value
-- **************************************************************




-- **************************************************************
-- **************************************************************
-- GAMES TABLE
CREATE TABLE games
(
    game_id       int not null AUTO_INCREMENT,
    home_id       int not null,
    away_id       int not null,
    pwdhash      varchar(256) not null,
    PRIMARY KEY  (game_id)
);
-- ID Starting Value
ALTER TABLE games AUTO_INCREMENT = 1001;  -- starting value
-- **************************************************************




-- **************************************************************
-- **************************************************************
-- LINES TABLE
CREATE TABLE lines
(
    line_id         int not null AUTO_INCREMENT,
    player_id       int not null,
    stat_type       varchar(64) not null,
    line_value      int not null,
    pwdhash      varchar(256) not null,
    PRIMARY KEY  (line_id),
);
-- ID Starting Value
ALTER TABLE lines AUTO_INCREMENT = 1001;  -- starting value
-- **************************************************************



-- **************************************************************
-- **************************************************************
-- Other
-- creating user accounts for database access:
-- ref: https://dev.mysql.com/doc/refman/8.0/en/create-user.html
DROP USER IF EXISTS 'benfordapp-read-only';
DROP USER IF EXISTS 'benfordapp-read-write';
--
CREATE USER 'benfordapp-read-only' IDENTIFIED BY 'abc123!!';
CREATE USER 'benfordapp-read-write' IDENTIFIED BY 'def456!!';
--
GRANT SELECT, SHOW VIEW ON benfordapp.* 
      TO 'benfordapp-read-only';
GRANT SELECT, SHOW VIEW, INSERT, UPDATE, DELETE, DROP, CREATE, ALTER ON benfordapp.* 
      TO 'benfordapp-read-write';
--  
FLUSH PRIVILEGES;
-- **************************************************************