from django.db import connection

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class ReviewManager:
    @classmethod
    def get_random_reviews(cls, limit=10):
        with connection.cursor() as cursor:
            # cursor.execute(f"""
            #     SELECT *
            #     FROM reviews
            #     ORDER BY RANDOM()
            #     LIMIT %s
            # """, [limit])
            cursor.execute(f"""
                SELECT r.*, tp.name AS training_program_name
                FROM reviews r
                INNER JOIN training_programs tp
                    ON r.training_program_id = tp.id
                ORDER BY RANDOM()
                LIMIT %s
            """, [limit])
            return dictfetchall(cursor)
        
    @classmethod
    def get_random_reviews_by_industry(cls, industry_id, limit=10):
        with connection.cursor() as cursor:
            # cursor.execute("""
            #     SELECT r.*
            #     FROM reviews r
            #     INNER JOIN users u ON r.user_account_id = u.id
            #     WHERE u.industory_id = %s
            #     ORDER BY RANDOM()
            #     LIMIT %s
            # """, [industry_id, limit])
            cursor.execute("""
                SELECT r.*, tp.name AS training_program_name
                FROM reviews r
                INNER JOIN users u ON r.user_account_id = u.id
                INNER JOIN training_programs tp ON r.training_program_id = tp.id
                WHERE u.industory_id = %s
                ORDER BY RANDOM()
                LIMIT %s
            """, [industry_id, limit])
            return dictfetchall(cursor)


class TrainingProgramManager:
    @classmethod
    def get_all_programs(cls):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, description
                FROM training_programs
                ORDER BY id
            """)
            return dictfetchall(cursor)

    @classmethod
    def get_program_by_id(cls, program_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, description
                FROM training_programs
                WHERE id = %s
            """, [program_id])
            result = dictfetchall(cursor)
            return result[0] if result else None

    @classmethod
    def get_program_with_averages(cls, program_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    tp.id, tp.name,
                    AVG(r.overall_rating) AS avg_overall_rating,
                    AVG(r.contents_rating) AS avg_contents_rating,
                    AVG(r.lecturer_rating) AS avg_lecturer_rating,
                    AVG(r.cost_performance_rating) AS avg_cost_performance_rating,
                    AVG(r.practicality_rating) AS avg_practicality_rating,
                    AVG(r.ease_of_understanding_rating) AS avg_ease_of_understanding_rating
                FROM training_programs tp
                LEFT JOIN reviews r ON tp.id = r.training_program_id
                WHERE tp.id = %s
                GROUP BY tp.id
            """, [program_id])
            result = dictfetchall(cursor)
            return result[0] if result else None

    # @classmethod
    # def get_reviews_for_program(cls, program_id, limit=10):
    #     with connection.cursor() as cursor:
    #         cursor.execute("""
    #             SELECT 
    #                 overall_rating, contents_rating, lecturer_rating,
    #                 cost_performance_rating, practicality_rating, ease_of_understanding_rating,
    #                 comment_summary, pros, cons, created_at
    #             FROM reviews
    #             WHERE training_program_id = %s
    #             ORDER BY RANDOM()
    #             LIMIT %s
    #         """, [program_id, limit])
    #         return dictfetchall(cursor)

    @classmethod
    def get_reviews_for_program(cls, program_id, industory_id=0, limit=10):
        with connection.cursor() as cursor:
            if industory_id == 0:
                # 業種フィルタなし
                cursor.execute("""
                    SELECT 
                        overall_rating, contents_rating, lecturer_rating,
                        cost_performance_rating, practicality_rating, ease_of_understanding_rating,
                        comment_summary, pros, cons, created_at
                    FROM reviews
                    WHERE training_program_id = %s
                    ORDER BY RANDOM()
                    LIMIT %s
                """, [program_id, limit])
            else:
                # usersテーブルとJOINして業種で絞り込み
                cursor.execute("""
                    SELECT 
                        r.overall_rating, r.contents_rating, r.lecturer_rating,
                        r.cost_performance_rating, r.practicality_rating, r.ease_of_understanding_rating,
                        r.comment_summary, r.pros, r.cons, r.created_at
                    FROM reviews r
                    INNER JOIN users u ON r.user_account_id = u.id
                    WHERE r.training_program_id = %s AND u.industory_id = %s
                    ORDER BY RANDOM()
                    LIMIT %s
                """, [program_id, industory_id, limit])

            return dictfetchall(cursor)
    
    @classmethod
    def get_all_industories(cls):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name FROM industories ORDER BY id
            """)
            return dictfetchall(cursor)



