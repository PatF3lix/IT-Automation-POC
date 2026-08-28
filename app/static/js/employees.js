const loadEmployeesButton = document.getElementById("load-employees-button");


// Load all employees
if (loadEmployeesButton) {

    loadEmployeesButton.addEventListener("click", async function() {

        try {

            const response = await fetch("/employees");
            const employees = await response.json();

            if (!response.ok) {
                alert("Unable to load employees");
                return;
            }

            const employeesList =
                document.getElementById("employees-list");

            employeesList.innerHTML = "";

            employees.forEach(function(employee) {

                const employeeDiv =
                    document.createElement("div");

                employeeDiv.classList.add("employee-item");

                employeeDiv.innerHTML = `
                    <div class="employee-summary">

                        <div class="employee-summary-main">

                            <h3 class="employee-card-name">
                                ${employee.first_name} ${employee.last_name}
                            </h3>

                            <p class="employee-card-role">
                                ${employee.job_title}
                            </p>

                            <p class="employee-card-department">
                                ${employee.department}
                            </p>

                        </div>

                        <span class="employee-card-id">
                            #${employee.id}
                        </span>

                    </div>

                    <div
                        id="employee-details-${employee.id}"
                        class="employee-inline-details"
                        style="display: none;"
                    >
                    </div>

                    <button
                        type="button"
                        class="view-employee-button"
                        id="employee-button-${employee.id}"
                        onclick="toggleEmployee(${employee.id})"
                    >
                        View Employee
                    </button>
                `;

                employeesList.appendChild(employeeDiv);
            });

        } catch(error) {

            console.error(error);
            alert("Unable to communicate with the server.");
        }
    });
}


// Toggle employee details
async function toggleEmployee(employeeId) {

    const detailsContainer =
        document.getElementById(
            `employee-details-${employeeId}`
        );

    const button =
        document.getElementById(
            `employee-button-${employeeId}`
        );


    // If currently visible, hide details
    if (detailsContainer.style.display === "block") {

        detailsContainer.style.display = "none";

        button.textContent = "View Employee";

        return;
    }


    // Otherwise load and show details
    await loadEmployee(employeeId);

    button.textContent = "Less Details";
}


// Load one employee + assigned assets + assigned tickets
async function loadEmployee(employeeId) {

    try {

        // Employee details
        const employeeResponse =
            await fetch(`/employees/${employeeId}`);

        const employee =
            await employeeResponse.json();

        if (!employeeResponse.ok) {
            alert(employee.error || "Employee not found");
            return;
        }


        // Assigned assets
        const assetsResponse =
            await fetch(`/employees/${employeeId}/assets`);

        const assetsData =
            await assetsResponse.json();

        if (!assetsResponse.ok) {
            alert("Unable to load employee assets");
            return;
        }


        // Assigned tickets
        const ticketsResponse =
            await fetch(`/employees/${employeeId}/tickets`);

        const ticketsData =
            await ticketsResponse.json();

        if (!ticketsResponse.ok) {
            alert("Unable to load employee tickets");
            return;
        }


        displayEmployee(
            employee,
            assetsData.assets,
            ticketsData.tickets
        );

    } catch(error) {

        console.error(error);

        alert("Unable to communicate with the server.");
    }
}


// Display employee information
function displayEmployee(employee, assets, tickets) {

    const detailsContainer =
        document.getElementById(
            `employee-details-${employee.id}`
        );


    // Build assigned assets
    let assetsHTML = "";

    if (assets.length === 0) {

        assetsHTML = `
            <div class="employee-empty-state">
                No assets assigned.
            </div>
        `;

    } else {

        assets.forEach(function(asset) {

            assetsHTML += `
                <div class="employee-asset">

                    <div class="employee-asset-header">

                        <strong>
                            ${asset.asset_tag}
                        </strong>

                        <span class="employee-asset-status">
                            ${asset.status || ""}
                        </span>

                    </div>

                    <div class="employee-asset-grid">

                        <div>
                            <span class="inline-label">
                                Type
                            </span>

                            <span class="inline-value">
                                ${asset.asset_type || "-"}
                            </span>
                        </div>


                        <div>
                            <span class="inline-label">
                                Manufacturer
                            </span>

                            <span class="inline-value">
                                ${asset.manufacturer || "-"}
                            </span>
                        </div>


                        <div>
                            <span class="inline-label">
                                Serial Number
                            </span>

                            <span class="inline-value">
                                ${asset.serial_number || "-"}
                            </span>
                        </div>

                    </div>

                </div>
            `;
        });
    }


    // Build assigned tickets
    let ticketsHTML = "";

    if (tickets.length === 0) {

        ticketsHTML = `
            <div class="employee-empty-state">
                No tickets assigned.
            </div>
        `;

    } else {

        tickets.forEach(function(ticket) {

            ticketsHTML += `
                <div class="employee-ticket">

                    <div class="employee-ticket-header">

                        <strong>
                            ${ticket.ticket_number}
                        </strong>

                        <span class="employee-ticket-status">
                            ${ticket.status || ""}
                        </span>

                    </div>

                    <div class="employee-ticket-grid">

                        <div>
                            <span class="inline-label">
                                Title
                            </span>

                            <span class="inline-value">
                                ${ticket.title || "-"}
                            </span>
                        </div>


                        <div>
                            <span class="inline-label">
                                Category
                            </span>

                            <span class="inline-value">
                                ${ticket.category || "-"}
                            </span>
                        </div>


                        <div>
                            <span class="inline-label">
                                Priority
                            </span>

                            <span class="inline-value">
                                ${ticket.priority || "-"}
                            </span>
                        </div>


                        <div>
                            <span class="inline-label">
                                Assigned Team
                            </span>

                            <span class="inline-value">
                                ${ticket.assigned_team || "-"}
                            </span>
                        </div>

                    </div>

                </div>
            `;
        });
    }


    // Display employee details
    detailsContainer.innerHTML = `

        <div class="inline-section">

            <span class="inline-section-label">
                Employee Information
            </span>

            <div class="employee-info-grid">

                <div class="employee-info-item">

                    <span class="inline-label">
                        Department
                    </span>

                    <span class="inline-value">
                        ${employee.department || "-"}
                    </span>

                </div>


                <div class="employee-info-item">

                    <span class="inline-label">
                        Manager
                    </span>

                    <span class="inline-value">
                        ${employee.manager || "-"}
                    </span>

                </div>


                <div class="employee-info-item">

                    <span class="inline-label">
                        Start Date
                    </span>

                    <span class="inline-value">
                        ${employee.start_date || "-"}
                    </span>

                </div>

            </div>

        </div>


        <div class="inline-section">

            <span class="inline-section-label">
                Assigned Assets
            </span>

            <div class="employee-assets-list">
                ${assetsHTML}
            </div>

        </div>


        <div class="inline-section">

            <span class="inline-section-label">
                Assigned Tickets
            </span>

            <div class="employee-tickets-list">
                ${ticketsHTML}
            </div>

        </div>
    `;

    detailsContainer.style.display = "block";
}