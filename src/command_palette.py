from nicegui import ui
from nicegui.events import GenericEventArguments, ValueChangeEventArguments


class CommandTable(ui.table):
    def __init__(self) -> None:
        columns = [
            {
                'name': 'value',
                'label': 'value',
                'field': 'value',
                'align': 'left',
                'sortable': True,
            }
        ]
        super().__init__(rows=[], columns=columns, row_key='id')
        self.classes('w-full')
        self.props('hide-header')
        self.items = []
        self.on('@selection', self.row_clicked)
        self.current_selection = 0

    def select_up(self):
        self.current_selection = max(self.current_selection - 1, 0)
        self.set_selection()

    def select_down(self):
        self.current_selection = min(self.current_selection + 1, len(self.items) - 1)
        self.set_selection()

    def set_selection(self):
        self.selected = [self.items[self.current_selection]]

    def get_selection(self):
        return self.selected[0]['value']

    def add_item(self, value):
        row = {'value': value, 'id': len(self.items)}
        self.items.append(row)
        self.add_row(row)

    def sort(self, new_value):
        self.current_selection = 0
        self.set_selection()
        # sort list and update highlighting
        pass

    def row_clicked(self, e):
        ui.notify(e)


class CommandPalette(ui.dialog):
    def __init__(self) -> None:
        super().__init__(value=True)

        self.props('transition-duration=0')

        with self, ui.card().classes('absolute top-10 w-1/2 px-2').tight():
            self.text = ui.input(on_change=self.on_change).classes('w-full')
            self.table = CommandTable()

        self.text.run_method('select')
        self.on('keydown', self.handle_key)

    def on_change(self, e: ValueChangeEventArguments):
        self.table.sort(e.value)

    def add_item(self, value: str):
        self.table.add_item(value)

        self.text.set_autocomplete(self.table.items)

    def add_items(self, values: list[str] | dict[str, str]):
        if isinstance(values, list):
            for value in values:
                self.table.add_item(value)
        if isinstance(values, dict):
            for k, v in values.items():
                self.table.add_item(v)

        self.text.set_autocomplete(self.table.items)

    def handle_key(self, e: GenericEventArguments):
        if e.args['key'] == 'Enter':
            self.submit(self.table.get_selection())
        if e.args['key'] == 'ArrowUp':
            self.table.select_up()
        if e.args['key'] == 'ArrowDown':
            self.table.select_down()

    def __await__(self):
        self.table.set_selection()
        return super().__await__()
