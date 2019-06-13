from Tkinter import *
import random
from Tkinter import SINGLE, MULTIPLE, END
import tkFont


class Patient_info_gui_req(object):
    def __init__(self, master, title, choices_list, is_fetal=False):

        font_small = tkFont.Font(family='Helvetica', size=11)
        font_big = tkFont.Font(family='Helvetica', size=14)
        font_header = tkFont.Font(family='Helvetica', size=15, underline=1)

        self.master = master

        self.check_box_value = BooleanVar()

        self.main_diagnosis_value = None

        self.text_box_age = None

        self.list = choices_list

        self.modalPane = Toplevel(self.master)
        self.modalPane.transient(self.master)
        self.modalPane.grab_set()
        self.modalPane.title(title)
        Label(self.modalPane, text="Required Patient Info", font=font_header).pack(padx=5, pady=10)

        if is_fetal:
            text_frame = Frame(self.modalPane)
            text_frame.pack(side=TOP, padx=10, pady=10)
            Label(text_frame, text="Enter the Fetal age in weeks", font=font_big).pack()
            self.text_box_age = Text(text_frame, width=40, height=2)
            self.text_box_age.pack(side=TOP)

        list_frame = Frame(self.modalPane)
        list_frame.pack(side=TOP, padx=10, pady=10)
        Label(list_frame, text="SELECT ONE MAIN DIAGNOSIS", font=font_big).pack()
        self.list_box_main = Listbox(list_frame, selectmode=SINGLE, width=40, height=12, yscrollcommand=True)
        for item in self.list:
            self.list_box_main.insert(END, item)
        self.list_box_main.pack(side=LEFT, fill=Y)

        check_box_frame = Frame(self.modalPane)
        check_box_frame.pack(side=TOP, padx=10, pady=10)
        self.check_box_value.set(True)
        self.check_box = Checkbutton(check_box_frame, text='Should be considered for \"Normal\"',
                                     variable=self.check_box_value, font=font_small)
        self.check_box.pack(side=TOP, pady=5)

        button_frame = Frame(self.modalPane)
        button_frame.pack(side=BOTTOM, padx=10, pady=10)
        self.choose_button = Button(button_frame, text="OK", command=self._choose, width=4, height=1, font=font_big)
        self.choose_button.pack(side=BOTTOM, pady=5)

    def _choose(self, event=None):

        try:
            for choice in self.list_box_main.curselection():
                self.main_diagnosis_value = self.list[int(choice)]
        except IndexError:
            self.main_diagnosis_value = None
            print("you have to choose one main Diagnosis")

        if self.text_box_age != None:
            self.text_box_age = self.text_box_age.get("0.1", "end")

        self.modalPane.destroy()

    def return_value(self):
        # Wait until a WIDGET is destroyed.
        self.master.wait_window(self.modalPane)

        print(self.text_box_age, self.main_diagnosis_value, self.check_box_value.get())
        return self.text_box_age, self.main_diagnosis_value, self.check_box_value.get()
        # age_string, diagnosis_string, additional_list_of_strings_or_[], normal_boolean, notes_string


def main(title, choices_list, is_fetal): #=[random.randint(1, 100) for x in range(10)]
    main_window = Tk()
    fetal_age, main_diagnosis, is_normal = Patient_info_gui_req(main_window, title, choices_list,
                                                                           is_fetal).return_value()

    main_window.destroy()
    return fetal_age, main_diagnosis, is_normal


if __name__ == '__main__':
    main()
