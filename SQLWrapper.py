import sqlite3

class SqlLiteWrapper():

    def __init__(self):
        self.conn = sqlite3.connect('Leaderboard.db')
        self.cur = self.conn.cursor()

        self.cur.execute('''CREATE TABLE IF NOT EXISTS 
                    leaderboard (
                                    user_id TEXT PRIMARY KEY,
                                    current_score INTEGER,
                                    questions_answered_correctly INTEGER,
                                    questions_answered_incorrectly INTEGER
                                )
                        ''')

    
    def user_exists_in_leaderboard(self, user_id: str) -> None:
        self.cur.execute("SELECT * FROM leaderboard where user_id = ?", (user_id,))

        if self.cur.fetchone():
            return True 
        else:
            return False


    def add_user_to_leaderboard(self, user_id: str) -> None:
        self.cur.execute("INSERT INTO leaderboard VALUES (?,?,?,?)", (user_id, 0, 0, 0))
        self.conn.commit()


    def add_user_if_doesnt_exist(self, user_id: str) -> None:
        if not self.user_exists_in_leaderboard(user_id):
            self.add_user_to_leaderboard(user_id)


    def get_current_score(self, user_id: str) -> int:
        self.cur.execute("SELECT current_score FROM leaderboard WHERE user_id = ?", (user_id,))

        return self.cur.fetchone()[0]


    def increment_game_score(self, user_id: str, score_increment: int) -> None:
        self.add_user_if_doesnt_exist(user_id)

        old_score = self.get_current_score(user_id)
        new_score = old_score + score_increment

        self.cur.execute("UPDATE leaderboard SET current_score = ? WHERE user_id = ?", (new_score, user_id))
        self.conn.commit()


    def get_questions_answered_correctly(self, user_id: str) -> int:
        self.cur.execute("SELECT questions_answered_correctly FROM leaderboard WHERE user_id = ?", (user_id,))

        return self.cur.fetchone()[0]


    def increment_questions_correct(self, user_id: str) -> None:
        self.add_user_if_doesnt_exist(user_id)

        new_questions_correct = self.get_questions_answered_correctly(user_id) + 1

        self.cur.execute("UPDATE leaderboard SET questions_answered_correctly = ? WHERE user_id = ?", (new_questions_correct, user_id))
        self.conn.commit()


    def get_questions_answered_incorrectly(self, user_id: str) -> int:
        self.cur.execute("SELECT questions_answered_incorrectly FROM leaderboard WHERE user_id = ?", (user_id,))

        return self.cur.fetchone()[0]


    def increment_questions_incorrect(self, user_id: str) -> None:
        self.add_user_if_doesnt_exist(user_id)

        new_questions_incorrect = self.get_questions_answered_correctly(user_id) + 1

        self.cur.execute("UPDATE leaderboard SET questions_answered_incorrectly = ? WHERE user_id = ?", (new_questions_incorrect, user_id))
        self.conn.commit()

    