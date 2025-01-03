from text_editor_project.controllers.main_controller import MainController
from text_editor_project.models.text_model import *
from text_editor_project.views.curses_view import CursesView

class TextEditor:
    def __init__(self):
        model = TextModel()
        implemented_model : ITextModel
        implemented_model = model
        publisher : Publisher
        publisher = model
        implemented_model.append_line("\n")
        view = CursesView()
        publisher.add_subscriber(view)
        controller = MainController(implemented_model, view.adapter, view.cmd_buf)
        publisher.notify_subscribers()  # Уведомляем подписчиков об изменении
        while True:
            controller.handle_input(controller.adapter.get_key_input())
