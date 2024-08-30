const MAX_VALUE = 10; // Define the maximum value for the dropdowns

document.addEventListener("DOMContentLoaded", function() {
    const number1 = document.getElementById("number1");
    const number2 = document.getElementById("number2");

    // Populate dropdowns with numbers from 1 to MAX_VALUE
    for (let i = 1; i <= MAX_VALUE; i++) {
        let option1 = document.createElement("option");
        let option2 = document.createElement("option");
        option1.value = option2.value = i;
        option1.text = option2.text = i;
        number1.appendChild(option1);
        number2.appendChild(option2);
    }

    // Set up event listeners for buttons
    document.getElementById("cancelButton").addEventListener("click", clearSelections);
    document.getElementById("executeButton").addEventListener("click", calculate);
});

function clearSelections() {
    document.getElementById("number1").selectedIndex = 0;
    document.getElementById("operator").selectedIndex = 0;
    document.getElementById("number2").selectedIndex = 0;
}

function calculate() {
    const num1 = parseInt(document.getElementById("number1").value);
    const num2 = parseInt(document.getElementById("number2").value);
    const operator = document.getElementById("operator").value;

    if (isNaN(num1) || isNaN(num2)) {
        alert("Please select both numbers.");
        return;
    }

    let result;
    switch (operator) {
        case '+':
            result = num1 + num2;
            break;
        case '-':
            result = num1 - num2;
            break;
        case '*':
            result = num1 * num2;
            break;
        case '/':
            if (num2 === 0) {
                alert("Cannot divide by zero.");
                return;
            }
            result = num1 / num2;
            break;
        default:
            alert("Invalid operation.");
            return;
    }

    console.log("Result: " + result);
}