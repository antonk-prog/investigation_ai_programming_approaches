# 06. BDD / Example-Driven

[← к оглавлению](../../README.md)

## Суть

Требования формулируются конкретными примерами на языке предметной области:

```gherkin
Scenario: Фильтр по модулю
  Given журнал sample.csv
  When я запускаю logstat с аргументом "--module can"
  Then код возврата 0
  And в выводе 4 записи
```

Сценарии пишутся до кода и становятся приёмочными тестами. Это мост между «что хочет заказчик» и «что проверяет машина».

## Что понадобится

```bash
python3 -m pip install --user behave
behave --version
```

`behave` будет чёрным ящиком вызывать собранный `build/logstat`. Это проще и надёжнее, чем Cucumber-cpp, и не добавляет зависимостей в C++.

## Настройка

```bash
cd ~/Projects/Personal/investigation_ai_programming_approaches
impl=approaches/06-bdd-example-driven/impl
cp shared/starter/CMakeLists.txt "$impl/"
mkdir -p "$impl/src"
cp shared/starter/src/main.cpp "$impl/src/"
mkdir -p "$impl/features/steps"
```

Структура:

```
impl/
├── build/logstat
├── features/
│   ├── logstat.feature
│   └── steps/
│       └── logstat_steps.py
└── src/
```

## Промпт для старта

```text
Прочитай ТЗ ../../../docs/00-common-task.md и фикстуры ../../../shared/fixtures/.

Работаем через BDD.
1. Напиши features/logstat.feature со сценариями на русском (Given/When/Then) для всех критериев приёмки.
2. Напиши steps/logstat_steps.py, который запускает build/logstat через subprocess и проверяет код возврата, stdout, stderr.
3. Реализацию пока не пиши.
4. Запусти behave: сценарии должны падать.
5. Затем реализуй logstat, пока все сценарии не станут зелёными.
```

Пример шага:

```python
import subprocess
from pathlib import Path
from behave import given, when, then

BIN = Path(__file__).resolve().parents[2] / "build" / "logstat"
FIX = Path(__file__).resolve().parents[5] / "shared" / "fixtures"

@given('журнал "{name}"')
def step_journal(context, name):
    context.input = str(FIX / name)

@when('я запускаю logstat с аргументом "{arg}"')
def step_run(context, arg):
    context.proc = subprocess.run(
        [str(BIN), context.input, arg],
        capture_output=True, text=True,
    )

@then("код возврата {code:d}")
def step_rc(context, code):
    assert context.proc.returncode == code, context.proc.stderr
```

Путь `parents[5]` проверьте под свою структуру: `steps → features → impl → 06-bdd-example-driven → approaches → корень`.

## Ход работы

1. Выпишите сценарии из критериев приёмки. Один сценарий = один пример поведения.
2. Сначала сценарии должны падать — это нормально.
3. Реализуйте до зелёного.
4. Добавьте 2–3 краевых сценария (пустой файл, плохая дата, кавычки).
5. Соберите и проверьте:

```bash
cd ~/Projects/Personal/investigation_ai_programming_approaches
./check.sh approaches/06-bdd-example-driven/impl
```

## Что фиксировать

- Число сценариев и шагов.
- Сколько шагов переиспользовались.
- Сколько времени ушло на step definitions против реализации.
- Насколько сценарии понятны не-программисту.
- Сколько сценариев пришлось менять.

## Критерии успеха

- [ ] Сценарии написаны до реализации.
- [ ] Сценарии читаются как требования.
- [ ] Все сценарии зелёные.
- [ ] 100% acceptance.

## Типичные ошибки

- **Слишком техничные шаги.** «Вызвать метод parse()» — это не BDD.
- **Взрыв step definitions.** Каждый шаг уникален и не переиспользуется.
- **BDD ради BDD.** Если сценарии никто не читает, достаточно обычных тестов.
- **Тестирование UI вместо поведения.** Для CLI это соблазнительно.
- **Забыть про отрицательные сценарии.** Ошибки — тоже поведение.

## Время

90–120 минут.

## Что сравнить с другими подходами

- Понятность требований для не-разработчика.
- Стоимость поддержки сценариев.
- Сколько дефектов поймали сценарии.
