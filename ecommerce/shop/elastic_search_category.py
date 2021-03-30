from elasticsearch_dsl import Document,Text,connections,Keyword
class Category(Document):
    category=Text(fields={"keyword":Keyword()})
    class Index:
        name="ecommerce_category_using_python"
    def save(self,**kwargs):
        return super().save(**kwargs)
connections.create_connection()
if not Category._index.exists():
    Category.init()

