-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (player_id serial PRIMARY KEY,
					  player_name text NOT NULL);

CREATE TABLE games (game_id int PRIMARY KEY,
				    round_id int,
				    winner_id serial FOREIGN KEY REFERENCES players(player_id),
				    loser_id serial FOREIGN KEY REFERENCES players(player_id));
