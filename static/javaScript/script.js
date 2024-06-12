

if (!localStorage.getItem('state')) {
    localStorage.setItem('state', 'true');
};

const box = document.getElementById("switchBox");

if (localStorage.getItem('state') === 'true') {
    box.setAttribute("checked", 'checked');
}
else {
    box.removeAttribute("checked");
};

box.addEventListener("click", function() {

    localStorage.setItem('state', box.checked);

    const city = document.getElementById("City");
    const region = document.getElementById("region");
    const content = document.getElementById("content");

    let send = {
        city: city.innerHTML,
        state: localStorage.getItem('state')
    };
    
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(send)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        city.innerHTML = data.city;
        region.innerHTML = data.region;
        content.innerHTML = data.content;
    })
    .then(() => {
        // window.location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

