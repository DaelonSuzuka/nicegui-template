from nicegui import ui


@ui.page('/')
def index():
    ui.label('Hello!')


ui.run(
    title='NiceGUI Template',
    dark=True,
)
