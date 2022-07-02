
function eventUpdateUser(username) {
    //var eventSource = new EventSource("{{ url_for('views.listen') }}");
    var eventSource = new EventSource("/listen");

    eventSource.addEventListener(username, function(e) {
        var data = e.data;
        data = data.replaceAll("\'", '\"');
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
        console.log(data);
        data = JSON.parse(data);
        console.log("Event arrived!");

        machine_or_exercise = data['machine_or_exercise'];
        console.log("Prima valeva: " + document.getElementById(machine_or_exercise).textContent);
        if (document.getElementById(machine_or_exercise + "_notification").textContent == " X ") {
            console.log("It's a STRING");
            document.getElementById(machine_or_exercise).innerHTML = data['calories_or_repetitions_spent'] + " Cal";
        } else {
            console.log("It's an INT");
            document.getElementById(machine_or_exercise).innerHTML = data['calories_or_repetitions_spent'] + " Rep";
        }
    }, true)
}