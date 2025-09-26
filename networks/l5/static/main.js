const form = document.getElementById('calcForm');
const exprInput = document.getElementById('expr');
const resultInput = document.getElementById('result');

// Примеры поддерживаемых выражений:
//  a+b, a-b, a*b, a/b, a^b, root(a,b), sin(a), cos(a), tan(a), cot(a)
// Пробелы допускаются.

function parseExpression(expr) {
  const s = expr.trim().toLowerCase();
  if (!s) return null;

  // root(a,b)
  let m = s.match(/^root\(([-+]?\d+(?:\.\d+)?),\s*([-+]?\d+(?:\.\d+)?)\)$/);
  if (m) return { op: 'root', op1: m[1], op2: m[2] };

  // sin(a) / cos(a) / tan(a) / cot(a)
  m = s.match(/^(sin|cos|tan|cot)\(([-+]?\d+(?:\.\d+)?)\)$/);
  if (m) return { op: m[1], op1: m[2], op2: '' };

  // Бинарные операции с инфиксными символами
  // a ^ b (степень)
  m = s.match(/^([-+]?\d+(?:\.\d+)?)\s*\^\s*([-+]?\d+(?:\.\d+)?)$/);
  if (m) return { op: 'pow', op1: m[1], op2: m[2] };

  // a + b
  m = s.match(/^([-+]?\d+(?:\.\d+)?)\s*\+\s*([-+]?\d+(?:\.\d+)?)$/);
  if (m) return { op: 'add', op1: m[1], op2: m[2] };

  // a - b
  m = s.match(/^([-+]?\d+(?:\.\d+)?)\s*-\s*([-+]?\d+(?:\.\d+)?)$/);
  if (m) return { op: 'sub', op1: m[1], op2: m[2] };

  // a * b (в том числе ×)
  m = s.match(/^([-+]?\d+(?:\.\d+)?)\s*[\*×]\s*([-+]?\d+(?:\.\d+)?)$/);
  if (m) return { op: 'mul', op1: m[1], op2: m[2] };

  // a / b (в том числе ÷)
  m = s.match(/^([-+]?\d+(?:\.\d+)?)\s*[\/÷]\s*([-+]?\d+(?:\.\d+)?)$/);
  if (m) return { op: 'div', op1: m[1], op2: m[2] };

  return null;
}

let controller = null;
async function compute(expr) {
  const parsed = parseExpression(expr);
  if (!parsed) {
    resultInput.classList.remove('ok', 'err');
    resultInput.value = '';
    return;
  }

  // Отменяем предыдущий запрос, если пользователь продолжает ввод
  if (controller) controller.abort();
  controller = new AbortController();

  const data = new URLSearchParams();
  data.append('op', parsed.op);
  data.append('op1', parsed.op1 ?? '');
  data.append('op2', parsed.op2 ?? '');

  try {
    const resp = await fetch('/api/calc', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
      body: data.toString(),
      signal: controller.signal,
    });
    const json = await resp.json();
    if (json.ok) {
      resultInput.classList.add('ok');
      resultInput.classList.remove('err');
      resultInput.value = String(json.result);
    } else {
      resultInput.classList.add('err');
      resultInput.classList.remove('ok');
      resultInput.value = `Ошибка: ${json.error}`;
    }
  } catch (err) {
    if (err?.name === 'AbortError') return; // игнорируем отмену
    resultInput.classList.add('err');
    resultInput.classList.remove('ok');
    resultInput.value = 'Сетевая ошибка';
  }
}

// Запуск вычисления по мере ввода
exprInput.addEventListener('input', (e) => compute(e.target.value));
// Первичный парс, если поле предзаполнено
if (exprInput.value) compute(exprInput.value);