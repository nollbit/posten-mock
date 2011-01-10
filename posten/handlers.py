import logging
from datetime import datetime

from django.utils import simplejson as json

from google.appengine.ext import webapp
from django.utils import simplejson as json

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
            self.response.headers["Content-Type"] =  "text/plain; charset=UTF-8"
            self.response.out.write(message)

    def not_found(self):
        self.response.set_status(404)

    def no_content(self):
        self.response.set_status(204)
        
    def get(self, parcel_id, parcel_event_id):
        response_dict = None
        if parcel_id is None:
            # show all parcels, sans events
            pq = Parcel.all()
            parcels = pq.fetch(100)
            response_dict = [p.to_dict() for p in parcels]
        else:
            # show single parcel, with events
            # unless event id set,
            # in that case, just return the event
            parcel = Parcel.get_by_id(int(parcel_id))
            if parcel is None:
                return self.not_found()
            response_dict = parcel.to_dict()
            
            if parcel_event_id is None:
                eq = ParcelEvent.all()
                eq.ancestor(parcel)
                eq.order("date")
                events = eq.fetch(100)
                event_dicts = [e.to_dict() for e in events]
                response_dict["events"] = event_dicts
            else:
                event = ParcelEvent.get_by_id(int(parcel_event_id), parent=parcel)
                if event is None:
                    return self.not_found()
                response_dict = event.to_dict()
        
        self.response.headers["Content-Type"] =  "application/json; charset=UTF-8"
        self.response.out.write(json.dumps(response_dict))

    def put(self, parcel_id, parcel_event_id):
        try:
            data = json.load(self.request.body_file)
        except Exception, e:
            self.write_error(400, 1000, "Invalid body (should be json parcel)")
            return

        if parcel_id is None:
            return self.not_found()
            
        parcel = Parcel.get_by_id(int(parcel_id))
        if parcel is None:
            return self.not_found()
        
        if parcel_event_id is None:
            parcel.update_from_dict(data)
            parcel.put()
        else:
            #no update support for parcel events
            pass
        
        return self.no_content()

    def delete(self, parcel_id, parcel_event_id):
        if parcel_id is None:
            return self.not_found()

        parcel = Parcel.get_by_id(int(parcel_id))
        if parcel is None:
            return self.not_found()

        if parcel_event_id is None:
            parcel.delete()
        else:
            parcelEvent = ParcelEvent.get_by_id(int(parcel_event_id), parent=parcel)
            if parcelEvent is None:
                return self.not_found()
                
            parcelEvent.delete()

        return self.no_content()

        
class FixtureHandler(webapp.RequestHandler):
    def get(self):
        # just add a single parcel with events
        FixtureHelper().load()
        self.response.out.write("done")