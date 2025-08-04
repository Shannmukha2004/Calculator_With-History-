let expression = '';

function press(val) {
    expression += val;
    document.getElementById('display').value = expression;
}

function clearDisplay() {
    expression = '';
    document.getElementById('display').value = '';
}
function deleteLast() {
      display.value = display.value.slice(0, -1);
    }

function calculate() {
    fetch('/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expression: expression })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('display').value = data.result;
        expression = '';
        loadHistory();
    });
}

function loadHistory() {
    fetch('/history')
        .then(res => res.json())
        .then(data => {
            let list = document.getElementById('historyList');
            list.innerHTML = '';
            data.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `${item[0]} = ${item[1]}`;
                list.appendChild(li);
            });
        });
}

window.onload = loadHistory;