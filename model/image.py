from google.appengine.ext import ndb


class ImageModel(ndb.Model):
    name = ndb.StringProperty()
    bucket_name = ndb.StringProperty()
    blob_key = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_name(cls, name):
        return cls.query(ImageModel.name == name)
