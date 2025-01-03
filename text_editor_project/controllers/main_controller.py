from text_editor_project.controllers.controller_states import NavigationState, InsertState, SearchState, CommandState
from abc import ABC, abstractmethod


class ICAdapter(ABC):
    @abstractmethod
    def get_key_input(self):
        pass

class MainController:
    def __init__(self, model, adapter, cmd_buf):
        self.model = model
        self.state = NavigationState(self)  # Начальное состояние
        self.model.controller_state_str = "NAV"
        self.adapter : ICAdapter
        self.adapter = adapter  # Для работы с curses
        self.cmd_buf = cmd_buf

    def set_state(self, state):
        self.state = state
        if isinstance(state, NavigationState):
            self.model.controller_state_str = "NAV"
        elif isinstance(state, InsertState):
            self.model.controller_state_str = "INS"
        elif isinstance(state, SearchState):
            self.model.controller_state_str = "SRC"
        elif isinstance(state, CommandState):
            self.model.controller_state_str = "CMD"

    def handle_input(self, key):
        if self.state:
            self.state.handle_input(key)
            self.model.notify_subscribers()