const assetForm = document.getElementById("asset-form");
const assetSearchForm = document.getElementById("asset-search-form");
const assignAssetForm = document.getElementById("assign-asset-form");
const returnAssetForm = document.getElementById("return-asset-form");


function displayAsset(asset) {
    document.getElementById("result-asset-id").textContent = asset.id;
    document.getElementById("result-asset-tag").textContent = asset.asset_tag;
    document.getElementById("result-asset-type").textContent = asset.asset_type;
    document.getElementById("result-manufacturer").textContent =
        asset.manufacturer || "-";
    document.getElementById("result-serial-number").textContent =
        asset.serial_number || "-";
    document.getElementById("result-status").textContent = asset.status;
    document.getElementById("result-assigned-to").textContent =
        asset.assigned_to ?? "Not assigned";
    document.getElementById("result-purchase-date").textContent =
        asset.purchase_date || "-";
    document.getElementById("result-warranty-end").textContent =
        asset.warranty_end || "-";

    document.getElementById("asset-result").style.display = "block";
}


// CREATE ASSET
if (assetForm) {
    assetForm.addEventListener("submit", async function(event) {
        event.preventDefault();

        const assetData = {
            asset_tag: document.getElementById("asset-tag").value,
            asset_type: document.getElementById("asset-type").value,
            manufacturer: document.getElementById("manufacturer").value,
            serial_number: document.getElementById("serial-number").value,
            assigned_to: null,
            purchase_date:
                document.getElementById("purchase-date").value || null,
            warranty_end:
                document.getElementById("warranty-end").value || null
        };

        try {
            const response = await fetch("/assets", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(assetData)
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.error || "Asset creation failed");
                return;
            }

            displayAsset(data);
            assetForm.reset();

        } catch(error) {
            console.error(error);
            alert("Unable to communicate with the server.");
        }
    });
}


// FIND ASSET
if (assetSearchForm) {
    assetSearchForm.addEventListener("submit", async function(event) {
        event.preventDefault();

        const assetId =
            document.getElementById("search-asset-id").value;

        try {
            const response = await fetch(`/assets/${assetId}`);
            const data = await response.json();

            if (!response.ok) {
                alert(data.error || "Asset not found");
                return;
            }

            displayAsset(data);

        } catch(error) {
            console.error(error);
            alert("Unable to communicate with the server.");
        }
    });
}


// ASSIGN ASSET
if (assignAssetForm) {
    assignAssetForm.addEventListener("submit", async function(event) {
        event.preventDefault();

        const assetId = parseInt(
            document.getElementById("assign-asset-id").value
        );

        const employeeId = parseInt(
            document.getElementById("assign-employee-id").value
        );

        try {
            const response = await fetch(`/assets/${assetId}/assign`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    employee_id: employeeId
                })
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.error || "Asset assignment failed");
                return;
            }

            displayAsset(data);
            assignAssetForm.reset();

        } catch(error) {
            console.error(error);
            alert("Unable to communicate with the server.");
        }
    });
}


// RETURN ASSET
if (returnAssetForm) {
    returnAssetForm.addEventListener("submit", async function(event) {
        event.preventDefault();

        const assetId = parseInt(
            document.getElementById("return-asset-id").value
        );

        try {
            const response = await fetch(`/assets/${assetId}/return`, {
                method: "POST"
            });

            const data = await response.json();

            if (!response.ok) {
                alert(
                    data.error ||
                    data.Error ||
                    "Asset return failed"
                );
                return;
            }

            displayAsset(data);
            returnAssetForm.reset();

        } catch(error) {
            console.error(error);
            alert("Unable to communicate with the server.");
        }
    });
}