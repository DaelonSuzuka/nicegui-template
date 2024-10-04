from nicegui import ui


@ui.page('/')
def index():
    ui.label('hi')


ui.run(
    title='NiceGUI Template',
    dark=True,
)
