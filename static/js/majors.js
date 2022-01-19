$( document ).ready(function() {
    loadMajors();
});

function loadMajors(){
    searchVal = $('#search').val();
    $.ajax({
        type: "GET",
        url: "/getMajors/" + searchVal,
        success: function (majors) {
            displayMajors(JSON.parse(majors));
        },
        failure: function (data) {
            console.log("Failure on GET in loadMajors");
        }
    });
}

function displayMajors(majors){
    $("#majorsDisplay").empty();

    for (var i = 0; i < majors.length; i++){
        var major = majors[i];
        var majorName = major['name'];
        
        // Create a class div for each class with id  
        $("#majorsDisplay").append("<div id='"+ i +"'></div>");

        id = '#' + i;
        $(id).append("<a href='majorPage/" + majorName + "'>"+ majorName + "</a></br>");
        
        for(var j = 0; j < major['users'].length; j++) {
            var majorUser = major['users'][j]

            var majorType = majorUser['type'];
            if (majorType == 'major') {
                majorType = "Major";
            }
            else if (majorType == 'doubleMajor') {
                majorType = "Double Major";
            }
            else {
                majorType = "Minor";
            }
            
            $(id).append("<a href='/profile/" + majorUser['name'] + "'>" + majorUser['name'] + "</a> - " + majorType + "</br>");
        }

        $(id).append("</br></br");
    }
}