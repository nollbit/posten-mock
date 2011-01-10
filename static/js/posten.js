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
        $("#info-loader").show();  
    },
    hideParcelInfoLoader : function() {
        $("#info-loader").hide();  
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
            formObject = pm.formAsJson($("#parcel-form form"));
            console.log(formObject);
            e.stopPropagation();
            return false;
        });
    },
    formAsJson : function(formElement) {
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
    }
    
}

$(document).ready(function(){
    pm.init();
})