from nicegui import ui, app

# import auth


@ui.page('/')
def index():
    ui.label('hi')


ui.run(title='NiceGUI Template', 
    #    host='0.0.0.0', port=8081, 
       dark=True)
