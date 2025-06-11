from django.db import models
from django.db import connection
from ..scripts.Models_Manager import Manager_Base

# Create your models here.
class carriculumManager(Manager_Base):
    def __init__(self):
        super.__init__()

    @classmethod
    def get_all_carriculums(cls, table):
        """全てのホテルを取得"""
        colums = ['id', 'name', 'category_id']
        return cls.get_all(table, colums)