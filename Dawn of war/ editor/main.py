import re


def change_key(text, command, new_key):
    """Изменяет назначение клавиши для указанной команды."""

    pattern = rf'(^\s*{re.escape(command)}\s*=\s*")[^"]*(")'

    updated_text, count = re.subn(
        pattern,
        rf'\g<1>{new_key}\g<2>',
        text,
        count=1,
        flags=re.MULTILINE,
    )

    if count == 0:
        raise ValueError(f"Команда {command!r} не найдена")

    return updated_text


def main():
    with open("KEYDEFAULTS_my.lua", "r", encoding="utf-8") as file:
        keys = file.read()

    command = "attackmove"
    new_key = "W"

    try:
        updated_keys = change_key(keys, command, new_key)
    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    with open("KEYDEFAULTS_modified.lua", "w", encoding="utf-8") as file:
        file.write(updated_keys)

    print(f"Команда {command!r} изменена на клавишу {new_key!r}")
    print("Изменённый файл сохранён в KEYDEFAULTS_modified.lua")


if __name__ == "__main__":
    main()
