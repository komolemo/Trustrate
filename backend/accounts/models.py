from django.db import connection

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class UserManager:
    @classmethod
    def create_user(cls, username, hashed_password, industory_id, email):   
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (username, email, industory_id, password)
                VALUES (%s, %s, %s, %s)
            """, [username, hashed_password, industory_id, email])
            return True


    @classmethod
    def get_user_by_username(cls, username):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, username, email, industory_id, password
                FROM users
                WHERE username = %s
            """, [username])
            results = dictfetchall(cursor)
            return results[0] if results else None