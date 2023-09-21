document.addEventListener("DOMContentLoaded", function () {
    const textInput = document.getElementById("textInput");
    const showTableButton = document.getElementById("showTableButton");
    const tableContainer = document.getElementById("table-container");
    const dataTable = document.getElementById("dataTable");

    // Function to handle button click
    function handleButtonClick() {
        const searchText = textInput.value;
        // Send a POST request to the server with the search text
        fetch("/get_table_data", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ searchText })
        })
            .then(response => response.json())
            .then(data => {
                // Clear previous table data
                dataTable.innerHTML = "";

                // Create table headers
                // const headers = Object.keys(data[0]);
                const headers = ["Cate", "Keyword"]
                const headerRow = document.createElement("tr");
                headers.forEach(header => {
                    const th = document.createElement("th");
                    th.textContent = header;
                    headerRow.appendChild(th);
                });
                dataTable.appendChild(headerRow);

                // Populate table with data
                data.forEach(item => {
                    const row = document.createElement("tr");
                    headers.forEach(header => {
                        const td = document.createElement("td");
                        td.textContent = item[header];
                        row.appendChild(td);
                        // console.log(item[header], header)
                    });
                    dataTable.appendChild(row);
                });

                // Show the table
                tableContainer.style.display = "block";
            })
            .catch(error => console.error(error));
    }

    // Event listener for the button click
    showTableButton.addEventListener("click", handleButtonClick);

    // Event listener for the Enter key press
    textInput.addEventListener("keyup", function (event) {
        if (event.key === "Enter") {
            // Simulate a button click when Enter is pressed
            handleButtonClick();
        }
    });
});
