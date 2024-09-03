

const DLF_PROJECT_NAME = "signal-combiner-dlf";

document.addEventListener("DOMContentLoaded", function() {
    registerHandlers();
    updateExecuteButton();

    document.getElementById("cancelButton").addEventListener("click", clearSelections);
    document.getElementById("executeButton").addEventListener("click", calculate);
    document.getElementById("signalA").addEventListener("change", updateExecuteButton);
    document.getElementById("signalB").addEventListener("change", updateExecuteButton);
});

function registerHandlers() {
    getSeeqApi().then(_seeq => {
        seeq = _seeq;
        seeq.subscribeToSignals(signals => syncSignals(signals));
    });
}

function syncSignals(signals) {
    const newSignals = signals.filter(s => s.valueUnitOfMeasure !== 'string')
    updateOptionSignals("signalA", newSignals);
    updateOptionSignals("signalB", newSignals); 
}

function updateOptionSignals(id, signals) {
    optionElement = document.getElementById(id);
    currentValue = optionElement.value;
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
    optionElement.value = currentValue;
}

function removeChildren(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
    return element;
}

function updateExecuteButton() {
    const signalA = document.getElementById("signalA").value;
    const signalB = document.getElementById("signalB").value;
    document.getElementById("executeButton").disabled = signalA === "" || signalB === "";
}

function clearSelections() {
    document.getElementById("signalA").selectedIndex = 0;
    document.getElementById("signalB").selectedIndex = 0;
    document.getElementById("operator").selectedIndex = 0;
    seeq.closeActiveTool();
}

async function calculate() {
    const idA = document.getElementById("signalA").value;
    const idB = document.getElementById("signalB").value;
    const op = document.getElementById("operator").value;

    hideError();
    showSpinner();
    try {
        const { projectId }= await seeq.getDataLabProject(DLF_PROJECT_NAME);
        const response = await seeq.callDataLabApi({
            projectId,
            notebookName: "api",
            method: "POST",
            path: "/combine",
            body: {
                idA,
                idB,
                op,
                workbookId: seeq.workbook.id,
                worksheetId: seeq.worksheet.id
            }
        })
    }
    catch (error) {
        showError(error?.data?.statusMessage);
    } finally {
        hideSpinner();
    }
}

function showSpinner() {
    document.getElementById("spinner").style.display = "block";
}

function hideSpinner() {
    document.getElementById("spinner").style.display = "none";
}

function showError(message) {
    document.getElementById("error").style.display = "block";
    document.getElementById("error").innerText = message;
}

function hideError() {
    document.getElementById("error").innerText = "";
    document.getElementById("error").style.display = "none";
}