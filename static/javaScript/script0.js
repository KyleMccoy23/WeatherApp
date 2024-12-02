document.addEventListener("DOMContentLoaded", () => {
    const cityInput = document.getElementById("City");
    const submitButton = document.getElementById("submit");
    const toggleSwitch = document.getElementById("switchBox");
    const contentElement = document.getElementById("content");
    const cityElement = document.getElementById("city");
    const regionElement = document.getElementById("region");

    // Handle weather form submission
    submitButton.addEventListener("click", (event) => {
        event.preventDefault(); // Prevent form submission

        const city = cityInput.value.trim();
        if (city) {
            fetchWeather(city);
        }
    });

    // Handle temperature unit toggle
    toggleSwitch.addEventListener("change", () => {
        const state = toggleSwitch.checked;
        toggleTemperatureUnit(state);
    });

    // Fetch weather data
    function fetchWeather(city) {
        fetch("/weather", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ City: city }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    console.error("Error fetching weather:", data.error);
                } else {
                    updateWeatherUI(data);
                }
            })
            .catch((error) => console.error("Error:", error));
    }

    // Toggle temperature unit
    function toggleTemperatureUnit(state) {
        fetch("/toggle-unit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ state: state }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    console.error("Error toggling unit:", data.error);
                } else {
                    // Re-fetch weather with the updated unit
                    const city = cityInput.value.trim() || cityElement.textContent;
                    fetchWeather(city);
                }
            })
            .catch((error) => console.error("Error:", error));
    }

    // Update UI with fetched weather data
    function updateWeatherUI(data) {
        contentElement.textContent = data.content;
        cityElement.textContent = data.city;
        regionElement.textContent = data.region;
    }
});
