from nicegui import ui
from nicegui.events import GenericEventArguments, ValueChangeEventArguments
from difflib import SequenceMatcher


class CommandTable(ui.table, component='command_table.vue'):
    def __init__(self) -> None:
        columns = [
            {'name': 'value', 'label': 'value', 'field': 'value', 'align': 'left'},
            # {'name': 'ratio', 'label': 'ratio', 'field': 'ratio', 'align': 'right'},
        ]
        super().__init__(rows=[], columns=columns, row_key='id')
        self.items = []
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

    def add_item(self, value: str, display: str = None):
        row = {
            'value': value,
            'display': display if display else value,
            'id': len(self.items),
            'ratio': 1,
        }
        self.items.append(row)
        self.add_row(row)

    def sort(self, target: str):
        if target:
            for item in self.items:
                item['ratio'] = SequenceMatcher(a=item['value'], b=target).ratio()
                if target not in item['value']:
                    item['ratio'] = 0
        else:
            # if target is "", match everything
            for item in self.items:
                item['ratio'] = 1

        self.items.sort(key=lambda x: x['ratio'], reverse=True)

        items = filter(lambda x: x['ratio'] > 0, self.items)

        self.update_rows(items, clear_selection=False)
        self.current_selection = 0
        self.set_selection()


class CommandPalette(ui.dialog):
    def __init__(self, options: list[str] | dict[str, str] = None) -> None:
        super().__init__(value=True)

        self.props('transition-duration=0')

        with self, ui.card().classes('absolute top-10 w-1/2').tight():
            self.text = ui.input(on_change=self.on_change).classes('w-full px-2')
            self.table = CommandTable()

        self.text.run_method('select')
        self.on('keydown', self.handle_key)
        self.table.on('row_clicked', self.row_clicked)

        if options is not None:
            self.add_items(options)

    def on_change(self, e: ValueChangeEventArguments):
        self.table.sort(e.value)

    def row_clicked(self, e: GenericEventArguments):
        value = e.args['value']
        self.submit(value)

    def add_item(self, value: str, display: str = None):
        self.table.add_item(value, display)

    def add_items(self, values: list[str] | dict[str, str]):
        if isinstance(values, list):
            for value in values:
                self.table.add_item(value)
        if isinstance(values, dict):
            for k, v in values.items():
                self.table.add_item(k, v)

    def handle_key(self, e: GenericEventArguments):
        if e.args['key'] == 'Enter':
            self.submit(self.table.get_selection())
        if e.args['key'] == 'ArrowUp':
            self.table.select_up()
        if e.args['key'] == 'ArrowDown':
            self.table.select_down()

    def __await__(self):
        self.table.set_selection()

        items = list(map(lambda x: x['value'], self.table.items))
        self.text.set_autocomplete(items)

        return super().__await__()
