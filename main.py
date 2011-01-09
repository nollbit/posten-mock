from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from posten.handlers import GuiHandler

def main():
    application = webapp.WSGIApplication([('/', GuiHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
