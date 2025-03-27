async function askQuestion() {
    const question = document.getElementById('question').value;
    const response = await fetch('/ask', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({question})
    });
    const data = await response.json();
    document.getElementById('answer').innerText = data.answer;

    const historyEl = document.getElementById('history');
    historyEl.innerHTML = '';
    data.history.forEach(item => {
        const li = document.createElement('li');
        li.innerText = `Q: ${item.question} | A: ${item.answer}`;
        historyEl.appendChild(li);
    });
}

async function startQuiz() {
    const response = await fetch('/quiz', { method: 'POST' });
    const data = await response.json();
    alert("Quiz Started! First Question: " + data.questions[0]);
}
