

executables = [cx_Freeze.Executable('my_app.py')]

cx_Freeze.setup(
    name='MyApp',
    options={'build_exe': {'packages': ['tkinter'],
                           'include_files': ['my_app.ico']}},
    executables=executables
)
