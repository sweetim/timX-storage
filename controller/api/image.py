import webapp2
import json
import logging

import lib.cloudstorage as gcs
from model.image import ImageModel

from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.api import app_identity


BUCKET_NAME = app_identity.get_default_gcs_bucket_name()
DATASTORE_KEY = 'Image'


def generate_bucket_filename(name):
    return "/{0}/{1}".format(BUCKET_NAME, name)


def generate_blobstore_filename(name):
    return "/gs{0}".format(generate_bucket_filename(name))


class BaseImageHandler(webapp2.RequestHandler):
    def handle_exception(self, exception, debug):
        logging.exception(exception)

        if isinstance(exception, gcs.NotFoundError):
            self.generate_error_response(404, 'image not found')

        else:
            self.generate_error_response(500, 'server error')

    def generate_error_response(self, code, message):
        self.response.set_status(code)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            'error': code,
            'message': message
        }))


class ImageHandler(BaseImageHandler):
    def post(self):
        image = self.request.get('image')
        name = self.request.get('name')
        content_type = self.request.POST['image'].type

        bucket_name = generate_bucket_filename(name)

        with gcs.open(bucket_name, 'w', content_type=content_type) as f:
            f.write(image)

        blobstore_filename = generate_blobstore_filename(name)
        blob_key = blobstore.create_gs_key(blobstore_filename)
        restaurant_image_url = images.get_serving_url(blob_key)

        image_model = ImageModel(name=name,
                                 bucket_name=bucket_name,
                                 blob_key=blob_key)
        image_key = image_model.put()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            'url': restaurant_image_url,
            'name': name,
            'mimetype': content_type,
            'id': image_key.id()
        }))


class ImageIDHandler(BaseImageHandler):
    def get(self, image_id):
        image_model = ImageModel.get_by_id(int(image_id))

        filename = image_model.bucket_name
        filestat = gcs.stat(filename)
        image_url = images.get_serving_url(image_model.blob_key)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            'id': image_id,
            'name': image_model.name,
            'size': filestat.st_size,
            'url': image_url,
            'time': str(image_model.date)
        }))

    def delete(self, image_id):
        image_model = ImageModel.get_by_id(int(image_id))
        filename = image_model.bucket_name
        gcs.delete(filename)
        image_model.key.delete()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            'id': image_id
        }))
