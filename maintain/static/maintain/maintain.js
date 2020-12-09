
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
    const partGroup = document.getElementById("part-group");
    const numPart = partGroup.childElementCount + 1;

    // Clone the first part element
    let part = partGroup.firstElementChild.cloneNode(true)
    let inputs = part.getElementsByTagName("input")
    for (let input of inputs) {

        // Get the input's name attribute
        let name = input.getAttribute("name")

        // Change the name attribute based on new part num
        let pos = name.lastIndexOf("-")
        name = name.slice(0, pos+1) + numPart.toString()

        // Set new name
        input.setAttribute("name", name)
    }
    
    // Add part to end of partGroup
    partGroup.append(part)
}