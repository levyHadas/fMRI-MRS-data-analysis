from Tkinter import *
import random
import tkFont
from Tkinter import SINGLE, MULTIPLE



class Series_gui(object):
    def __init__(self, master, title, message, choices_list, select_mode):

        my_font = tkFont.Font(family='Helvetica', size=16)

        self.master = master
        self.list = choices_list
        self.select_mode = select_mode

        self.choice_box_value=None

        self.modalPane = Toplevel(self.master)
        self.modalPane.transient(self.master)
        self.modalPane.grab_set()
        self.modalPane.title(title)
        Label(self.modalPane, text=message, font=my_font).pack(padx=5, pady=10)



        list_frame = Frame(self.modalPane)
        list_frame.pack(side=TOP, padx=20, pady=20, )


        self.list_box = Listbox(list_frame, selectmode=self.select_mode, width=80, height=20)

        for item in self.list:
            self.list_box.insert(END, item)
        self.list_box.pack(side=LEFT, fill=Y)



        button_frame = Frame(self.modalPane)
        button_frame.pack(side=BOTTOM)
        self.choose_button = Button(button_frame, text="OK", command=self._choose, width=4, height=1, font=my_font)
        self.choose_button.pack( pady=5)





    def _choose(self, event=None):
        if self.select_mode == SINGLE:
            try:
                for index in self.list_box.curselection():
                    self.choice_box_value = self.list[int(index)]
            except IndexError:
                self.choice_box_value = None
                print("you have to choose one")
        else:
            self.choice_box_value= []
            try:
                for index in self.list_box.curselection():
                    self.choice_box_value.append(self.list[int(index)])
            except IndexError:
                self.choice_box_value = None

        self.modalPane.destroy()

        
    def return_value(self):
        #Wait until a WIDGET is destroyed.
        self.master.wait_window(self.modalPane)
        return self.choice_box_value




def main (title, message, choices_list, select_mode):#(title="test", message="test", choices_list=[random.randint(1,12) for x in range(50)], select_mode= SINGLE):
    main_window = Tk()
    choice_box_answer  = Series_gui(main_window,title, message, choices_list, select_mode).return_value()
    main_window.destroy()
    return choice_box_answer #return type: string

if __name__ == '__main__':
    main()
