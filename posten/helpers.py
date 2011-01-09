# coding=UTF-8

from datetime import datetime

from posten.models import Parcel, ParcelEvent


class FixtureHelper():
    def load(self):
        p1 = Parcel(
                tracking_number     = "151825825SE",
                customer_name       = "TELIA INFOMEDIA REKLAM AB",
                customer_id         = "3502560000",
                status_code         = 7,
                status_description  = "-",
                service_name        = "Foetagspaket 16.00",
                service_code        = 15,
                receiver_zip        = "85232",
                receiver_city       = "Boras",
                date_sent           = datetime(2010, 04, 05),
                date_delivered      = datetime(2010, 04, 18),
                actual_weight       = "2.7"
            )
        p1.put()
        
        p1_events = [
            {
                "date":         datetime(2010, 04, 05, 20, 00),
                "location":     "Boras",
                "code" :        20,
                "description":  "Inkommet inhamtningsterminal"
            },
            {
                "date":         datetime(2010, 04, 06, 8, 19),
                "location":     "Ange",
                "code" :        22,
                "description":  "Inkommet spridande terminal"
            },
            {
                "date":         datetime(2010, 04, 06, 13, 33),
                "location":     "Sunsdsvall 1",
                "code" :        25,
                "description":  "Summarisk kvittenslista skapad"
            },
            {
                "date":         datetime(2010, 04, 06, 14, 23),
                "location":     "Sunsdsvall lokal",
                "code" :        97,
                "description":  "Kolli ej utlamnat"
            },
            {
                "date":         datetime(2010, 04, 06, 14, 52),
                "location":     "Sunsdsvall lokal",
                "code" :        43,
                "description":  "Aviserat, kvitterat Pk"
            },
            {
                "date":         datetime(2010, 04, 06, 15, 06),
                "location":     "Sunsdsvall 1",
                "code" :        40,
                "description":  "Ankomst postkontor"
            },
            {
                "date":         datetime(2010, 04, 18, 11, 06),
                "location":     "Sunsdsvall 1",
                "code" :        49,
                "description":  "Utlamnat postkontor"
            },
            {
                "date":         datetime(2010, 04, 18, 11, 32),
                "location":     "Sunsdsvall lokal",
                "code" :        31,
                "description":  "Utlamnat mottagare, kollireg"
            },
            {
                "date":         datetime(2010, 04, 25, 11, 52),
                "location":     "System Ange",
                "code" :        30,
                "description":  "Kvittensreg. vid scannerstat."
            },
            {
                "error":        True,
                "date":         datetime(2010, 04, 06, 11, 52),
                "location":     "Sunsdsvall lokal",
                "code" :        802,
                "description":  "Stangt hos mottagare"
            },
        ]
        
        for event in p1_events:
            e = ParcelEvent(parent=p1)
            e.date = event["date"]
            e.location = event["location"]
            e.code = event["code"]
            e.description = event["description"]
            if event.has_key("error"):
                e.error = event["error"]
            e.put()
    
        """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        			<errorevent>
        				<date>20000406</date>
        				<time>1423</time>
        				<location>Sunsdsvall lokal</location>
        				<code>802</code>
        				<description>Stängt hos mottagare</description>
        			</errorevent>
        			<invoicespec>
        				<invoicespecid>16374596</invoicespecid>
        				<invoicespecdate>20000406</invoicespecdate>
        			</invoicespec>
        		</parcel>
        	</body>
        	<footer/>
        </pactrack>
        """