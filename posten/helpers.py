# coding=UTF-8
from datetime import datetime
from xml.etree import cElementTree as etree

from posten.models import Parcel, ParcelEvent

class ParcelHelper():
    
    def _parcel_root_and_body(self):
        root_element = etree.Element("pactrack", {
            "version": "1.0",
            "date": datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z%z %Y"),
            "size": "0",
            "lang": "SE"
        })

        header_element = etree.SubElement(root_element, "header")
        etree.SubElement(header_element, "noofparcelentries").text = "1"
        etree.SubElement(header_element, "noofuniqueparcels").text = "1"

        body_element = etree.SubElement(root_element, "body")

        return (root_element, body_element)
    
    def tracking_number_error_as_xml(self):
        # yeah, because they couldn't just use Bad Request...
        (root_element, body_element) = self._parcel_root_and_body()
        etree.SubElement(body_element, "programevent", {"level": "4"}).text = "Kolliid maste vara minst 9 tecken"
        return etree.tostring(root_element, encoding="ISO-8859-1")
    
    def no_parcel_as_xml(self, tracking_number):
        return self.parcel_as_xml(tracking_number)
        
    def parcel_as_xml(self, tracking_number, parcel=None, events=[]):
        (root_element, body_element) = self._parcel_root_and_body()
        
        parcel_element = etree.SubElement(body_element, "parcel", {"id":tracking_number})
        
        etree.SubElement(parcel_element, "customerref")
        
        if parcel is not None:
            etree.SubElement(parcel_element, "internalstatus").text = "1"
        
            etree.SubElement(parcel_element, "customerno").text = parcel.customer_id
            etree.SubElement(parcel_element, "customername").text = parcel.customer_name
        
            etree.SubElement(parcel_element, "statuscode").text = str(parcel.status_code)
            etree.SubElement(parcel_element, "statusdescription").text = parcel.status_description
            etree.SubElement(parcel_element, "servicecode").text = str(parcel.service_code)
            etree.SubElement(parcel_element, "servicename").text = parcel.service_name
            etree.SubElement(parcel_element, "receiverzipcode").text = parcel.receiver_zip
            etree.SubElement(parcel_element, "receivercity").text = parcel.receiver_city
        
            etree.SubElement(parcel_element, "datesent").text = parcel.date_sent.strftime("%Y%m%d")
            etree.SubElement(parcel_element, "datedelivered").text = parcel.date_delivered.strftime("%Y%m%d")
            etree.SubElement(parcel_element, "actualweight").text = parcel.actual_weight

            for event in events:
                event_element = etree.SubElement(
                        parcel_element, 
                        "event" if event.error is not True else "errorevent"
                    )
                etree.SubElement(event_element, "date").text = event.date.strftime("%Y%m%d")
                etree.SubElement(event_element, "time").text = event.date.strftime("%H%M")
                etree.SubElement(event_element, "location").text = event.location
                etree.SubElement(event_element, "code").text = str(event.code)
                etree.SubElement(event_element, "description").text = event.description

            invoicespec_element = etree.SubElement(parcel_element, "invoicespec")
            etree.SubElement(invoicespec_element, "invoicespecid").text = "0"
            etree.SubElement(invoicespec_element, "invoicespecdate").text = "20000101"
        else:
            etree.SubElement(parcel_element, "internalstatus").text = "0"
            
        return etree.tostring(root_element, encoding="ISO-8859-1")

    def posten_xml(self):
        return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <pactrack version="1.0" date="Fri Apr 28 11:10:48 GMT+02:00 2000" size="2652" lang="SE">
        	<header>
        		<noofparcelentries>1</noofparcelentries>
        		<noofuniqueparcels>1</noofuniqueparcels>
        	</header>
        	<body>
        		<parcel id="11131739625SE">
        			<customerref/>
        			<internalstatus>1</internalstatus>
        			<customerno>3502560000</customerno>
        			<customername>TELIA INFOMEDIA REKLAM AB</customername>
        			<statuscode>7</statuscode>
        			<statusdescription>-</statusdescription>
        			<servicecode>15</servicecode>
        			<servicename>Företagspaket 16.00</servicename>
        			<receiverzipcode>85232</receiverzipcode>
        			<receivercity>SUNDSVALL</receivercity>
        			<datesent>20000405</datesent>
        			<datedelivered>20000418</datedelivered>
        			<actualweight>2.7</actualweight>
        			<event>
        				<date>20000405</date>
        				<time>2000</time>
        				<location>Borås</location>
        				<code>20</code>
        				<description>Inkommet inhämtningsterminal</description>
        			</event>
        			<event>
        				<date>20000406</date>
        				<time>0819</time>
        				<location>Ånge</location>
        				<code>22</code>
        				<description>Inkommet spridande terminal</description>
        			</event>
        			<event>
        				<date>20000406</date>
        				<time>1333</time>
        				<location>Sunsdsvall lokal</location>
        				<code>25</code>
        				<description>Summarisk kvittenslista skapad</description>
        			</event>
        			<event>
        				<date>20000406</date>
        				<time>1423</time>
        				<location>Sunsdsvall lokal</location>
        				<code>97</code>
        				<description>Kolli ej utlämnat</description>
        			</event>
        			<event>
        				<date>20000406</date>
        				<time>1452</time>
        				<location>Sunsdsvall lokal</location>
        				<code>43</code>
        				<description>Aviserat, kvitterat Pk</description>
        			</event>
        			<event>
        				<date>20000406</date>
        				<time>1506</time>
        				<location>Sundsvall 1</location>
        				<code>40</code>
        				<description>Ankomst postkontor</description>
        			</event>
        			<event>
        				<date>20000418</date>
        				<time>1106</time>
        				<location>Sundsvall 1</location>
        				<code>49</code>
        				<description>Utlämnat postkontor</description>
        			</event>
        			<event>
        				<date>20000418</date>
        				<time>1132</time>
        				<location>Sunsdsvall lokal</location>
        				<code>31</code>
        				<description>Utlämnat mottagare, kollireg</description>
        			</event>
        			<event>
        				<date>20000425</date>
        				<time>1152</time>
        				<location>System Ånge</location>
        				<code>30</code>
        				<description>Kvittensreg. vid scannerstat.</description>
        			</event>
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