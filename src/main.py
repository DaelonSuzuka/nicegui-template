from nicegui import ui
from nicegui.events import KeyEventArguments
from command_palette import CommandPalette


@ui.page('/')
def index():
    async def handle_key(e: KeyEventArguments):
        if e.modifiers.shift and e.modifiers.ctrl and e.action.keydown and e.key == 'P':
            cmd = CommandPalette()
            cmd.add_item('one')
            cmd.add_item('two')
            result = await cmd
            if result:
                ui.notify(result)

    ui.keyboard(on_key=handle_key)


ui.run(
    title='NiceGUI Template',
    dark=True,
)
