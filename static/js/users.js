$( document ).ready(function() {
    loadUsers();
});

function loadUsers(){
    searchVal = $('#search').val();
    $.ajax({
        type: "GET",
        url: "/getUsers/" + searchVal,
        success: function (users) {
            displayUsers(JSON.parse(users));
        },
        failure: function (data) {
            console.log("Failure on GET in loadUsers");
        }
    });
}

function displayUsers(users) {
    $("#userDisplay").empty();

    for (var i = 0; i < users.length; i++){
        var user = users[i];
        var name = user['name'];
        var email = user['email'];
        var major = user['major'];
        var doubleMajor = user['doubleMajor'];
        var minor = user['minor'];
        var phoneNumber = user['phoneNumber'];
        var year = user['year'];

        // Create a user div for each user with id name# 
        $("#userDisplay").append("<div id='"+i+"'></div>");

        id = '#' + i;
        $(id).append("<a href='/profile/" + name + "'>"+ name + "</a></br>");
        if (year) {$(id).append("Year: " + year + "</br>")}
        $(id).append(email + "</br>");
        if (phoneNumber) {$(id).append("Phone Number: " + phoneNumber + "</br>")}
        if (major) {$(id).append("Major: " + major + "</br>")}
        if (doubleMajor) {$(id).append("Double Major: " + doubleMajor + "</br>")}
        if (minor) {$(id).append("Minor: " + minor + "</br>") }

        /* Remove for now
        for(var j = 0; j < user['semesters'].length; j++) {
            var semester = user['semesters'][j];
            $(id).append("<b>" + semester['year'] + "</b></br>");

            for(var k = 0; k < semester['classes'].length; k++) {
                var cls = semester['classes'][k];
                $(id).append(cls + "</br>");
            }
        }
        */

        $(id).append("</br></br");
    }
}