# Инструменты: что уже есть и что ставить

## Проверено в этом окружении

| Инструмент | Версия | Статус |
|---|---|---|
| opencode | 1.19.3 | установлен |
| OpenSpec CLI | 1.13.1 | установлен |
| CMake | 3.31.6 | установлен |
| Ninja | 1.12.1 | установлен |
| GCC / G++ | 14.2.0 | установлен |
| Clang++ | 19.1.7 | установлен |
| Node.js / npm / npx | 22.23.3 / 10.9.9 | установлены |
| Python | 3.13.5 | установлен |
| Git | 2.47.3 | установлен |

Почти всё для базовых экспериментов уже есть. Доставлять нужно только инструменты конкретных подходов.

---

## Что ставить под каждый подход

| # | Подход | Что установить | Команда |
|---|---|---|---|
| 01 | Spec-Driven (OpenSpec) | уже есть | `openspec --version` |
| 02 | Common Ground | уже есть (команда opencode) | `/common-ground` |
| 03 | Conductor | плагин opencode | `opencode-conductor@latest` в `opencode.json` |
| 04 | Plan-first | ничего | режим Plan в opencode |
| 05 | Agentic TDD | опционально gtest | FetchContent или `libgtest-dev` |
| 06 | BDD | behave | `pip install behave` |
| 07 | Memory Bank | ничего (опц. Cline) | — |
| 08 | PRP | skills/шаблон | шаблон уже лежит в папке |
| 09 | BMAD | Node 20.12+, Python 3.10+, uv | `npx bmad-method install` |
| 10 | Eval-Driven | ничего (опц. promptfoo) | чекер уже есть |
| 11 | Multi-agent | ничего | конфиги агентов уже лежат |
| 12 | ADR | ничего (опц. adr-tools) | шаблон уже лежит |
| 13 | Vibe coding | ничего | — |

---

## 01. OpenSpec

Уже установлен глобально. Дополнительно в проекте:

```bash
cd approaches/01-spec-driven/impl
openspec init --tools opencode
```

Проверка:

```bash
openspec --version
openspec list
```

В этом окружении также подключён плагин `@devcxl/opencode-spec`, который даёт команды `/opsx-propose`, `/opsx-apply`, `/opsx-archive`. **Не смешивайте** два способа в одном эксперименте: либо команды `/opsx-*`, либо CLI `openspec`.

Документация: https://openspec.dev

---

## 02. Common Ground

Команда уже лежит в `~/.config/opencode/commands/common-ground.md`.

```text
/common-ground
```

Она написана под Claude (`AskUserQuestion`). Если в opencode интерактивный опрос не запустится — просто попросите: «проведи common-ground вручную и задай мне вопросы». Результат сохраняется в:

```
~/.config/opencode/common-ground/<project-id>/COMMON-GROUND.md
```

Важно: это не методология реализации. После выравнивания допущений реализуйте задачу обычным plan-first.

---

## 03. Conductor

Плагин сообщества. Версию лучше зафиксировать.

Создайте `approaches/03-context-driven-conductor/impl/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["opencode-conductor@latest"]
}
```

Перезапустите opencode в этой папке и выполните:

```text
/conductor-setup
/conductor-new-track
/conductor-implement
```

Плагин создаст `conductor/product.md`, `tech-stack.md`, `workflow.md`, `tracks.md`.

Если плагин не подхватился — проверьте, что opencode загружает проектный конфиг, и посмотрите лог. Альтернатива: клонировать `https://github.com/NocturnLabs/opencode-conductor` и собрать локально.

---

## 04. Plan-first

Ничего ставить не нужно.

В opencode переключитесь на агент **Plan** (Tab) или явно напишите:

```text
Составь план реализации. Файлы не меняй. Сначала задай вопросы, если что-то неоднозначно.
```

После одобрения переключитесь на **Build** и попросите выполнить план по шагам.

---

## 05. Agentic TDD

Вариант A — без зависимостей: маленький самописный test runner на `assert`.

Вариант B — GoogleTest через FetchContent (нужна сеть при первой сборке):

```cmake
include(FetchContent)
FetchContent_Declare(
    googletest
    URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.tar.gz
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)
enable_testing()
```

Вариант C — системный пакет:

```bash
sudo apt install libgtest-dev
```

Для эксперимента достаточно A: важно не наличие фреймворка, а цикл red-green-refactor.

---

## 06. BDD

```bash
python3 -m pip install --user behave
# или, если используете uv:
uv tool install behave
```

Проверка: `behave --version`.

`behave` будет чёрным ящиком вызывать собранный `build/logstat` через `subprocess`. Это удобнее, чем Cucumber-cpp, и не добавляет зависимостей в C++.

---

## 07. Memory Bank

Ставить ничего не нужно. Опционально — расширение **Cline** для VS Code, если хотите попробовать оригинальный Memory Bank.

В opencode роль «ритуала» выполняет проектный `AGENTS.md` с правилом:

```text
В начале каждой сессии прочитай memory-bank/*.md.
В конце сессии обнови activeContext.md и progress.md.
```

---

## 08. PRP

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

Вариант без установки — использовать шаблон `approaches/08-prp/template/PRP.md` и попросить агента заполнить его.

---

## 09. BMAD-METHOD

Требования: Node.js 20.12+, Python 3.10+, `uv`.

```bash
# uv, если ещё нет
curl -LsSf https://astral.sh/uv/install.sh | sh

# установка стабильной версии
cd approaches/09-bmad-method/impl
npx bmad-method install
```

Проверить поддерживаемые инструменты:

```bash
npx bmad-method install --list-tools
```

Стабильная ветка — v6.12; v7 в alpha и может ломаться. Для эксперимента берите стабильную.

Дальше в чате:

```text
bmad-help what should I do first?
bmad-build
```

Учтите: BMAD создаёт `_bmad/` и `_bmad-output/`. Это нормально, они уже в `.gitignore`.

---

## 10. Eval-Driven

Обязательный инструмент уже есть — `shared/acceptance/check.py`. Это и есть eval-harness для детерминированной задачи.

Опционально, если хотите оценивать качество кода/промптов через LLM:

```bash
npx promptfoo@latest init --example getting-started
npx promptfoo@latest eval
npx promptfoo@latest view
```

Promptfoo требует API-ключ и тратит токены. Для базового эксперимента не обязателен.

---

## 11. Multi-agent

Ставить ничего не нужно. Примеры конфигов лежат в `approaches/11-multi-agent/impl/.opencode/agents/`.

Использование:

```text
Используй субагента planner для исследования, затем implementer, затем reviewer.
```

Можно также обойтись встроенным `Task` (агенты `explore` и `general`).

---

## 12. ADR

Ставить ничего не нужно. Шаблон: `approaches/12-adr-driven/impl/docs/adr/0000-template.md`.

Опционально `adr-tools` (только macOS/Homebrew и shell-скрипты) — для эксперимента не нужен.

---

## 13. Vibe coding

Ставить ничего не нужно. Только дисциплина: таймбокс, песочница, никаких секретов и продакшена.

---

## Общие требования

- Один и тот же провайдер и модель для всех подходов.
- Модель и версию записывайте в `WORKLOG.md`.
- Для воспроизводимости фиксируйте версии инструментов.
- Не ставьте всё сразу: ставьте по мере прохождения подходов.
