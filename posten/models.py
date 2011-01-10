# coding=UTF-8
from datetime import datetime, time, date
import time
import logging

from google.appengine.ext import db

SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

class PostenModel(db.Model):
    def to_dict(self):
        model = self
        output = {}
        for key, prop in model.properties().iteritems():
            value = getattr(model, key)

            if value is None or isinstance(value, SIMPLE_TYPES):
                output[key] = value
            elif isinstance(value, date):
                # Convert date/datetime to ms-since-epoch ("new Date()").
                ms = time.mktime(value.utctimetuple()) * 1000
                ms += getattr(value, 'microseconds', 0) / 1000
                output[key] = int(ms)
            elif isinstance(value, db.Model):
                output[key] = to_dict(value)
            else:
                raise ValueError('cannot encode ' + repr(prop))
        output["id"] = model.key().id()
        return output

    def update_from_dict(self, dict_representation):
        for k, v in dict_representation.iteritems():
            if hasattr(self, k):
                logging.info("%s = %s" % (k,v))
                field_type = type(getattr(self, k))
                logging.info(field_type)
                if field_type == long:
                    v = int(v)
                if field_type == datetime:
                    logging.info(v)
                    v = datetime.fromtimestamp(v/1000) # microseconds in javascript
                    logging.info(v)
                setattr(self, k, v)

class Parcel(PostenModel):
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)

    tracking_number = db.StringProperty(required=True)

    customer_name = db.StringProperty()
    customer_id = db.StringProperty()

    status_code = db.IntegerProperty()
    status_description = db.StringProperty()

    service_name = db.StringProperty()
    service_code = db.IntegerProperty()
    
    receiver_zip = db.StringProperty()
    receiver_city = db.StringProperty()

    date_sent = db.DateTimeProperty()
    date_delivered = db.DateTimeProperty()
    
    actual_weight = db.StringProperty()

class ParcelEvent(PostenModel):
    error = db.BooleanProperty(default=False)
    date = db.DateTimeProperty(default=datetime.utcnow())
    location = db.StringProperty(default="")
    code = db.IntegerProperty(default=1L)
    description = db.StringProperty(default="")
    
