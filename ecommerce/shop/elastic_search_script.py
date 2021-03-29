from datetime import datetime
from elasticsearch_dsl import Document,Date,Nested,Boolean,analyzer,InnerDoc,Completion,Keyword,Text

class Comment(InnerDoc):
    author=Text(fields={'raw':Keyword()})
class Post(Document):
    title=Text()