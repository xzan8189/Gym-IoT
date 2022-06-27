
function eventUpdateUser(username) {
    //var eventSource = new EventSource("{{ url_for('views.listen') }}");
    var eventSource = new EventSource("/listen");

    eventSource.addEventListener(username, function(e) {
        var data = e.data;
        data = data.replaceAll("\'", '\"');
        //console.log(data);
        data = JSON.parse(data);
        console.log("Event arrived! Username (it is also the Id) is: " + data["username"]);

        myAreaChart(data['gym']);
        myBarChart(data['gym']['machines']);
        myPieChart(data['gym']['data'])
    }, true)


}