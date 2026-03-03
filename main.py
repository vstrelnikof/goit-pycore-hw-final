import os
import platform
import logging
from models.app_config import AppConfig
from providers.config_provider import ConfigProvider
from utils.state import AppState

# Тільки для Windows терміналу
if platform.system() == "Windows":
    # Виставляємо кодування UTF-8 (65001)
    os.system('chcp 65001 > nul 2>&1')
    os.system('cls')
else:
    os.system('clear')

logging.basicConfig(
    filename="assistant.log",
    level=logging.INFO,
    filemode="a",
    datefmt="%Y-%m-%d %H:%M:%S",
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
)
app_config: AppConfig = ConfigProvider.load()
logging.root.setLevel(app_config.log_level)
logger = logging.getLogger(__name__)

# Контейнер стану застосунку
app_state = AppState(app_config)

if app_config.classic:
    import colorama
    colorama.init(autoreset=True)
    from cli.classic import run
    logger.info("Starting personal assistant (classic mode)...")
    run(app_state)
else:
    from asciimatics.screen import Screen
    from asciimatics.scene import Scene
    from factories.scene_factory import SceneFactory
    from enums.scene_type import SceneType
    from cli.tui.forms.contact_form import ContactForm
    from cli.tui.forms.note_form import NoteForm
    from cli.tui.views.dashboard_view import DashboardView
    from cli.tui.views.contact_grid_view import ContactGridView
    from cli.tui.views.note_grid_view import NoteGridView
    from cli.tui.views.birthday_grid_view import BirthdayGridView

    def demo(screen: Screen, state: AppState):
        """Ініціалізатор asciimatics"""
        scenes: list[Scene] = SceneFactory.createScenes({
            SceneType.MAIN: DashboardView(screen, state),
            SceneType.CONTACT_FORM: ContactForm(screen, state),
            SceneType.CONTACTS_GRID: ContactGridView(screen, state),
            SceneType.BIRTHDAYS_GRID: BirthdayGridView(screen, state),
            SceneType.NOTE_FORM: NoteForm(screen, state),
            SceneType.NOTES_GRID: NoteGridView(screen, state),
        })
        screen.play(scenes,
                    stop_on_resize=True,
                    repeat=True)

    logger.info("Starting personal assistant...")
    Screen.wrapper(demo, arguments=[app_state])