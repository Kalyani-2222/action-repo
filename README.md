GitHub Webhook Activity Tracker
A web-based application that captures GitHub events via webhooks and displays them live using MongoDB and Flask.


<!DOCTYPE html>
<html>
<head>
    <title>GitHub Events</title>
</head>
<body>
    <h1>Latest GitHub Events</h1>
    <ul id="eventList"></ul>

    <script>
        function fetchEvents() {
            fetch("/events")
                .then(response => response.json())
                .then(data => {
                    const list = document.getElementById("eventList");
                    list.innerHTML = "";
                    data.forEach(event => {
                        let text = "";
                        const author = event?.sender?.login || "Someone";
                        const time = event.timestamp || "Unknown time";

                        if (event.event === "push") {
                            const branch = event.ref?.split("/").pop();
                            text = `${author} pushed to ${branch} on ${time}`;
                        } else if (event.event === "pull_request") {
                            const from = event.pull_request?.head?.ref;
                            const to = event.pull_request?.base?.ref;
                            text = `${author} submitted a pull request from ${from} to ${to} on ${time}`;
                        } else if (event.event === "merge") {
                            const from = event.pull_request?.head?.ref;
                            const to = event.pull_request?.base?.ref;
                            text = `${author} merged branch ${from} to ${to} on ${time}`;
                        }

                        const li = document.createElement("li");
                        li.textContent = text;
                        list.appendChild(li);
                    });
                });
        }

        setInterval(fetchEvents, 15000);
        fetchEvents();
    </script>
</body>
</html>
