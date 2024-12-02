

document.addEventListener("DOMContentLoaded", () => {
    const cityInput = document.getElementById("City");
    const suggestionsBox = document.getElementById("suggestions");

    cityInput.addEventListener("input", () => {
        const query = cityInput.value;
        if (query.length > 2) {
            fetch(`/autocomplete?query=${query}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsBox.innerHTML = "";
                    data.forEach(location => {
                        const suggestion = document.createElement("div");
                        suggestion.textContent = location;
                        suggestion.style.padding = "5px";
                        suggestion.style.cursor = "pointer";
                        suggestion.addEventListener("click", () => {
                            cityInput.value = location;
                            suggestionsBox.innerHTML = "";
                        });
                        suggestionsBox.appendChild(suggestion);
                        console.log(suggestion);
                    });
                })
                .catch(error => console.error("Error fetching autocomplete data:", error));
        } else {
            suggestionsBox.innerHTML = "";
        }
    });

    document.addEventListener("click", (e) => {
        if (!suggestionsBox.contains(e.target) && e.target !== cityInput) {
            suggestionsBox.innerHTML = "";
        }
    });

    if (!localStorage.getItem('state')) {
        localStorage.setItem('state', 'true');
    };
    
    const box = document.getElementById("switchBox");
    
    if (localStorage.getItem('state') === 'true') {
        box.setAttribute("checked", true);
    }
    else {
        box.removeAttribute("checked");
    };
});


//  working 

const box = document.getElementById("switchBox");

box.addEventListener("click", function() {

    localStorage.setItem('state', box.checked);

    const city = document.getElementById("City");
    const region = document.getElementById("region");
    const content = document.getElementById("content");

    let send = {
        state: localStorage.getItem('state')
    };
    console.log(send);
    fetch('/toggle-unit', {
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
    .catch(error => {
        console.error('Error:', error);
    });
});

