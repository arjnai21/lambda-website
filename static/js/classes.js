$( document ).ready(function() {
    loadClasses();
});

function loadClasses(){
    searchVal = $('#search').val();
    $.ajax({
        type: "GET",
        url: "/getClasses/" + searchVal,
        success: function (classes) {
            displayClasses(JSON.parse(classes));
        },
        failure: function (data) {
            console.log("Failure on GET in loadClasses");
        }
    });
}

function displayClasses(classes) {
    $("#classesDisplay").empty();

    for (var i = 0; i < classes.length; i++){
        var cls = classes[i];
        var classId = cls['id'];
        var name = cls['name'];
        
        // Create a class div for each class with id name# 
        $("#classesDisplay").append("<div id='"+ i +"'></div>");

        id = '#' + i;
        $(id).append("<a href='classPage/" + classId + "'>"+ classId + " - " + name + "</a></br>");
        
        for(var j = 0; j < cls['semesters'].length; j++) {
            var semester = cls['semesters'][j];

            $(id).append("<b>" + semester['year'] + "</b></br>");

            for(var k = 0; k < semester['usernames'].length; k++) {
                var name = semester['usernames'][k];
                $(id).append("<a href='/profile/" + name + "'>" + name + "</a></br>");
            }
        }

        $(id).append("</br></br");
    }
}