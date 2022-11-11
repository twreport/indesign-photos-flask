from api.model.author import Authors, AuthorsSchema


class Other:
    def add(self, sum):
        fetched = Authors.query.get(sum)
        authors_schema = AuthorsSchema()
        authors = authors_schema.dump(fetched)
        return authors

class Ext:
    def add(self, sum):
        fetched = Authors.query.get(sum)
        authors_schema = AuthorsSchema()
        authors = authors_schema.dump(fetched)
        return authors['id']

