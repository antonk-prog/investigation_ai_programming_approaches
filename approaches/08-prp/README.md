# 08. PRP (Product Requirement Prompt)

[← к оглавлению](../../README.md)

## Суть

PRP = PRD + курированный контекст кодовой базы + runbook агента. Один плотный документ, который содержит всё, что нужно для реализации вертикального среза:

- цель и зачем;
- что входит и что не входит;
- конкретные файлы, паттерны, версии;
- план реализации по фазам;
- команды проверки.

Это «умный бриф», а не набор артефактов с жизненным циклом, как в SDD.

## Что понадобится

Полный фреймворк: https://github.com/Wirasm/PRPs-agentic-eng

Вариант для Claude Code:

```text
/plugin marketplace add Wirasm/PRPs-agentic-eng
/plugin install prp-core@prp-marketplace
```

Вариант для opencode — скопировать skills:

```bash
mkdir -p .opencode/skills
cp -r /path/to/PRPs-agentic-eng/.claude/skills/* .opencode/skills/
```

Вариант без установки — шаблон уже лежит рядом:

```
approaches/08-prp/template/PRP.md
```

## Настройка

```bash
cd ~/Projects/Personal/investigation_ai_programming_approaches
impl=approaches/08-prp/impl
cp shared/starter/CMakeLists.txt "$impl/"
mkdir -p "$impl/src"
cp shared/starter/src/main.cpp "$impl/src/"
mkdir -p "$impl/prps"
cp approaches/08-prp/template/PRP.md "$impl/prps/logstat.md"
```

## Промпт для старта

Если skills установлены:

```text
/prp-prd logstat по ТЗ ../../../docs/00-common-task.md
```

Затем:

```text
/prp-plan
/prp-implement
```

Если skills нет:

```text
Прочитай template/PRP.md и ТЗ ../../../docs/00-common-task.md.

Заполни PRP для logstat:
- Goal / Why / What / Non-goals
- Context: конкретные файлы, паттерны, ограничения
- Implementation Blueprint: фазы и шаги
- Validation: команды сборки и проверки, ожидаемые результаты

Сохрани в prps/logstat.md. Ничего не реализуй, пока я не проверю PRP.
```

После проверки:

```text
Реализуй строго по PRP. После каждой фазы запускай validation из PRP.
Если реальность расходится с PRP — обнови PRP и объясни расхождение.
```

## Ход работы

1. Соберите PRP. Он должен быть коротким: 1–3 страницы.
2. Проверьте раздел Context: там должны быть **точные** пути и паттерны, а не общие слова.
3. Проверьте Validation: команды должны быть выполнимыми.
4. Реализуйте по фазам.
5. Соберите и проверьте:

```bash
cd ~/Projects/Personal/investigation_ai_programming_approaches
./check.sh approaches/08-prp/impl
```

6. Обновите PRP по факту, если были отклонения.

## Что фиксировать

- Время на PRP.
- Сколько контекста пришлось добавлять после первой попытки.
- Сколько фаз совпало с реальностью.
- Помог ли PRP пройти всё с первого раза.
- Насколько документ понятен другому человеку.

## Критерии успеха

- [ ] PRP создан до реализации.
- [ ] В Context есть конкретные файлы и паттерны.
- [ ] Validation выполним и воспроизводим.
- [ ] 100% acceptance.
- [ ] PRP обновлён по факту.

## Типичные ошибки

- **Мегапромпт.** PRP разрастается до 20 страниц и перестаёт читаться.
- **Общий контекст.** «Используй хорошие практики» — бесполезно.
- **Нет валидации.** Без команд проверки PRP превращается в пожелание.
- **Игнорирование расхождений.** Реальность изменилась, а PRP нет.
- **Путать с SDD.** У PRP нет жизненного цикла и архива.

## Время

60–90 минут.

## Что сравнить с другими подходами

- Время до первого рабочего результата.
- Качество контекста против SDD.
- Стоимость поддержки одного файла против набора артефактов.
