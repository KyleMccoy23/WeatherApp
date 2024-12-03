

document.addEventListener("DOMContentLoaded", () => {

    const tabIdKey = "weatherTabId";

    // Check if a tab ID exists in sessionStorage
    if (!sessionStorage.getItem(tabIdKey)) {
        // Generate a new unique tab ID
        const tabId = `tab_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
        sessionStorage.setItem(tabIdKey, tabId);
    }

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

    if (!sessionStorage.getItem('state')) {
        sessionStorage.setItem('state', 'true');
    };
    
    const box = document.getElementById("switchBox");
    
    if (sessionStorage.getItem('state') === 'true') {
        box.setAttribute("checked", true);
    }
    else {
        box.removeAttribute("checked");
    };
});


const submitButton = document.getElementById('submit')

submitButton.addEventListener('click', () => {


    const tabId = sessionStorage.getItem("weatherTabId");

    // const city = document.getElementById("City");
    const region = document.getElementById("region");
    const content = document.getElementById("content");

    fetch("/weather", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ City: cityInput, tabId: tabId }),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log('Success:', data);
            city.innerHTML = data.city;
            region.innerHTML = data.region;
            content.innerHTML = data.content;
        })
        .catch((error) => console.error("Error:", error));
});


//  working 

const box = document.getElementById("switchBox");

box.addEventListener("click", function() {

    sessionStorage.setItem('state', box.checked);

    const city = document.getElementById("City");
    const region = document.getElementById("region");
    const content = document.getElementById("content");

    let send = {
        state: sessionStorage.getItem('state')
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

