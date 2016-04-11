import webapp2
import os

from controller.api import image


debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

app = webapp2.WSGIApplication([
    ('/api/image', image.ImageHandler),
    webapp2.Route('/api/image/<image_id>', handler=image.ImageIDHandler)
], debug=debug)
