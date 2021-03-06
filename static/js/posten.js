var pm = {
    parcels : [],
    parcelFormFields : [
        {name: "id", type: "display"},
        {name: "tracking_number", type:  "string"},
        {name: "customer_name", type:  "string"},
        {name: "customer_id", type:  "string"},
        {name: "status_code", type:  "int"},
        {name: "status_description", type:  "string"},
        {name: "service_name", type:  "string"},
        {name: "service_code", type:  "int"},
        {name: "receiver_zip", type:  "string"},
        {name: "receiver_city", type:  "string"},
        {name: "date_sent", type:  "date"},
        {name: "date_delivered", type:  "date"},
        {name: "actual_weight", type:  "string"},
    ],
    currentParcel : null,
    init : function() {
        $(document).ajaxError(function(e, r, ajaxOptions, thrownError){
            $("#error").empty();
            console.log(e);
            error = {
                request : r,
                options : ajaxOptions,
            }
            console.log(error);
            $("#errorTemplate").tmpl(error).appendTo("#error");
            
        });
        // set up "set to now" buttons for date and datetime input fields
        $(".set-to-now").live("click", function(e){
            /*
            parent should be a label pointing to an input field
            of type "date" or "datetime"
            */
            label = $(this).parent();
            labelFor = label.attr("for");
            
            input = $("#" + labelFor);
            
            console.log(input.attr("type"));
            d = new Date();
            if (input.attr("type") == "date") {
                input.val(pm.getNiceDate());
            } else if (input.attr("type") == "datetime") {
                input.val(pm.getNiceDateTime());
            }
            e.stopPropagation();
            return false;
        });
        
        $("#randomize-tracking-number").click(function(e){
            e.stopPropagation();
            randomTrackingNumber = pm.generateRandomTrackingNumber();
            $("#add-tracking-number").val(randomTrackingNumber);
            return false;
        });
        
        $("#add-parcel-button").click(function(e){
            e.stopPropagation();
            trackingNumber = $("#add-tracking-number").val();
            if (trackingNumber.length < 10) return false;
            parcelSkeleton = {
                "tracking_number": trackingNumber
            }
            pm.addParcel(parcelSkeleton);
            return false;
        });
        pm.loadParcels();
    },
    generateRandomTrackingNumber : function() {
        numberPart = "";
        for(var i=0; i<10; i++) {
            numberPart += Math.floor(Math.random() * 10)
        }
        return numberPart + "SE";
    },
    loadParcels : function() {
        console.log("loading");
        $.getJSON("/parcels", function(response){
            console.log(response);
            pm.parcels = response;
            pm.updateParcelList();
        });
    },
    updateParcelList : function(){
        $("#parcels").empty();
        $("#parcelListItemTemplate").tmpl(pm.parcels).appendTo("#parcels");
        $("#parcels li:last").addClass("selected");
        $("#parcels a.tracking-number").click(function(e){
            pm.selectParcel($(this));
        });
        pm.selectParcel($("#parcels li:last a"));
    },
    showParcelInfoLoader : function() {
        $("#parcel-events").hide();
        $("#parcel-form").hide();
        $("#info-loader").show();  
    },
    hideParcelInfoLoader : function() {
        $("#info-loader").hide();  
        $("#parcel-events").show();
        $("#parcel-form").show();
    },
    selectParcel : function(parcelLinkElement) {
        pm.showParcelInfoLoader();
        $("#parcels li.selected").removeClass("selected");
        parcelLinkElement.parent().addClass("selected");
        
        parcelPath = parcelLinkElement.attr("href").slice(2);
        console.log(parcelPath);
        pm.loadParcelData(parcelPath);
    },
    loadParcelData : function(parcelPath, eventsOnly) {
        if (eventsOnly == undefined) {
            eventsOnly = false
        }
        $.getJSON(parcelPath, function(response){
            console.log(response);
            pm.currentParcel = response;
            pm.parcelDataUpdated(eventsOnly);
        });
    },
    parcelDataUpdated : function(eventsOnly) {
        pm.hideParcelInfoLoader();
        parcelForm = {
            fields: pm.parcelFormFields,
            parcel: pm.currentParcel,
        }

        if (!eventsOnly) {
            $("#parcel-form").empty();
            $("#parcelFormTemplate").tmpl(parcelForm).appendTo("#parcel-form");

            $("#parcel-form button").click(function(e){
                parcelForm = $("#parcel-form form");
                actionPath = parcelForm.attr("action").slice(2);
                formObject = pm.formAsObject(parcelForm);
                action = $(this).attr("id");
                
                console.log(formObject);

                if (action == "update") {
                    pm.updateParcel(actionPath, formObject);
                } else if (action == "delete") {
                    pm.deleteParcel(actionPath);
                }
                
                e.stopPropagation();
                return false;
            });
        }

        $("#parcel-events-list").empty();
        
        $("#parcelEventListItemTemplate").tmpl(pm.currentParcel.events).appendTo("#parcel-events-list");

        $("#parcel-events-list li").hover(function(){
            $(this).find("button").show(100);
        },function(){
            $(this).find("button").hide(100);
        });
        
        $("#parcel-events-list li button").click(function(){
            parentId = $(this).parent().attr("id");
            eventId = parentId.split("_")[1]; // haaaaack
            parcelId = pm.currentParcel.id;
            console.log(parcelId);
            console.log(eventId);
            pm.deleteEvent($(this).parent(), parcelId, eventId);
        });
        
        $("#event-form button").click(function(e){
            eventForm = $("#event-form");
            parcelId = pm.currentParcel.id;
            formObject = pm.formAsObject(eventForm);
            pm.addEvent(parcelId, formObject);
            e.stopPropagation();
            return false;
        });


    },
    addEvent : function(parcelId, formObject) {
        console.log(parcelId);
        console.log(formObject);
        parcelPath = "/parcels/" + parcelId;
        formJson = JSON.stringify(formObject);
        $.post(parcelPath, formJson, function(){
            pm.loadParcelData(parcelPath, true);
        });
    },
    deleteEvent : function(eventElement, parcelId, eventId) {
        url = "/parcels/" + parcelId + "/" + eventId;
        console.log(url);
        $.ajax({url: url, success: function(response){
            console.log(response);
            eventElement.hide(200);
        }, type: "DELETE"});
    },
    addParcel : function(formObject) {
        formJson = JSON.stringify(formObject);
        console.log(formJson);
        $.ajax({url: "/parcels", data: formJson, success: function(response){
            pm.loadParcels();
        }, contentType: "application/json", type: "POST"});
    },
    updateParcel : function(url, formObject) {
        formJson = JSON.stringify(formObject);
        console.log(url);
        console.log(formJson);
        $.ajax({url: url, data: formJson, success: function(response){
            console.log(response);
        }, contentType: "application/json", type: "PUT"});
    },
    deleteParcel : function(url) {
        formJson = JSON.stringify(formObject);
        console.log(url);
        $.ajax({url: url, success: function(response){
            pm.loadParcels();
        }, type: "DELETE"});
    },
    formAsObject : function(formElement) {
        asArray = formElement.serializeArray();
        formHash = {};
        $.each(asArray, function(i, item){
            value = item.value;
            if (item.name.indexOf("date") >= 0) {
                if (value.length == 10) {
                    dateArray = value.split("-");
                    temp_date = new Date(dateArray[0], dateArray[1], dateArray[2]);
                    value = temp_date.getTime();
                } else {
                    dateTimeParts = value.split(" ");
                    dateArray = dateTimeParts[0].split("-")
                    timeArray = dateTimeParts[1].split(":")
                    temp_date = new Date(dateArray[0], dateArray[1], dateArray[2], timeArray[0], timeArray[1], timeArray[2]);
                    value = temp_date.getTime();
                }
            }
            
            if (item.name == "error" && value == "on") {
                // hack for fixing the error flag
                value = true;
            }
            formHash[item.name] = value;
        });
        console.log(formHash);
        return formHash;
    },
    prettifyFieldName : function(fieldName) {
        prettyFieldName = fieldName.replace("_", " ");
        return prettyFieldName;
    },
    getNiceDate : function(timestamp) {
        d = new Date()
        if (timestamp != undefined) {
            d = new Date(timestamp);
        }
        
        javascriptLacksDateFormatter = "";
        javascriptLacksDateFormatter += d.getFullYear();
        javascriptLacksDateFormatter += "-";
        month = d.getMonth() + 1; // !"€(!"%/!/"%(!"%)!"(%!)))"!!!!!!!!!!
        if (month < 10) {
            javascriptLacksDateFormatter += "0";
        }
        javascriptLacksDateFormatter += month;
        javascriptLacksDateFormatter += "-";
        if (d.getDate() < 10) {
            javascriptLacksDateFormatter += "0";
        }
        javascriptLacksDateFormatter += d.getDate();
        return javascriptLacksDateFormatter;
    },
    getNiceDateTime : function(timestamp) {
        d = new Date()
        if (timestamp != undefined) {
            d = new Date(timestamp);
        }

        javascriptLacksDateFormatter = pm.getNiceDate(timestamp);
        javascriptLacksDateFormatter += " ";
        if (d.getHours() < 10) {
            javascriptLacksDateFormatter += "0";
        }
        javascriptLacksDateFormatter += d.getHours();
        javascriptLacksDateFormatter += ":";
        if (d.getMinutes() < 10) {
            javascriptLacksDateFormatter += "0";
        }
        javascriptLacksDateFormatter += d.getMinutes();
        return javascriptLacksDateFormatter;
    }
    
}

$(document).ready(function(){
    pm.init();
})