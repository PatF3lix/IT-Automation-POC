const loadEmployeesButton = document.getElementById("load-employees-button");

//Load all employees
if(loadEmployeesButton) {

    loadEmployeesButton.addEventListener("click", async function() {

        try{
            const response = await fetch("/employees");
            const employees = await response.json();

            if(!response.ok) {
                alert("Unable to load employees");
                return;
            }

            const employeesList = document.getElementById("employees-list");
            employeesList.innerHTML = "";

            employees.forEach(function(employee){
                const employeeDiv = document.createElement("div");
                employeeDiv.classList.add("employee-item");

                employeeDiv.innerHTML = `
                    <p>
                        <strong>
                            ${employee.first_name} ${employee.last_name}
                        </strong>
                    </p>

                    <p>${employee.job_title}</p>

                    <div
                        id="employee-details-${employee.id}"
                        class="employee-inline-details"
                        style="display: none;"
                    >
                    </div>

                    <button
                        type="button"
                        onclick="loadEmployee(${employee.id})"
                    >
                        View Employee
                    </button>

                    <hr>
                `;

                employeesList.appendChild(employeeDiv);
            });
        }catch(error){
            console.error(error);
            alert("Unable to communicate with the server.")
        }
    });
}

// Load one employee + assigned assets
async function loadEmployee(employeeId){

    try{

        //Employee details
        const employeeResponse = await fetch(`/employees/${employeeId}`);
        const employee = await employeeResponse.json();

        if (!employeeResponse.ok){
            alert(employee.error || "Employee not found");
            return;
        }

        //Assigned assets
        const assetsResponse = await fetch(`/employees/${employeeId}/assets`);
        const assetsData = await assetsResponse.json();

        if (!assetsResponse.ok){
            alert("Unable to load employee assets");
            return;
        }

        displayEmployee(employee, assetsData.assets);

        document.getElementById("employee-tickets-card").style.display = "block";
    }catch(error){
        console.error(error);
        alert("Unable to communicate with the server.");
    }
}

// Display employee information
function displayEmployee(employee, assets){

    const detailsContainer = document.getElementById(
        `employee-details-${employee.id}`
    );

    let assetsHTML = "";

    if (assets.length === 0) {
        assetsHTML = `
            <p>No assets assigned.</p>
        `;
    } else {

        assets.forEach(function(asset){
            assetsHTML += `
                <div class="employee-asset">
                    <p><strong>${asset.asset_tag}</strong></p>
                    <p>Type: ${asset.asset_type}</p>
                    <p>Manufacturer: ${asset.manufacturer}</p>
                    <p>Serial Number: ${asset.serial_number}</p>
                </div>
            `;
        });
    }

    detailsContainer.innerHTML = `
        <h4>Employee Details</h4>

        <p><strong>ID:</strong> ${employee.id}</p>
        <p><strong>Department:</strong> ${employee.department}</p>
        <p><strong>Manager:</strong> ${employee.manager || "-"}</p>
        <p><strong>Start Date:</strong> ${employee.start_date || "-"}</p>

        <h4>Assigned Assets</h4>

        ${assetsHTML}

        <h4>Assigned Tickets</h4>

        <p>Individual ticket assignment not implemented yet.</p>
    `;

    detailsContainer.style.display = "block";
}

// Display assigned assets
function displayEmployeeAssets(assets){

    const assetsContainer = document.getElementById("employee-assets");

    assetsContainer.innerHTML = "";

    if(assets.length === 0){
        assetsContainer.innerHTML = `
            <p>No assets assigned.</p>
        `;
        return;
    }

    assets.forEach(function(asset){

        const assetDiv = document.createElement("div");

        assetDiv.classList.add("employee-asset");

        assetDiv.innerHTML = `
            <p>
                <strong>${asset.asset_tag}</strong>
            </p>

            <p>
                Type: ${asset.asset_type}
            </p>

            <p>
                Manufacturer: ${asset.manufacturer}
            </p>

            <p>
                Serial Number: ${asset.serial_number}
            </p>

            <p>
                Status: ${asset.status}
            </p>

            <hr>
        `;

        assetsContainer.appendChild(assetDiv);
    });
}