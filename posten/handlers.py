from google.appengine.ext import webapp

class GuiHandler(webapp.RequestHandler):
    def get(self):
        # all I do i redirect man
        self.redirect('/static/gui.html')