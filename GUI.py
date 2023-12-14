from SerializableFile import *
from Animal import *
import PySimpleGUI as sg
import operator


fAnimal = open('Animal.csv', 'a+')
listaAnimales = []

readAnimal('Animal.csv', listaAnimales)

def addAnimal(animalesLista, table_data, nuevoAnimal):
    animalesLista.append(nuevoAnimal)
    saveAnimal("Animal.csv", nuevoAnimal)
    table_data.append([nuevoAnimal.ID, nuevoAnimal.name, nuevoAnimal.owner,
                       nuevoAnimal.phone, nuevoAnimal.age, nuevoAnimal.posFile])


def deleteAnimal(animalesLista, table_data, row_index):
    pos_in_file = table_data[row_index][-1]
    animalBorrar = None
    for x in animalesLista:
        if x.animalInPos(pos_in_file):
            animalBorrar = x
            break
    if animalBorrar is not None:
        animalesLista.remove(animalBorrar)
        table_data.remove(table_data[row_index])
        animalBorrar.erased = True
        modifyAnimal(fAnimal, animalBorrar)


def updateAnimal(animalesLista, row_data, pos_in_file):
    updateAnimal = None
    for x in animalesLista:
        if x.animalInPos(pos_in_file):
            updateAnimal = x
            break
    if updateAnimal is not None:
        updateAnimal.setAnimal(row_data[1], row_data[2], row_data[3], row_data[4], row_data[5])
        modifyAnimal(fAnimal, updateAnimal)


def sortTable(table, cols):
    return table

def interface():    #interfaz gráfica
    sg.theme('Blue')
    sg.set_options(font=('Calibri', 10))
    table_data = []
    row_to_update = []

    for animal in listaAnimales:
        if not animal.erased:
            table_data.append([animal.ID, animal.name, animal.owner,
                               animal.phone, animal.age, animal.posFile])


    layout = [
        [sg.Push(), sg.Text('Animals CRUD'), sg.Push()],
        *[[sg.Text(text), sg.Push(), sg.Input(key=key)] for key, text in Animal.fields.items()],
        [sg.Push()] + [sg.Button(button) for button in ('Add', 'Delete', 'Modify', 'Clear')] + [sg.Push()],
        [sg.Table(values=table_data, headings=Animal.headings, max_col_width=50, num_rows=10,
                  display_row_numbers=False, justification='center', enable_events=True,
                  enable_click_events=True, vertical_scroll_only=False,
                  select_mode=sg.TABLE_SELECT_MODE_BROWSE, expand_x=True, bind_return_key=True, key='-Table-')],
        [sg.Button('Purge'), sg.Push(), sg.Button('Sort File')],
    ]

    window = sg.Window('Animals Management with Files', layout, finalize=True)
    window['-PosFile-'].update(disabled=True)
    window['-Table-'].bind("<Double-Button-1>", " Double")

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == 'Add':
            validate = True

            if validate:
                nuevoAnimal = Animal(values['-ID-'], values['-Name-'], values['-Owner-'],
                                            values['-Phone-'], values['-Age-'], -1)
                addAnimal(listaAnimales, table_data, nuevoAnimal)
                window['-Table-'].update(table_data)

        if event == 'Delete':
            if len(values['-Table-']) > 0:
                deleteAnimal(listaAnimales, table_data, values['-Table-'][0])
                window['-Table-'].update(table_data)

        if event == '-Table- Double':
            if len(values['-Table-']) > 0:
                row = values['-Table-'][0]
                window['-ID-'].update(disabled=True)
                window['-ID-'].update(str(table_data[row][0]))
                window['-Name-'].update(str(table_data[row][1]))
                window['-Owner-'].update(str(table_data[row][2]))
                window['-Phone-'].update(str(table_data[row][3]))
                window['-Age-'].update(str(table_data[row][4]))
                window['-PosFile-'].update(str(table_data[row][5]))

        if event == 'Clear':
            window['-ID-'].update(disabled=False)
            window['-ID-'].update('')
            window['-Name-'].update('')
            window['-Owner-'].update('')
            window['-Phone-'].update('')
            window['-Age-'].update('')
            window['-PosFile-'].update('')

        if event == 'Modify':
            validate = True
            if validate:
                for animal in listaAnimales:
                    if animal.animalInPos(values['-PosFile-']):
                        if values['-PosFile-']:
                            row_to_update = animal
                            row_to_update.setMotorcycle(values['-Name-'], values['-Owner-'], values['-Phone-'],
                                                        values['-Age-'])
                            break
                        else:
                            print("PosFile cannot be an empty string.")
                            break
                else:
                    print("PosFile not found in the motorcycles list.")

                updateAnimal(row_to_update)
                window['-Table-'].update(table_data)
                window['-ID-'].update(disabled=False)


        if isinstance(event, tuple):
            print(event)
            print(values)

            if event[0] == '-Table-':
                if event[2][0] == -1:
                    col_num_clicked = event[2][1]
                    table_data = sortTable(table_data, (col_num_clicked, 0))
                    window['-Table-'].update(table_data)

    window.close()
    interface()
    fAnimal.close()
