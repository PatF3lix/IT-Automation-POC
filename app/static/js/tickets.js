// 1- get form
const ticketForm = document.getElementById("ticket-form");

if (ticketForm) {
    // 2- create listener
    ticketForm.addEventListener("submit", async function(event){
        // stops page from reloading
        event.preventDefault();

        // 3- build ticket js object
        const ticketData = {
            employee_id: parseInt(
                document.getElementById("employee-id").value
            ),
            title: document.getElementById("title").value,
            description: document.getElementById("description").value
        };

        try {
            // 4- send it to flask
            const response = await fetch("/tickets", {
                method: "POST",
                headers: {
                    "Content-type": "application/json"
                },
                body: JSON.stringify(ticketData)
            });
            //5- await for flask response
            const data = await response.json();

            if (!response.ok){
                alert(data.error || "Ticket creation failed");
                return;
            }
            // 7- display response values
            document.getElementById("result-ticket-number").textContent = data.ticket_number;
            document.getElementById("result-category").textContent = data.category;
            document.getElementById("result-priority").textContent = data.priority;
            document.getElementById("result-team").textContent = data.assigned_team;
            document.getElementById("result-summary").textContent = data.ai_summary;

            const recommendationList = document.getElementById("result-recommendations");

            recommendationList.innerHTML = "";
            // 8- display multiple recommendations
            data.ai_recommendations.forEach(function (recommendation) {
                const item = document.createElement("li");
                item.textContent = recommendation;
                recommendationList.appendChild(item);
            });
            // 9- show the hidden result card
            document.getElementById("ticket-result").style.display = "block";
        } catch (error) {
        // 10 -catch unexpected failures
        console.error(error);
        alert("Unable to communicate with the server.");
    }
    });
}