import logging
from factories.scene_factory import SceneFactory
from models.app_config import AppConfig
from providers.config_provider import ConfigProvider
from utils.state import AppState
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from cli.tui.scene_type import SceneType
from cli.tui.forms.contact_form import ContactForm
from cli.tui.forms.note_form import NoteForm
from cli.tui.views.dashboard_view import DashboardView
from cli.tui.views.contact_grid_view import ContactGridView
from cli.tui.views.note_grid_view import NoteGridView
from cli.tui.views.birthday_grid_view import BirthdayGridView

"""Конфігурація застосунку через відповідний провайдер"""
app_config: AppConfig | None = ConfigProvider.load()

"""Конфігурація логування у файл"""
logging.basicConfig(filename="assistant.log",
                    level=app_config.log_level if app_config else logging.INFO,
                    filemode="w",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")

"""Контейнер стану застосунку"""
app_state = AppState(app_config)

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

if __name__ == "__main__":
    logging.info("Starting personal assistant...")
    Screen.wrapper(demo, arguments=[app_state])
