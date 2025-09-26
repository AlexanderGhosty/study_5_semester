const form = document.getElementById('calcForm');
const opSelect = document.getElementById('op');
const op2Row = document.getElementById('op2Row');
const resultBox = document.getElementById('result');

function toggleOp2() {
  const op = opSelect.value;
  const unary = new Set(['sin', 'cos', 'tan', 'cot']);
  if (unary.has(op)) {
    op2Row.style.display = 'none';
  } else {
    op2Row.style.display = '';
  }
}

opSelect.addEventListener('change', toggleOp2);
toggleOp2();

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  resultBox.textContent = 'Вычисление…';

  const data = new URLSearchParams();
  data.append('op', form.op.value);
  data.append('op1', form.op1.value.trim());
  // Для унарных опер. сервер просто проигнорирует op2
  data.append('op2', (form.op2?.value ?? '').trim());

  try {
    const resp = await fetch('/api/calc', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
      body: data.toString(),
    });
    const json = await resp.json();
    if (json.ok) {
      resultBox.className = 'result ok';
      resultBox.textContent = `Результат: ${json.result}`;
    } else {
      resultBox.className = 'result err';
      resultBox.textContent = `Ошибка: ${json.error}`;
    }
  } catch (err) {
    resultBox.className = 'result err';
    resultBox.textContent = 'Сетевая ошибка';
  }
});