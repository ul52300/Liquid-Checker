import PySimpleGUI as sg
import os
import math

# Version 1.0

sg.theme('DarkBlack')

layout = [[sg.Text("Choose a .prn file from SAR drive:", size=(26,1), font=('Times New Roman', 12, "bold")), sg.Input(key="-file_1-", size=(10,1)), sg.FileBrowse(size=(10,1))],
          [sg.Text("Input a target (MHz):", size=(26,1), font=('Times New Roman', 12, "bold")), sg.InputText(key="-target_1-", size=(10,1))],
          [sg.Txt('')],
          [sg.Text("Results", font=("Times New Roman", 14, "bold", "underline"))],
          [sg.Text("Target Frequency (MHz):", size=(20,1), font=('Times New Roman', 12)), sg.Push(), sg.Text('', size=(10, 1), font=('Times New Roman', 12, "bold"), key='input_1')],
          [sg.Text("Permitivity:", size=(20,1), font=('Times New Roman', 12)), sg.Push(), sg.Text('', size=(10, 1), font=('Times New Roman', 12, "bold"), key='input_2')],
          [sg.Text("Conductivity:", size=(20,1), font=('Times New Roman', 12)), sg.Push(), sg.Text('', size=(10, 1), font=('Times New Roman', 12, "bold"), key='input_3')],
          [sg.Txt('')],
          [sg.Button("Calculate", size=(10,1)), sg.Push(), sg.Button("Quit", size=(10,1))]
]

window = sg.FlexForm('Liquid Checker', default_button_element_size = (5,2), auto_size_buttons=False, grab_anywhere=False, resizable=False)
window.Layout(layout)

Result = ''
Other_Result = ''
Pressed_equal = False

while True:
    event, values = window.Read()
    
    if event == "Quit" or event == sg.WIN_CLOSED:
        break    
    elif event == "Calculate" and values["-target_1-"].strip() != '':
        
        target = float(values["-target_1-"])
        
        file_1 = values["-file_1-"]
        myfile = open(file_1, "rt")
        lines = myfile.readlines()
        
        low_freq = target - (target % 5)
        high_freq = target - (target % 5) + 5
        
        for line in lines:
            if line.find(str(int(low_freq * pow(10,6)))) != -1:
                rperm_cond_low = list((line.rstrip().split()[1],line.rstrip().split()[2]))
            if line.find(str(int(high_freq * pow(10,6)))) != -1:
                rperm_cond_high = list((line.rstrip().split()[1],line.rstrip().split()[2]))
                break
        
        if target < 20 or target > 6000:
            window['input_1'].update("N/A")
            window['input_2'].update("N/A")
            window['input_3'].update("N/A")    
        else:
            rpermitivity = ((high_freq - target)/(high_freq - low_freq))* float(rperm_cond_low[0]) + ((low_freq - target)/(low_freq - high_freq)) * float(rperm_cond_high[0])
            rconductivity = ((high_freq - target)/(high_freq - low_freq))* float(rperm_cond_low[1]) + ((low_freq - target)/(low_freq - high_freq)) * float(rperm_cond_high[1])
            conductivity = rconductivity * (2 * math.pi) * (target * pow(10,6)) * (8.854 * pow(10,-12))    
            window['input_1'].update(target)
            window['input_2'].update(round(rpermitivity,1))
            window['input_3'].update(round(conductivity,3))
            

        
window.close()