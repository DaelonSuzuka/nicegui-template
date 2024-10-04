from nicegui import ui, app

# import auth


@ui.page('/')
def index():
    ui.label('hi')


ui.run(
    title='NiceGUI Template',
    dark=True,
)
