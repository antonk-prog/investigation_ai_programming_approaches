# Исследование подходов к AI-разработке

Практический полигон: **одна и та же задача на C++** реализуется 13 разными подходами. Цель — не получить CSV-парсер, а понять, какой процесс даёт лучший результат в условиях Инкомсистем.

## Быстрый старт

```bash
# 1. Прочитайте ТЗ и правила
less docs/00-common-task.md
less docs/02-experiment-protocol.md

# 2. Выберите подход и откройте его README
less approaches/01-spec-driven/README.md

# 3. Подготовьте стартовый каркас
impl=approaches/01-spec-driven/impl
cp shared/starter/CMakeLists.txt "$impl/"
mkdir -p "$impl/src"
cp shared/starter/src/main.cpp "$impl/src/"

# 4. Соберите и проверьте (пока будут FAIL — это нормально)
cmake -S "$impl" -B "$impl/build" -G Ninja
cmake --build "$impl/build"
./check.sh "$impl"

# 5. Работайте по README подхода, заполняйте WORKLOG.md
# 6. После — results/NN-<name>.md и docs/04-comparison.md
```

## Карта подходов

| # | Подход | Папка | Что проверяем | Установка |
|---|---|---|---|---|
| 01 | Spec-Driven (OpenSpec) | [01-spec-driven](approaches/01-spec-driven/README.md) | дисциплина требований, трассируемость | уже есть |
| 02 | Common Ground | [02-common-ground](approaches/02-common-ground/README.md) | вскрытие неявных допущений | уже есть |
| 03 | Context-Driven / Conductor | [03-context-driven-conductor](approaches/03-context-driven-conductor/README.md) | преемственность контекста между сессиями | плагин |
| 04 | Plan-first | [04-plan-first](approaches/04-plan-first/README.md) | дешёвая коррекция до кода | нет |
| 05 | Agentic TDD | [05-agentic-tdd](approaches/05-agentic-tdd/README.md) | петля обратной связи через тесты | опц. gtest |
| 06 | BDD / Example-Driven | [06-bdd-example-driven](approaches/06-bdd-example-driven/README.md) | требования как примеры | behave |
| 07 | Memory Bank | [07-memory-bank](approaches/07-memory-bank/README.md) | память между сессиями | нет |
| 08 | PRP | [08-prp](approaches/08-prp/README.md) | один плотный контекст-пакет на фичу | опц. skills |
| 09 | BMAD-METHOD | [09-bmad-method](approaches/09-bmad-method/README.md) | полный agile-процесс агентами | npx |
| 10 | Eval-Driven | [10-eval-driven](approaches/10-eval-driven/README.md) | измерение результата, регрессии | чекер |
| 11 | Multi-agent | [11-multi-agent](approaches/11-multi-agent/README.md) | специализация и параллелизм | нет |
| 12 | ADR-driven | [12-adr-driven](approaches/12-adr-driven/README.md) | решения как ограничения для агента | нет |
| 13 | Vibe coding | [13-vibe-coding](approaches/13-vibe-coding/README.md) | контрольная группа: хаос vs процесс | нет |

## Рекомендуемый порядок

Не проходите всё подряд. Идите волнами:

**Волна 1 — база (дешёво, эффект сразу)**
1. `04-plan-first`
2. `02-common-ground`
3. `12-adr-driven`

**Волна 2 — процесс**
4. `01-spec-driven`
5. `03-context-driven-conductor`
6. `07-memory-bank`

**Волна 3 — качество**
7. `05-agentic-tdd`
8. `06-bdd-example-driven`
9. `10-eval-driven`

**Волна 4 — тяжёлое и контроль**
10. `08-prp`
11. `11-multi-agent`
12. `09-bmad-method`
13. `13-vibe-coding` (последним, как контрольная группа)

## Состав репозитория

```
.
├── docs/
│   ├── 00-common-task.md          # ТЗ, одинаковое для всех
│   ├── 01-tooling.md              # что установить
│   ├── 02-experiment-protocol.md  # правила честного сравнения
│   ├── 03-evaluation-rubric.md    # как оценивать
│   ├── 04-comparison.md           # сводная таблица
│   └── 05-company-rollout.md      # как перенести в компанию
├── shared/
│   ├── fixtures/                  # входные CSV
│   ├── acceptance/check.py        # автоматическая приёмка
│   └── starter/                   # одинаковый каркас для всех
├── approaches/NN-name/
│   ├── README.md                  # теория + установка + промпты + шаги
│   ├── WORKLOG.md                 # журнал эксперимента
│   ├── impl/                      # здесь пишется код
│   └── notes/                     # артефакты подхода
├── results/                       # карточки результатов
└── check.sh                       # обёртка над чекером
```

## Прогресс

- [ ] 01 Spec-Driven
- [ ] 02 Common Ground
- [ ] 03 Conductor
- [ ] 04 Plan-first
- [ ] 05 Agentic TDD
- [ ] 06 BDD
- [ ] 07 Memory Bank
- [ ] 08 PRP
- [ ] 09 BMAD
- [ ] 10 Eval-Driven
- [ ] 11 Multi-agent
- [ ] 12 ADR-driven
- [ ] 13 Vibe coding

## Главное правило

Сравниваем **процессы**, а не людей и не модели. Одна задача, одна модель, одинаковый старт, честный журнал.
