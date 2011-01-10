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
        pm.loadParcels();
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
        $("#parcels li:first").addClass("selected");
        $("#parcels a.tracking-number").click(function(e){
            pm.selectParcel($(this));
        });
        pm.selectParcel($("#parcels li:first a"));
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
    loadParcelData : function(parcelPath) {
        $.getJSON(parcelPath, function(response){
            console.log(response);
            pm.currentParcel = response;
            pm.parcelDataUpdated();
        });
    },
    parcelDataUpdated : function() {
        pm.hideParcelInfoLoader();
        parcelForm = {
            fields: pm.parcelFormFields,
            parcel: pm.currentParcel,
        }

        $("#parcel-form").empty();
        $("#parcelFormTemplate").tmpl(parcelForm).appendTo("#parcel-form");
        
        $("#submit").click(function(e){
            parcelForm = $("#parcel-form form");
            actionPath = parcelForm.attr("action").slice(2);
            formObject = pm.formAsObject(parcelForm);
            pm.updateParcel(actionPath, formObject);
            console.log(formObject);
            e.stopPropagation();
            return false;
        });

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


    },
    deleteEvent : function(eventElement, parcelId, eventId) {
        url = "/parcels/" + parcelId + "/" + eventId;
        console.log(url);
        $.ajax({url: url, success: function(response){
            console.log(response);
            eventElement.hide(200);
        }, type: "DELETE"});
    },
    updateParcel : function(url, formObject) {
        formJson = JSON.stringify(formObject);
        console.log(url);
        console.log(formJson);
        $.ajax({url: url, data: formJson, success: function(response){
            console.log(response);
        }, contentType: "application/json", type: "PUT"});
    },
    formAsObject : function(formElement) {
        asArray = formElement.serializeArray();
        formHash = {};
        $.each(asArray, function(i, item){
            value = item.value;
            if (item.name.indexOf("date") >= 0) {
                dateArray = value.split("-");
                temp_date = new Date(dateArray[0], dateArray[1], dateArray[2]);
                value = temp_date.getTime();
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
        d = new Date(timestamp);
        javascriptLacksDateFormatter = "";
        javascriptLacksDateFormatter += d.getFullYear();
        javascriptLacksDateFormatter += "-";
        if (d.getMonth() < 10) {
            javascriptLacksDateFormatter += "0";
        }
        javascriptLacksDateFormatter += d.getMonth();
        javascriptLacksDateFormatter += "-";
        if (d.getDate() < 10) {
            javascriptLacksDateFormatter += "0";
        }
        javascriptLacksDateFormatter += d.getDate();
        return javascriptLacksDateFormatter;
    },
    getNiceDateTime : function(timestamp) {
        d = new Date(timestamp);
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