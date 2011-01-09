var pm = {
    "parcels" : [],
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
        $("#parcels a.tracking-number").click(function(){
            console.log($(this));
            return false;
        });
    },
}

$(document).ready(function(){
    pm.init();
});