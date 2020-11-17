document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM Loaded!")
    
});

function getcar(elem) {
    console.log(elem);

    // Grab the car id and site csrf token
    const car_id = elem.id;
    const csrftoken = Cookies.get('csrftoken');

    // Create request for car details route
    const request = new Request(
        `/car/${car_id}`,
        {
            method: "PUT",
            headers: {'X-CSRFToken': csrftoken},
            mode: "same-origin",
            body: JSON.stringify({
                default: true,
            })
        }
    );

    // Set as default car
    fetch(request)
    .then(response => {
        if (response.ok) {
            window.location.href = "/car/info";
        };
    })
};