#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM games;")
    conn.commit() 
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players;")
    conn.commit() 
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM players;")
    results = c.fetchall()
    conn.close()
    return results[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (player_name) VALUES (name);")
    conn.commit() 
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT players.player_id, players.player_name, "
              "COUNT((SELECT games.winner_id from games where games.winner_id = players.player_id)) as win, "
              "COUNT((SELECT games.loser_id from games where games.loser_id = players.player_id)) as loss, "
              "COUNT(games.winner_id) as games"
              "from players left join games on"
              "players.players_id = games.winner_id or players.player_id = games.loser_id"
              "GROUP BY players.id"
              "ORDER BY win;")
    results = c.fetchall()
    conn.close()
    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO games (winner_id, loser_id) VALUES (winner, loser);")
    conn.commit() 
    conn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()
    c.execute("CREATE view state as "
              "SELECT players.player_id as id, players.player_name, "
              "COUNT((SELECT games.winner_id FROM games WHERE games.winner_id = players.player_id)) as win, "
              "COUNT(games.winner_id) as games "
              "FROM players LEFT JOIN games ON players.player_id= games.winner_id or players.player_id = games.loser_id  "
              "GROUP BY players.player_id")
    conn.commit()
    c.execute("SELECT state_a.id, state_a.name, state_b.id, state_b.name "
              "FROM state as state_a, state as state_b "
              "WHERE state_a.win = state_b.win AND state_a.id > state_b.id")
    results = c.fetchall()
    c.execute("DROP VIEW state")
    conn.commit() 
    conn.close()
    return results

