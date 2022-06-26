
function eventUpdateUser() {
    //var eventSource = new EventSource("{{ url_for('views.listen') }}");
    var eventSource = new EventSource("/listen");

    eventSource.addEventListener("online", function(e) {
        var data = e.data;
        data = data.replaceAll("\'", '\"');
        console.log(data);
        data = JSON.parse(data);
        console.log("L'id è: " + data["Id"]);
    }, true)


}