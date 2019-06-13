from Tkinter import *
import add_new_exam
import compare_exam_to_normal



def close_window(): 
    win.destroy()
    win.quit()


def add():
    win.destroy()
    add_new_exam.main()


def compare():
    win.destroy()
    compare_exam_to_normal.main()




win = Tk()

win.title('Hello, choose an action!')
win.geometry('500x550') # Size 200, 200

btn_add_new_exam = Button(win, text='Add New Exam', command = lambda: add(), width = 20, font=('Helvetica', '20'))
btn_add_new_exam.pack(side=TOP, padx=2, pady=10)
btn_plot_series = Button(win, text='Plot Exam', command = lambda: compare(), width = 20, font=('Helvetica', '20'))
btn_plot_series.pack(side=TOP, padx=2, pady=10)


lbl_space = Label(text = '')
lbl_space.pack(side=TOP, padx=20, pady=45)


lbl_space2 = Label(text = '')
lbl_space2.pack(side=TOP, padx=20, pady=10)

btn_close = Button(win, text='Close Window', command = lambda: close_window(), width = 15, font=('Helvetica', '12'))
btn_close.pack(side=TOP, padx=2, pady=5)




mainloop()

