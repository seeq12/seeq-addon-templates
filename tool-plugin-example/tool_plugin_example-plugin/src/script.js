
document.addEventListener("DOMContentLoaded", function() {
    const number1 = document.getElementById("number1");
    const number2 = document.getElementById("number2");

    registerHandlers();

    document.getElementById("cancelButton").addEventListener("click", clearSelections);
    document.getElementById("executeButton").addEventListener("click", calculate);
});

function registerHandlers() {
    getSeeqApi().then(_seeq => {
        seeq = _seeq;
        seeq.subscribeToSignals(signals => syncSignals(signals));
    });
}

function syncSignals(signals) {
    const newSignals = signals.filter(s => s.valueUnitOfMeasure !== 'string')
    updateOptionSignals("number1", newSignals);
    updateOptionSignals("number2", newSignals); 
}

function updateOptionSignals(id, signals) {
    optionElement = document.getElementById(id);
    removeChildren(optionElement);
    const placeholderOption = new Option('Select an option', '', true, true);
    placeholderOption.hidden = true;
    optionElement.appendChild(placeholderOption);

    signals.forEach(signal => {
        let option = document.createElement("option");
        option.value = signal.id;
        option.text = signal.name;
        optionElement.appendChild(option);
    });
}

function removeChildren(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
    return element;
}

function clearSelections() {
    document.getElementById("number1").selectedIndex = 0;
    document.getElementById("operator").selectedIndex = 0;
    document.getElementById("number2").selectedIndex = 0;
    seeq.closeActiveTool();
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