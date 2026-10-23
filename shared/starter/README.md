# Стартовый каркас

Одинаковый старт для всех подходов, чтобы сравнение было честным.

```bash
# из корня репозитория
impl=approaches/01-spec-driven/impl
cp shared/starter/CMakeLists.txt "$impl/"
mkdir -p "$impl/src"
cp shared/starter/src/main.cpp "$impl/src/"
```

Сборка:

```bash
cmake -S "$impl" -B "$impl/build" -G Ninja
cmake --build "$impl/build"
./check.sh "$impl"
```

`main.cpp` — заглушка, которая сразу возвращает код 2. Вся логика пишется с нуля выбранным подходом.

## Правила

- Не меняйте путь к бинарнику: `impl/build/logstat`.
- Можно менять структуру файлов как угодно, но `CMakeLists.txt` должен собирать `logstat`.
- Тесты складывайте в `impl/tests/`.
- Не копируйте реализацию из соседних подходов: цель — сравнить процесс, а не код.
