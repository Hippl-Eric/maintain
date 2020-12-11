function setDefaultCar(elem, event) {
    event.preventDefault();

    // Grab the car id and site csrf token
    const car_id = elem.id;
    const csrftoken = Cookies.get('csrftoken');

    // Create request for get_car
    const request = new Request(
        `/defaultcar/${car_id}`,
        {
            method: "GET",
            headers: {'X-CSRFToken': csrftoken},
            mode: "same-origin",
        }
    );

    // Set as default car
    fetch(request)
    .then(response => {
        if (response.ok) {

            // Route to original anchor href
            const childAnchor = elem.children
            const href = childAnchor[0].href
            window.location.href = href;
        };
    })
};

if (document.getElementById("addPartBtn")) {
    document.getElementById("addPartBtn").addEventListener("click", addPart, true);
}

function addPart() {

    // Grab the part group div and determine number of existing parts
    const form = document.getElementById("service-form");
    const partGroup = form.querySelector("#part-group");
    const numPart = partGroup.childElementCount + 1;

    // Clone the first part element
    let part = partGroup.firstElementChild.cloneNode(true)
    let inputs = part.getElementsByTagName("input")
    for (let input of inputs) {

        // Get the input's name attribute
        let name = input.name;

        // Change the name attribute based on new part num
        let pos = name.lastIndexOf("-");
        name = name.slice(0, pos+1) + numPart.toString();

        // Set new name and reset value if present
        input.name = name;
        input.value = "";
    }
    
    // Add part to end of partGroup
    partGroup.append(part)
}

if (document.querySelector(".reminder-service")) {
    const serviceLinks = document.querySelectorAll(".reminder-service");
    serviceLinks.forEach((service) => {
        service.addEventListener("click", getService, true);
    });
};

function getService() {

    // Grab the reminder id and site csrf token
    const remID = this.dataset.remid;
    const csrftoken = Cookies.get('csrftoken');

    // Create request to get service data to pre-fill form
    const request = new Request(
        "/servicedata",
        {
            method: "PUT",
            headers: {'X-CSRFToken': csrftoken},
            mode: "same-origin",
            body: JSON.stringify({
                rem_id: remID,
            })
        }
    );
    
    // Fetch service data and call fillServiceForm()
    fetch(request)
    .then(response => response.json())
    .then(data => {
        if(data.error) {
            alert(data.error);
        }
        else {
            const jsonData = JSON.parse(data);
            fillServiceForm(jsonData, remID);
        }
    });
};

function fillServiceForm(data, remID) {

    // Parse data
    const serviceName = data["service"]["name"]
    const reminderDuration = data["reminder"]["duration"]
    const reminderMileAmount = data["reminder"]["mile-amount"]
    const partsList = data["service"]["parts"]

    // Add reminder and service to form
    const form = document.getElementById("service-form");
    const service = form.querySelector("[name='service']");
    service.value = serviceName;
    const remDuration = form.querySelector("[name='duration']");
    remDuration.value = reminderDuration;
    const remMile = form.querySelector("[name='mile-amount']");
    remMile.value = reminderMileAmount;

    // Create additional parts in form
    const numParts = partsList.length
    for (let i=0; i < numParts-1; i++) {
        addPart();
    };

    // Add part data to form
    for (let i=0; i < numParts; i++) {
        let partName = form.querySelector(`[name='part-name-${i+1}']`)
        partName.value = partsList[i]["name"];
        let partNum = form.querySelector(`[name='part-number-${i+1}']`)
        partNum.value = partsList[i]["number"];
    };

    // Add reminder id to hidden input
    const reminderID = form.querySelector("[name='reminder-id']");
    reminderID.value = remID;
}

// Reset Service form when Bootstrap modal is closed
$('#NewServiceModal').on('hidden.bs.modal', function () {
    resetForm()
})    

function resetForm() {

    // Clear all form values
    const form = document.getElementById("service-form");
    form.reset();

    // Remove any added parts
    const partGroup = form.querySelector("#part-group");
    const partNodes = partGroup.children;
    while (partNodes.length > 1) {
        partNodes[1].remove()
    }
}