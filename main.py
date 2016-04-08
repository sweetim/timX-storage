import webapp2


from controller.api import image


app = webapp2.WSGIApplication([
    ('/api/image', image.ImageHandler),
    webapp2.Route('/api/image/<image_id>', handler=image.ImageIDHandler)
], debug=True)
