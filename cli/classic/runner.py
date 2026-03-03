from cli.classic.colors import Colors
from cli.classic.dispatcher import EXIT_SENTINEL, CommandDispatcher
from utils.state import AppState


def run(app_state: AppState) -> None:
    """Головний цикл класичного режиму: читає рядки, виконує команди через CommandDispatcher, виводить результат."""
    dispatcher = CommandDispatcher(app_state)
    while True:
        try:
            line = input(Colors.accent("➜ "))
        except (EOFError, KeyboardInterrupt):
            break
        cmd, args = CommandDispatcher.parse_line(line)
        if not cmd:
            continue
        result = dispatcher.run(cmd, args)
        if result is EXIT_SENTINEL:
            break
        print(result)
