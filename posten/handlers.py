from django.utils import simplejson as json

from google.appengine.ext import webapp

from posten.helpers import FixtureHelper
from posten.models import Parcel, ParcelEvent

class TrackingHandler(webapp.RequestHandler):
    def get(self):
        pass

class GuiHandler(webapp.RequestHandler):
    def get(self):
        # all I do i redirect man
        self.redirect('/static/gui.html')

class ParcelHandler(webapp.RequestHandler):
    def bad_request(self, message = None):
        self.response.set_status(400)
        if message is not None:
            self.response.out.write(message)

    def not_found(self):
        self.response.set_status(404)
        
    def get(self, parcelId, parcelEventId):
        response_dict = None
        if parcelId is None:
            pq = Parcel.all()
            parcels = pq.fetch(100)
            response_dict = [p.to_dict() for p in parcels]
        else:
            parcel = Parcel.get_by_id(int(parcelId))
            if parcel is None:
                return self.not_found()
            response_dict = parcel.to_dict()
            
            if parcelEventId is None:
                eq = ParcelEvent.all()
                eq.ancestor(parcel)
                events = eq.fetch(100)
                event_dicts = [e.to_dict() for e in events]
                response_dict["events"] = event_dicts
            else:
                event = ParcelEvent.get_by_id(int(parcelEventId), parent=parcel)
                if event is None:
                    return self.not_found()
                response_dict = event.to_dict()
        
        self.response.headers["Content-Type"] =  "application/json; charset=UTF-8"
        self.response.out.write(json.dumps(response_dict))

        
class FixtureHandler(webapp.RequestHandler):
    def get(self):
        f = FixtureHelper()
        f.load()
        self.response.out.write("done")