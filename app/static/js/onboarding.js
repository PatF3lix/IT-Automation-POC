const startOnboardingForm = document.getElementById("start-onboarding-form");
const findOnboardingForm = document.getElementById("find-onboarding-form");
const completeOnboardingForm = document.getElementById("complete-onboarding-form");

// Display onboarding
function displayOnboarding(data) {
    const onboarding = data.onboarding;
    const tasks = data.tasks;

    document.getElementById("result-onboarding-id").textContent = onboarding.id;

    document.getElementById("result-employee-name").textContent =
        onboarding.employee_name || "Unknown Employee";

    document.getElementById("result-onboarding-status").textContent =
        onboarding.status;

    document.getElementById("result-created-at").textContent =
        onboarding.created_at || "-";

    document.getElementById("result-completed-at").textContent =
        onboarding.completed_at || "Not completed";

    const taskContainer = document.getElementById("onboarding-tasks");
    taskContainer.innerHTML = "";

    tasks.forEach(function(task) {

        const taskDiv = document.createElement("div");

        taskDiv.classList.add("onboarding-task");

        if (task.status === "Completed") {
            taskDiv.classList.add("completed");
        }

        taskDiv.innerHTML = `
            <p><strong>Task:</strong> ${task.task}</p>
            <p><strong>Category:</strong> ${task.category}</p>
            <p><strong>Assigned To:</strong> ${task.assigned_to}</p>
            <p><strong>Status:</strong> ${task.status}</p>

            <button
                type="button"
                onclick="completeTask(${task.id})"
                ${task.status === "Completed" ? "disabled" : ""}
            >
                Mark Completed
            </button>
        `;

        taskContainer.appendChild(taskDiv);
    });

    document.getElementById("onboarding-result").style.display = "block";
}


// Start Onboarding
if (startOnboardingForm) {

    startOnboardingForm.addEventListener("submit", async function(event) {

        event.preventDefault();

        const employeeId = parseInt(
            document.getElementById("onboarding-employee-id").value
        );

        try {

            const response = await fetch(
                `/employees/${employeeId}/onboarding`,
                {
                    method: "POST"
                }
            );

            const data = await response.json();

            if (!response.ok) {
                alert(data.error || "Unable to start onboarding");
                return;
            }

            displayOnboarding(data);

            startOnboardingForm.reset();

        } catch(error) {

            console.error(error);

            alert("Unable to communicate with the server.");
        }
    });
}


// Find Onboarding
if (findOnboardingForm) {

    findOnboardingForm.addEventListener("submit", async function(event) {

        event.preventDefault();

        const onboardingId =
            document.getElementById("search-onboarding-id").value;

        try {

            const response = await fetch(
                `/onboardings/${onboardingId}`
            );

            const data = await response.json();

            if (!response.ok) {
                alert(data.error || "Onboarding not found");
                return;
            }

            displayOnboarding(data);

        } catch(error) {

            console.error(error);

            alert("Unable to communicate with the server.");
        }
    });
}


// Complete Individual Task
async function completeTask(taskId) {

    try {

        const response = await fetch(
            `/onboarding/tasks/${taskId}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    status: "Completed"
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || "Unable to update task");
            return;
        }

        const onboardingId =
            document.getElementById("result-onboarding-id").textContent;

        const refreshResponse =
            await fetch(`/onboardings/${onboardingId}`);

        const refreshData =
            await refreshResponse.json();

        if (refreshResponse.ok) {
            displayOnboarding(refreshData);
        }

    } catch(error) {

        console.error(error);

        alert("Unable to communicate with the server.");
    }
}


// Complete Onboarding
if (completeOnboardingForm) {

    completeOnboardingForm.addEventListener("submit", async function(event) {

        event.preventDefault();

        const onboardingId =
            document.getElementById("complete-onboarding-id").value;

        try {

            const response = await fetch(
                `/onboardings/${onboardingId}/complete`,
                {
                    method: "POST"
                }
            );

            const data = await response.json();

            if (!response.ok) {
                alert(data.error || "Unable to complete onboarding");
                return;
            }

            const refreshResponse =
                await fetch(`/onboardings/${onboardingId}`);

            const refreshData =
                await refreshResponse.json();

            if (refreshResponse.ok) {
                displayOnboarding(refreshData);
            }

            completeOnboardingForm.reset();

        } catch(error) {

            console.error(error);

            alert("Unable to communicate with the server.");
        }
    });
}