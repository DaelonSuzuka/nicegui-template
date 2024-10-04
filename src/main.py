from nicegui import ui
from nicegui.events import KeyEventArguments
from command_palette import CommandPalette


@ui.page('/')
def index():
    async def handle_key(e: KeyEventArguments):
        if e.modifiers.shift and e.modifiers.ctrl and e.action.keydown and e.key == 'P':
            options = ['one', 'two']
            if result := await CommandPalette(options):
                ui.notify(result, position='bottom-right')

    ui.keyboard(on_key=handle_key)


ui.run(
    title='NiceGUI Template',
    uvicorn_reload_includes='*.vue',
    dark=True,
)
