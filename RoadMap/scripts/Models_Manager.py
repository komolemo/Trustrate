from django.db import models
from django.db import connection

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class Manager_Base:
    @classmethod
    def get_by_id(cls, table, record_id, columns):
        column_names = ", ".join(columns)
        query = f"SELECT {column_names} FROM {table} WHERE id = %s"

        with cls.connection.cursor() as cursor:
            cursor.execute(query, (record_id,))
            result = cursor.fetchone()
        
        return result if result else None
    
    @classmethod
    def get_all(cls, table, columns):
        """全てのレコードを取得"""
        column_names = ", ".join(columns)
        query = f"SELECT {column_names} FROM {table}"

        with cls.connection.cursor() as cursor:
            cursor.execute(query)
            return dictfetchall(cursor)