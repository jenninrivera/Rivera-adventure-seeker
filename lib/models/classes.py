import sqlite3
import ipdb 

CONN = sqlite3.connect('game_results.db')
CURSOR = CONN.cursor()

class Player:

    all = []

    def __init__(self, username):
        self.id = None
        self.username = username
        self.results_list = []

    def __repr__(self):
        repr_string = ""
        repr_string += f'Player: {self.username}'

        if not len(self.results_list) == 0:
            print("Here is this player's results:")
            for result in self.results_list:
                print(result)

        return repr_string

    @classmethod
    def create_table(cls):
        sql = '''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                username TEXT
            )
        '''
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS players
        """
        CURSOR.execute(sql)

    @classmethod
    def player_in_db(cls, row):
        player = cls(row[1])
        player.id = row[0]
        return player
    
    @classmethod
    def get_all(cls):
        sql = '''
            SELECT *
            FROM players
        '''
        
        all = CURSOR.execute(sql).fetchall()
        cls.all = [cls.player_in_db(row) for row in all]
        return cls.all

    @classmethod
    def find_by_id(cls, id):
        players = [player for player in Player.all if player.id == id]

        if players:
            return players[0]
        else:
            return None

    @classmethod
    def create(cls, username):
        player = Player(username)
        player.save()
        cls.all.append(player)
        return player

    def save(self):
        sql = """
            INSERT INTO players (username)
            VALUES (?)
        """

        CURSOR.execute(sql, (self.username,))
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM players").fetchone()[0]
        CONN.commit()

    def delete(self):
        sql = '''
            DELETE FROM players
            WHERE id = ?
        '''

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        Player.all = [player for player in Player.all if player.id != self.id]

        for result in self.results_list:
            if result.player_id == self.id:
                result.delete()
    
    @property
    def username(self):
        return self._username
    @username.setter
    def username(self, username):
        if type(username) == str and len(username) >= 3:
            self._username = username
        else: 
            print('Username can only be letters and must be at least 3 charcaters.')
    
class Result:

    all = []

    def __init__(self, player_id, points):
        self.id = None
        self.points = points
        self.player_id = player_id
        self.player = Player.find_by_id(player_id)
        self.player.results_list.append(self)

    def __repr__(self):
        return f'Result # {self.id}: {self.player.username} has {self.points} points'

    @classmethod
    def create_table(cls):
        sql = '''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY,
                player_id INTEGER,
                points INTEGER
            )
        '''
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS results
        """
        CURSOR.execute(sql)

        cls.all = []

    @classmethod
    def result_in_db(cls, row):
        result = cls(row[1], row[2])
        result.id = row[0]
        return result
    
    @classmethod
    def get_all(cls):
        sql = '''
            SELECT *
            FROM results
        '''
        
        all = CURSOR.execute(sql).fetchall()
        cls.all = [cls.result_in_db(row) for row in all]
        return cls.all

    @classmethod
    def create(cls, player_id, points):
        result = Result(player_id, points)
        result.save()
        cls.all.append(result)
        return result

    def save(self):
        sql = """
            INSERT INTO results (player_id, points)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.player_id, self.points))
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM results").fetchone()[0]
        CONN.commit()

    def delete(self):
        sql = '''
            DELETE FROM results
            WHERE id = ?
        '''

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        Result.all = [result for result in Result.all if result.id != self.id]

        self.player.results_list = [result for result in self.player.results_list if result.id != self.id]

    # def update(self):
    #     sql = '''
    #         UPDATE results
    #         SET player_id = ?, points = ?
    #         WHERE id = ?
    #     '''
    #     CURSOR.execute(sql, (self.player_id, self.points, self.id))
    #     CONN.commit()

    @property
    def player(self):
        return self._player
    @player.setter
    def player(self, player):
        if type(player) == Player:
            self._player = player
        else:
            raise Exception(f'Error: Player {self.player_id} does not exist!')

    @property
    def points(self):
        return self._points
    @points.setter
    def points(self, points):
        if type(points) == int:
            self._points = points