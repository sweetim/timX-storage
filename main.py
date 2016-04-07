import webapp2


from controller.api import image


app = webapp2.WSGIApplication([
    ('/api/image', image.ImageHandler)
], debug=True)
