from peewee import *

database = MySQLDatabase('sentimentanalysis', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'user': 'root', 'password': 'nurdan'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Ftse(BaseModel):
    cumulative_sentiment = FloatField(index=True, null=True)
    timestamp = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    top_story_sentiment = FloatField(index=True, null=True)
    value = FloatField()

    class Meta:
        table_name = 'ftse'

class Stories(BaseModel):
    content_sentiment = FloatField(index=True, null=True)
    html = TextField()
    is_top_level = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    text_content = TextField(index=True, null=True)
    text_title = TextField(index=True, null=True)
    timestamp = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    title_sentiment = FloatField(null=True)
    url = CharField(index=True)

    class Meta:
        table_name = 'stories'

class Ftselinkstories(BaseModel):
    ftse = ForeignKeyField(column_name='ftse_id', field='id', model=Ftse)
    stories = ForeignKeyField(column_name='stories_id', field='id', model=Stories)

    class Meta:
        table_name = 'ftselinkstories'
        indexes = (
            (('ftse', 'stories'), True),
        )
        primary_key = CompositeKey('ftse', 'stories')

