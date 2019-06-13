from Tkinter import *
import random
from Tkinter import SINGLE, MULTIPLE, END
import tkFont


class Patient_info_gui_opt(object):
    def __init__(self, master, title, choices_list, is_fetal=False):

        font_small = tkFont.Font(family='Helvetica', size=11)
        font_big = tkFont.Font(family='Helvetica', size=14)
        font_header = tkFont.Font(family='Helvetica', size=15, underline=1)

        self.master = master

        self.check_box_value_F = BooleanVar()
        self.check_box_value_M = BooleanVar()

        self.additional_diagnoses_value = []

        self.text_box_due = None

        self.list = choices_list

        self.modalPane = Toplevel(self.master)
        self.modalPane.transient(self.master)
        self.modalPane.grab_set()
        self.modalPane.title(title)
        Label(self.modalPane, text="Optional Patient Info", font=font_header).pack(padx=5, pady=10)



        list_frame = Frame(self.modalPane)
        list_frame.pack(side=TOP, padx=10, pady=10)
        Label(list_frame, text="Additional Diagnoses?", font=font_big).pack()
        self.list_box_additional = Listbox(list_frame, selectmode=MULTIPLE, width=40, height=12, yscrollcommand=True)
        for item in self.list:
            self.list_box_additional.insert(END, item)
        self.list_box_additional.pack(side=LEFT, fill=Y)

        if is_fetal:
            text_frame = Frame(self.modalPane)
            text_frame.pack(side=TOP, padx=10, pady=10)
            Label(text_frame, text="Enter the Birth Due Date", font=font_big).pack()
            self.text_box_due = Text(text_frame, width=40, height=2)
            self.text_box_due.pack(side=TOP)

            check_box_frame = Frame(self.modalPane)
            check_box_frame.pack(side=TOP, padx=10, pady=10)
            self.check_box_value_F.set(False)
            self.check_box_value_M.set(False)
            self.check_box_F = Checkbutton(check_box_frame, text='Female',
                                         variable=self.check_box_value_F, font=font_small)
            self.check_box_F.pack(side=TOP, pady=5)
            self.check_box_M = Checkbutton(check_box_frame, text='Male',
                                         variable=self.check_box_value_M, font=font_small)
            self.check_box_M.pack(side=TOP, pady=5)

        text_frame = Frame(self.modalPane)
        text_frame.pack(side=TOP, padx=10, pady=10)
        Label(text_frame, text="Notes", font=font_small).pack()
        self.text_box_notes = Text(text_frame, width=40, height=2)
        self.text_box_notes.pack(side=TOP)

        button_frame = Frame(self.modalPane)
        button_frame.pack(side=BOTTOM, padx=10, pady=10)
        self.choose_button = Button(button_frame, text="OK", command=self._choose, width=4, height=1, font=font_big)
        self.choose_button.pack(side=BOTTOM, pady=5)

    def _choose(self):
        print('choose')
        print (self.list_box_additional.curselection())
        try:
            for choice in self.list_box_additional.curselection():
                self.additional_diagnoses_value.append(self.list[int(choice)])
        except IndexError:
            self.additional_diagnoses_value = None

        if self.text_box_due != None:
            self.text_box_due = self.text_box_due.get("0.1","end")

        self.text_box_notes = self.text_box_notes.get("0.1","end")

        self.modalPane.destroy()

    def return_value(self):
        # Wait until a WIDGET is destroyed.
        self.master.wait_window(self.modalPane)

        if self.check_box_value_F.get() == True and  self.check_box_value_M.get() == False:
            fetal_gender = 'F'
        elif self.check_box_value_M.get() == True and self.check_box_value_F.get() == False:
            fetal_gender = 'M'
        else:
            fetal_gender = ''

        print(self.additional_diagnoses_value, self.text_box_due, fetal_gender, self.text_box_notes)
        return self.additional_diagnoses_value, self.text_box_due, fetal_gender, self.text_box_notes
        # age_string, diagnosis_string, additional_list_of_strings_or_[], normal_boolean, notes_string


def main(title, choices_list, is_fetal): #=[random.randint(1, 100) for x in range(10)]
    main_window = Tk()
    additional_diagnoses, fetal_due_date, fetal_gender, notes = Patient_info_gui_opt(main_window, title, choices_list,
                                                                           is_fetal).return_value()
    main_window.destroy()
    return additional_diagnoses, fetal_due_date, fetal_gender, notes


if __name__ == '__main__':
    main()
