import webapp2
import json

import lib.cloudstorage as gcs

from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.api import app_identity


BUCKET_NAME = app_identity.get_default_gcs_bucket_name()


class ImageHandler(webapp2.RequestHandler):
    def post(self):
        image = self.request.get('image')
        name = self.request.get('name')

        filename = self.generate_bucket_filename(name)

        with gcs.open(filename, 'w', content_type='image/jpeg') as f:
            f.write(image)

        blobstore_filename = self.generate_blobstore_filename(name)
        blob_key = blobstore.create_gs_key(blobstore_filename)
        restaurant_image_url = images.get_serving_url(blob_key)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            'url': restaurant_image_url,
            'name': name
        }))

    @staticmethod
    def generate_blobstore_filename(name):
        return "/gs{0}".format(ImageHandler.generate_bucket_filename(name))

    @staticmethod
    def generate_bucket_filename(name):
        return "/{0}/{1}".format(BUCKET_NAME, name)

