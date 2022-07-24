
function eventUpdateUser(username) {
    //var eventSource = new EventSource("{{ url_for('views.listen') }}");
    var eventSource = new EventSource("/listen");

    eventSource.addEventListener(username, function(e) {
        var data = e.data;
        data = data.replaceAll("\'", '\"');
        data = data.replaceAll("Decimal(", '');
        data = data.replaceAll(")", '');
        data = data.replaceAll("F", 'f');
        //console.log(data);
        data = JSON.parse(data);
        console.log("Event arrived! Username (it is also the Id of the event) is: " + data["username"]);

        myAreaChart(data['gym']);
        myBarChart(data['gym']['machines']);
        myPieChart(data['gym']['data'])
    }, true)
}

function eventUpdateTrainingCard(username) {
    var eventSource = new EventSource("/listenTrainingCard");

    eventSource.addEventListener(username + "TrainingCard", function(e) {
        var data = e.data;
        data = data.replaceAll("\'", '\"');
        data = data.replaceAll("Decimal(", '');
        data = data.replaceAll(")", '');
        console.log(data);
        data = JSON.parse(data);
        console.log("Event arrived!");

        name_machine = data['name_machine'];
        //console.log("Its value before: " + document.getElementById(name_machine).textContent);
        alert_success = document.getElementById('alert-success');
        alert_success_msg = document.getElementById('alert-success-msg');
        if (document.getElementById(name_machine + "_notification").textContent == " X ") {
            //console.log("It's a STRING");
            document.getElementById(name_machine).innerHTML = data['calories_left'] + " Cal";
            alert_success.innerHTML = "You just consumed about <b>" + data['calories_consumed'] + " Cal</b> on " + name_machine.replaceAll('_', " ") + "!";
        }

        alert_success.classList.add('show');
    }, true)
}