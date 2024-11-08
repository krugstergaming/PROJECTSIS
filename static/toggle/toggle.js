// Cache DOM elements for performance
const checkboxes = document.querySelectorAll('.column-check');
const table = document.querySelector(".table-hover");
const thElements = table.getElementsByTagName("th");
const trElements = table.getElementsByTagName("tr");
const searchInput = document.getElementById("Search");

// Add event listeners for checkboxes
checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', toggleColumns);
});

// Function to toggle visibility of table columns
function toggleColumns() {
    checkboxes.forEach(checkbox => {
        const columnIndex = checkbox.value;
        const displayStyle = checkbox.checked ? "" : "none";

        // Toggle visibility for the <th> element
        if (thElements[columnIndex]) {
            thElements[columnIndex].style.display = displayStyle;
        }

        // Toggle visibility for each row's corresponding <td> element
        for (let i = 0; i < trElements.length; i++) {
            const td = trElements[i].getElementsByTagName("td")[columnIndex];
            if (td) {
                td.style.display = displayStyle;
            }
        }
    });
}

// Add event listener for search input field
searchInput.addEventListener('keyup', searchTable);

// Function to search the table based on visible columns
function searchTable() {
    const filter = searchInput.value.toUpperCase();
    const tbody = table.querySelector("tbody");
    const rows = tbody.getElementsByTagName("tr");

    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName("td");
        let rowVisible = false;

        // Search only visible cells in the row
        for (let j = 0; j < cells.length; j++) {
            if (cells[j].style.display !== "none") {
                const cellText = cells[j].textContent || cells[j].innerText;
                if (cellText.toUpperCase().includes(filter)) {
                    rowVisible = true;
                    break;
                }
            }
        }

        // Show or hide the row based on the search result
        rows[i].style.display = rowVisible ? "" : "none";
    }
}
