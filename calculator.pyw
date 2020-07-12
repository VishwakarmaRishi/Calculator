# Written by Rishi 
# Completed on 7 July, 2020

import math
from threading import Thread
from time import sleep
from tkinter.__init__ import Tk, Button, Label, Frame, StringVar, BooleanVar, Menubutton, Menu, Toplevel
from tkinter.constants import *

from playsound import playsound #pip install playsound
#uncomment next 2 lines if you don't have playsound
#import os
#os.system('pip install playsound')

fact = math.factorial
rad = math.radians


def log(number):
    return round(math.log10(number), 3)


def ln(number):
    return round(math.log(number), 3)


def sin(angle, unit=rad):
    return round(math.sin(unit(angle)), 3)


def cos(angle, unit=rad):
    return round(math.cos(unit(angle)), 3)


def tan(angle, unit=rad):
    return round(math.tan(unit(angle)), 3)


def csc(angle, unit=rad):
    return round(1 / sin(angle), 3)


def sec(angle, unit=rad):
    return round(1 / cos(angle), 3)


def cot(angle, unit=rad):
    return round(1 / tan(angle), 3)


def HCF_of_2(x, y):
    while y:
        x, y = y, x % y
    return x


def HCF(*numbers):
    if len(numbers) == 2:
        return HCF_of_2(*numbers)
    else:
        numbers = list(numbers)
        for i in range(len(numbers) - 1):
            numbers.append(HCF_of_2(numbers.pop(), numbers.pop()))
        return numbers[0]


def LCM_of_2(x, y):
    return x * y // HCF(x, y)


def LCM(*numbers):
    if len(numbers) == 2:
        return LCM_of_2(*numbers)
    else:
        numbers = list(numbers)
        for i in range(len(numbers) - 1):
            numbers.append(LCM_of_2(numbers.pop(), numbers.pop()))
        return numbers[0]


class Window(Tk):
    def __init__(self):
        self.modes = ['Basic ', 'Advanced ']
        self.columns = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.buttons = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        self.labels = (
            ('DEL', '7', '4', '1', ' ± '),
            ('CLR', '8', '5', '2', ' 0 '),
            (' ÷ ', '9', '6', '3', ' . '),
            (' × ', '-', '+', ' ', ' = '),
            (' % ', '^', '×', '-', ' + '),
            ('sin', 'csc', '(', 'x²', '√x'),
            ('cos', 'sec', ')', 'x³', '∛x'),
            ('tan', 'cot', 'log', 'HCF', ','),
            ('π', '!', 'ln', 'LCM', ' = ')
        )

    def column_creator(self, x, y):
        for i in range(x, y):
            self.columns[i] = Frame(self.window)
            self.columns[i].pack(fill=BOTH, expand=True, side=LEFT)

    def button_creator(self, x, y):
        for i in range(x, y):
            for j in range(5):
                self.buttons[i][j] = Button(self.columns[i], text=self.labels[i][j], font=('Courier New', 18, 'bold'),
                                            activebackground='#111111', activeforeground='white', bg='black',
                                            fg='white',
                                            borderwidth=0, takefocus=False)
                self.buttons[i][j].pack(side=TOP, fill=BOTH, expand=True)

    def create_layout(self):
        self.window = Tk()

        self.window.geometry('330x510+90+90')
        self.window.resizable(1, 1)

        self.window.title('Calculator')
        self.window.iconbitmap('icon.ico')

        self.current_mode = StringVar()
        self.current_mode.set('Basic ')
        self.expression = StringVar()
        self.always_on_top = BooleanVar()
        self.click_sound_enabled = BooleanVar()

        self.options_bar = Frame(self.window, height=30, bg='black')
        self.options_bar.pack(fill=X)

        self.change_mode_button = Label(self.options_bar, text=' ⇄ ', bg='black', fg='white', font=('Helvetica', 27),
                                        borderwidth=0,
                                        activebackground='#111111',
                                        padx=0, pady=0)
        self.change_mode_button.pack(padx=0, pady=0, side=LEFT)
        self.change_mode_button.bind('<Button-1>', self.change_mode)
        self.change_mode_button.bind('<Enter>', lambda event: self.mode_highlight(1))
        self.change_mode_button.bind('<Leave>', lambda event: self.mode_highlight(0))

        self.current_mode_label = Label(self.options_bar, textvariable=self.current_mode, bg='black', fg='white',
                                        font=('Trebuchet MS', 22, 'bold'),
                                        padx=0, pady=0)
        self.current_mode_label.pack(side=LEFT)
        self.current_mode_label.bind('<Button-1>', self.change_mode)
        self.current_mode_label.bind('<Enter>', lambda event: self.mode_highlight(1))
        self.current_mode_label.bind('<Leave>', lambda event: self.mode_highlight(0))

        self.menu = Menubutton(self.options_bar, text=' ≡ ', bg='black', activebackground='#334033',
                               activeforeground='white',
                               fg='white',
                               font=('Helvetica', 24), borderwidth=0)
        self.menu.bind('<Button-1>', lambda event: self.play_click_sound())
        self.menu.pack(side=RIGHT)
        self.menu.menu = Menu(self.menu, bg='#446644', fg='white', tearoff=0)
        self.menu['menu'] = self.menu.menu

        self.menu.menu.add_checkbutton(label='Always on Top', font=('Consolas', 10, 'bold'),
                                       variable=self.always_on_top,
                                       command=self.always_on_top_control)
        self.menu.menu.add_checkbutton(label='Click Sound', font=('Consolas', 10, 'bold'),
                                       variable=self.click_sound_enabled)
        self.menu.menu.add_separator()
        self.menu.menu.add_command(label='Exit', font=('Consolas', 10, 'bold'), command=self.window.destroy)

        self.expression_bar = Frame(self.window, bg='yellow')
        self.expression_bar.pack(fill=X)

        self.full_expression = Label(self.expression_bar, textvariable=self.expression, font=('@Gungsuh', 20, 'bold'),
                                     bg='yellow',
                                     height=1)
        self.full_expression.pack(side=TOP, anchor=E, ipady=10)

        self.column_creator(0, 4)
        self.button_creator(0, 4)

    def handle_events_and_run(self):
        self.change_mode()
        self.button_click_control()
        self.hover_control()
        self.key_press_handler()
        self.window_updater()

        self.window.mainloop()

    def window_updater(self):
        def update_window():
            while True:
                self.window.update()
                sleep(.1)

        self.updater = Thread(target=update_window)
        self.updater.daemon = True
        self.updater.start()

    def play_click_sound(self):
        if self.click_sound_enabled.get():
            Thread(target=lambda: playsound('mouse_click.aif')).start()

    def always_on_top_control(self):
        if self.always_on_top.get():
            self.window.wm_attributes('-topmost', True)
        else:
            self.window.wm_attributes('-topmost', False)

    def throw_calculation_error(self):
        self.error_window = Toplevel(bg='#333633', bd=10)
        self.error_window.overrideredirect(True)
        self.error_window.wm_attributes('-topmost', True)
        self.error_window.grab_set()

        window_geometry = self.window.wm_geometry()
        x_padding = str(int(window_geometry.split("+")[1]) + int(window_geometry.split("x")[0]) // 3)
        y_padding = str(int(window_geometry.split("+")[2]) + 180)
        self.error_window.geometry(f'200x150+{x_padding}+{y_padding}')

        Label(self.error_window, text='Error!', padx=20, pady=20, font=('Consolas', 18, 'bold'), bg='black',
              fg='white').pack(side=TOP, fill=BOTH, expand=True)
        ok_button=Button(self.error_window, text='  OK  ', font=('Helvetica', 10, 'bold'), bg='#dddddd', fg='black', bd=2,
               command=self.error_window.destroy)
        ok_button.pack(side=TOP, anchor=E, padx=10, pady=10)
        ok_button.bind('<Button-1>',lambda event:self.play_click_sound())

    def expression_updater(self, value):
        self.expression.set(self.expression.get() + str(value))
        self.play_click_sound()

    def clear_all(self, event):
        self.expression.set('')
        self.play_click_sound()

    def backspace(self, event):
        current_expression = self.expression.get()
        self.expression.set(current_expression[:len(current_expression) - 1])
        self.play_click_sound()

    def negative(self, event):
        self.expression.set(f'-({self.expression.get()})')
        self.play_click_sound()

    def square(self, event):
        self.expression.set(f'(({self.expression.get()})**2)')
        self.play_click_sound()

    def cube(self, event):
        self.expression.set(f'(({self.expression.get()})**3)')
        self.play_click_sound()

    def square_root(self, event):
        self.expression.set(f'(({self.expression.get()})**(1/2))')
        self.play_click_sound()

    def cube_root(self, event):
        self.expression.set(f'(({self.expression.get()})**(1/3))')
        self.play_click_sound()

    def factorial(self, event):
        self.expression.set(f'fact({self.expression.get()})')
        self.play_click_sound()

    def evaluate(self, play_sound=False, mode='normal'):
        current_expression = self.expression.get()
        try:
            self.expression.set(str(round(eval(current_expression), 3)))
        except:
            if not current_expression:
                pass
            else:
                self.throw_calculation_error()
        if play_sound: self.play_click_sound()

    def basic_evaluate(self, click=False):
        if click:
            self.buttons[3][3].configure(bg='#111111')
            self.buttons[3][4].configure(bg='#111111')
            try:
                self.expression.set(str(round(eval(self.expression.get()), 3)))
            except:
                if not self.expression.get():
                    pass
                else:
                    self.throw_calculation_error()
        else:
            self.buttons[3][3].configure(bg='black')
            self.buttons[3][4].configure(bg='black')
        self.play_click_sound()

    def change_mode(self, event=None):
        self.play_click_sound()
        self.current_mode.set(self.modes[0])

        if self.modes[0] == 'Basic ':
            self.window.geometry('330x510')
            self.window.minsize(290, 420)
            try:
                for i in range(3, 9):
                    self.columns[i].destroy()
            except AttributeError:
                pass

            self.column_creator(3, 4)
            self.button_creator(3, 4)
            self.button_click_control()
            self.hover_control()

        else:
            self.window.geometry('660x510')
            self.window.minsize(615, 420)
            self.columns[3].destroy()
            self.column_creator(4, 9)
            self.button_creator(4, 9)
            self.button_click_control('advanced')
            self.hover_control('advanced')
        self.modes.reverse()

    def mode_highlight(self, hover):
        if hover:
            self.change_mode_button.configure(bg='#334033')
            self.current_mode_label.configure(bg='#334033')
        else:
            self.change_mode_button.configure(bg='black')
            self.current_mode_label.configure(bg='black')

    def button_click_control(self, mode='basic'):
        if mode == 'advanced':
            self.buttons[4][0].bind('<Button-1>', lambda event: self.expression_updater('%'))
            self.buttons[4][1].bind('<Button-1>', lambda event: self.expression_updater('**'))
            self.buttons[4][2].bind('<Button-1>', lambda event: self.expression_updater('*'))
            self.buttons[4][3].bind('<Button-1>', lambda event: self.expression_updater('-'))
            self.buttons[4][4].bind('<Button-1>', lambda event: self.expression_updater('+'))
            self.buttons[5][0].bind('<Button-1>', lambda event: self.expression_updater('+sin('))
            self.buttons[5][1].bind('<Button-1>', lambda event: self.expression_updater('+csc('))
            self.buttons[5][2].bind('<Button-1>', lambda event: self.expression_updater('('))
            self.buttons[5][3].bind('<Button-1>', self.square)
            self.buttons[5][4].bind('<Button-1>', self.square_root)
            self.buttons[6][0].bind('<Button-1>', lambda event: self.expression_updater('+cos('))
            self.buttons[6][1].bind('<Button-1>', lambda event: self.expression_updater('+sec('))
            self.buttons[6][2].bind('<Button-1>', lambda event: self.expression_updater(')'))
            self.buttons[6][3].bind('<Button-1>', self.cube)
            self.buttons[6][4].bind('<Button-1>', self.cube_root)
            self.buttons[7][0].bind('<Button-1>', lambda event: self.expression_updater('+tan('))
            self.buttons[7][1].bind('<Button-1>', lambda event: self.expression_updater('+cot('))
            self.buttons[7][2].bind('<Button-1>', lambda event: self.expression_updater('+log('))
            self.buttons[7][3].bind('<Button-1>', lambda event: self.expression_updater('+HCF('))
            self.buttons[7][4].bind('<Button-1>', lambda event: self.expression_updater(','))
            self.buttons[8][0].bind('<Button-1>', lambda event: self.expression_updater('+3.142'))
            self.buttons[8][1].bind('<Button-1>', self.factorial)
            self.buttons[8][2].bind('<Button-1>', lambda event: self.expression_updater('+ln('))
            self.buttons[8][3].bind('<Button-1>', lambda event: self.expression_updater('+LCM('))
            self.buttons[8][4].bind('<Button-1>', lambda event: self.evaluate(True))

        else:
            self.buttons[0][0].bind('<Button-1>', self.backspace)
            self.buttons[0][1].bind('<Button-1>', lambda event: self.expression_updater(7))
            self.buttons[0][2].bind('<Button-1>', lambda event: self.expression_updater(4))
            self.buttons[0][3].bind('<Button-1>', lambda event: self.expression_updater(1))
            self.buttons[0][4].bind('<Button-1>', self.negative)
            self.buttons[1][0].bind('<Button-1>', self.clear_all)
            self.buttons[1][1].bind('<Button-1>', lambda event: self.expression_updater(8))
            self.buttons[1][2].bind('<Button-1>', lambda event: self.expression_updater(5))
            self.buttons[1][3].bind('<Button-1>', lambda event: self.expression_updater(2))
            self.buttons[1][4].bind('<Button-1>', lambda event: self.expression_updater(0))
            self.buttons[2][0].bind('<Button-1>', lambda event: self.expression_updater('/'))
            self.buttons[2][1].bind('<Button-1>', lambda event: self.expression_updater(9))
            self.buttons[2][2].bind('<Button-1>', lambda event: self.expression_updater(6))
            self.buttons[2][3].bind('<Button-1>', lambda event: self.expression_updater(3))
            self.buttons[2][4].bind('<Button-1>', lambda event: self.expression_updater('.'))
            self.buttons[3][0].bind('<Button-1>', lambda event: self.expression_updater('*'))
            self.buttons[3][1].bind('<Button-1>', lambda event: self.expression_updater('-'))
            self.buttons[3][2].bind('<Button-1>', lambda event: self.expression_updater('+'))

            self.buttons[3][3].bind('<Button-1>', lambda event: self.basic_evaluate(True))
            self.buttons[3][4].bind('<Button-1>', lambda event: self.basic_evaluate(True))
            self.buttons[3][3].bind('<ButtonRelease-1>', lambda event: self.basic_evaluate())
            self.buttons[3][4].bind('<ButtonRelease-1>', lambda event: self.basic_evaluate())

    def hover_control(self, mode='basic'):
        def equal_hover(hover=False):
            if hover:
                self.buttons[3][3].configure(bg='#222222')
                self.buttons[3][4].configure(bg='#222222')
            else:
                self.buttons[3][3].configure(bg='black')
                self.buttons[3][4].configure(bg='black')

        if mode == 'advanced':
            self.buttons[4][0].bind('<Enter>', lambda event: self.buttons[4][0].configure(bg='#222222'))
            self.buttons[4][1].bind('<Enter>', lambda event: self.buttons[4][1].configure(bg='#222222'))
            self.buttons[4][2].bind('<Enter>', lambda event: self.buttons[4][2].configure(bg='#222222'))
            self.buttons[4][3].bind('<Enter>', lambda event: self.buttons[4][3].configure(bg='#222222'))
            self.buttons[4][4].bind('<Enter>', lambda event: self.buttons[4][4].configure(bg='#222222'))
            self.buttons[5][0].bind('<Enter>', lambda event: self.buttons[5][0].configure(bg='#222222'))
            self.buttons[5][1].bind('<Enter>', lambda event: self.buttons[5][1].configure(bg='#222222'))
            self.buttons[5][2].bind('<Enter>', lambda event: self.buttons[5][2].configure(bg='#222222'))
            self.buttons[5][3].bind('<Enter>', lambda event: self.buttons[5][3].configure(bg='#222222'))
            self.buttons[5][4].bind('<Enter>', lambda event: self.buttons[5][4].configure(bg='#222222'))
            self.buttons[6][0].bind('<Enter>', lambda event: self.buttons[6][0].configure(bg='#222222'))
            self.buttons[6][1].bind('<Enter>', lambda event: self.buttons[6][1].configure(bg='#222222'))
            self.buttons[6][2].bind('<Enter>', lambda event: self.buttons[6][2].configure(bg='#222222'))
            self.buttons[6][3].bind('<Enter>', lambda event: self.buttons[6][3].configure(bg='#222222'))
            self.buttons[6][4].bind('<Enter>', lambda event: self.buttons[6][4].configure(bg='#222222'))
            self.buttons[7][0].bind('<Enter>', lambda event: self.buttons[7][0].configure(bg='#222222'))
            self.buttons[7][1].bind('<Enter>', lambda event: self.buttons[7][1].configure(bg='#222222'))
            self.buttons[7][2].bind('<Enter>', lambda event: self.buttons[7][2].configure(bg='#222222'))
            self.buttons[7][3].bind('<Enter>', lambda event: self.buttons[7][3].configure(bg='#222222'))
            self.buttons[7][4].bind('<Enter>', lambda event: self.buttons[7][4].configure(bg='#222222'))
            self.buttons[8][0].bind('<Enter>', lambda event: self.buttons[8][0].configure(bg='#222222'))
            self.buttons[8][1].bind('<Enter>', lambda event: self.buttons[8][1].configure(bg='#222222'))
            self.buttons[8][2].bind('<Enter>', lambda event: self.buttons[8][2].configure(bg='#222222'))
            self.buttons[8][3].bind('<Enter>', lambda event: self.buttons[8][3].configure(bg='#222222'))
            self.buttons[8][4].bind('<Enter>', lambda event: self.buttons[8][4].configure(bg='#222222'))

            self.buttons[4][0].bind('<Leave>', lambda event: self.buttons[4][0].configure(bg='black'))
            self.buttons[4][1].bind('<Leave>', lambda event: self.buttons[4][1].configure(bg='black'))
            self.buttons[4][2].bind('<Leave>', lambda event: self.buttons[4][2].configure(bg='black'))
            self.buttons[4][3].bind('<Leave>', lambda event: self.buttons[4][3].configure(bg='black'))
            self.buttons[4][4].bind('<Leave>', lambda event: self.buttons[4][4].configure(bg='black'))
            self.buttons[5][0].bind('<Leave>', lambda event: self.buttons[5][0].configure(bg='black'))
            self.buttons[5][1].bind('<Leave>', lambda event: self.buttons[5][1].configure(bg='black'))
            self.buttons[5][2].bind('<Leave>', lambda event: self.buttons[5][2].configure(bg='black'))
            self.buttons[5][3].bind('<Leave>', lambda event: self.buttons[5][3].configure(bg='black'))
            self.buttons[5][4].bind('<Leave>', lambda event: self.buttons[5][4].configure(bg='black'))
            self.buttons[6][0].bind('<Leave>', lambda event: self.buttons[6][0].configure(bg='black'))
            self.buttons[6][1].bind('<Leave>', lambda event: self.buttons[6][1].configure(bg='black'))
            self.buttons[6][2].bind('<Leave>', lambda event: self.buttons[6][2].configure(bg='black'))
            self.buttons[6][3].bind('<Leave>', lambda event: self.buttons[6][3].configure(bg='black'))
            self.buttons[6][4].bind('<Leave>', lambda event: self.buttons[6][4].configure(bg='black'))
            self.buttons[7][0].bind('<Leave>', lambda event: self.buttons[7][0].configure(bg='black'))
            self.buttons[7][1].bind('<Leave>', lambda event: self.buttons[7][1].configure(bg='black'))
            self.buttons[7][2].bind('<Leave>', lambda event: self.buttons[7][2].configure(bg='black'))
            self.buttons[7][3].bind('<Leave>', lambda event: self.buttons[7][3].configure(bg='black'))
            self.buttons[7][4].bind('<Leave>', lambda event: self.buttons[7][4].configure(bg='black'))
            self.buttons[8][0].bind('<Leave>', lambda event: self.buttons[8][0].configure(bg='black'))
            self.buttons[8][1].bind('<Leave>', lambda event: self.buttons[8][1].configure(bg='black'))
            self.buttons[8][2].bind('<Leave>', lambda event: self.buttons[8][2].configure(bg='black'))
            self.buttons[8][3].bind('<Leave>', lambda event: self.buttons[8][3].configure(bg='black'))
            self.buttons[8][4].bind('<Leave>', lambda event: self.buttons[8][4].configure(bg='black'))
        else:
            self.buttons[0][0].bind('<Enter>', lambda event: self.buttons[0][0].configure(bg='#222222'))
            self.buttons[0][1].bind('<Enter>', lambda event: self.buttons[0][1].configure(bg='#222222'))
            self.buttons[0][2].bind('<Enter>', lambda event: self.buttons[0][2].configure(bg='#222222'))
            self.buttons[0][3].bind('<Enter>', lambda event: self.buttons[0][3].configure(bg='#222222'))
            self.buttons[0][4].bind('<Enter>', lambda event: self.buttons[0][4].configure(bg='#222222'))
            self.buttons[1][0].bind('<Enter>', lambda event: self.buttons[1][0].configure(bg='#222222'))
            self.buttons[1][1].bind('<Enter>', lambda event: self.buttons[1][1].configure(bg='#222222'))
            self.buttons[1][2].bind('<Enter>', lambda event: self.buttons[1][2].configure(bg='#222222'))
            self.buttons[1][3].bind('<Enter>', lambda event: self.buttons[1][3].configure(bg='#222222'))
            self.buttons[1][4].bind('<Enter>', lambda event: self.buttons[1][4].configure(bg='#222222'))
            self.buttons[2][0].bind('<Enter>', lambda event: self.buttons[2][0].configure(bg='#222222'))
            self.buttons[2][1].bind('<Enter>', lambda event: self.buttons[2][1].configure(bg='#222222'))
            self.buttons[2][2].bind('<Enter>', lambda event: self.buttons[2][2].configure(bg='#222222'))
            self.buttons[2][3].bind('<Enter>', lambda event: self.buttons[2][3].configure(bg='#222222'))
            self.buttons[2][4].bind('<Enter>', lambda event: self.buttons[2][4].configure(bg='#222222'))
            self.buttons[3][0].bind('<Enter>', lambda event: self.buttons[3][0].configure(bg='#222222'))
            self.buttons[3][1].bind('<Enter>', lambda event: self.buttons[3][1].configure(bg='#222222'))
            self.buttons[3][2].bind('<Enter>', lambda event: self.buttons[3][2].configure(bg='#222222'))
            self.buttons[3][3].bind('<Enter>', lambda event: equal_hover(True))
            self.buttons[3][4].bind('<Enter>', lambda event: equal_hover(True))
            self.buttons[0][0].bind('<Leave>', lambda event: self.buttons[0][0].configure(bg='black'))
            self.buttons[0][1].bind('<Leave>', lambda event: self.buttons[0][1].configure(bg='black'))
            self.buttons[0][2].bind('<Leave>', lambda event: self.buttons[0][2].configure(bg='black'))
            self.buttons[0][3].bind('<Leave>', lambda event: self.buttons[0][3].configure(bg='black'))
            self.buttons[0][4].bind('<Leave>', lambda event: self.buttons[0][4].configure(bg='black'))
            self.buttons[1][0].bind('<Leave>', lambda event: self.buttons[1][0].configure(bg='black'))
            self.buttons[1][1].bind('<Leave>', lambda event: self.buttons[1][1].configure(bg='black'))
            self.buttons[1][2].bind('<Leave>', lambda event: self.buttons[1][2].configure(bg='black'))
            self.buttons[1][3].bind('<Leave>', lambda event: self.buttons[1][3].configure(bg='black'))
            self.buttons[1][4].bind('<Leave>', lambda event: self.buttons[1][4].configure(bg='black'))
            self.buttons[2][0].bind('<Leave>', lambda event: self.buttons[2][0].configure(bg='black'))
            self.buttons[2][1].bind('<Leave>', lambda event: self.buttons[2][1].configure(bg='black'))
            self.buttons[2][2].bind('<Leave>', lambda event: self.buttons[2][2].configure(bg='black'))
            self.buttons[2][3].bind('<Leave>', lambda event: self.buttons[2][3].configure(bg='black'))
            self.buttons[2][4].bind('<Leave>', lambda event: self.buttons[2][4].configure(bg='black'))
            self.buttons[3][0].bind('<Leave>', lambda event: self.buttons[3][0].configure(bg='black'))
            self.buttons[3][1].bind('<Leave>', lambda event: self.buttons[3][1].configure(bg='black'))
            self.buttons[3][2].bind('<Leave>', lambda event: self.buttons[3][2].configure(bg='black'))
            self.buttons[3][3].bind('<Leave>', lambda event: equal_hover())
            self.buttons[3][4].bind('<Leave>', lambda event: equal_hover())

    def key_press_handler(self):
        self.window.bind('<Delete>', lambda event: self.expression.set(''))
        self.window.bind('pi', lambda event: self.expression_updater('+3.142'))
        self.window.bind('0', lambda event: self.expression_updater(0))
        self.window.bind('1', lambda event: self.expression_updater(1))
        self.window.bind('2', lambda event: self.expression_updater(2))
        self.window.bind('3', lambda event: self.expression_updater(3))
        self.window.bind('4', lambda event: self.expression_updater(4))
        self.window.bind('5', lambda event: self.expression_updater(5))
        self.window.bind('6', lambda event: self.expression_updater(6))
        self.window.bind('7', lambda event: self.expression_updater(7))
        self.window.bind('8', lambda event: self.expression_updater(8))
        self.window.bind('9', lambda event: self.expression_updater(9))
        self.window.bind('.', lambda event: self.expression_updater('.'))
        self.window.bind('+', lambda event: self.expression_updater('+'))
        self.window.bind('-', lambda event: self.expression_updater('-'))
        self.window.bind('*', lambda event: self.expression_updater('*'))
        self.window.bind('/', lambda event: self.expression_updater('/'))
        self.window.bind('%', lambda event: self.expression_updater('%'))
        self.window.bind('sin', lambda event: self.expression_updater('+sin('))
        self.window.bind('cos', lambda event: self.expression_updater('+cos('))
        self.window.bind('tan', lambda event: self.expression_updater('+tan('))
        self.window.bind('csc', lambda event: self.expression_updater('+csc('))
        self.window.bind('sec', lambda event: self.expression_updater('+sec('))
        self.window.bind('cot', lambda event: self.expression_updater('+cot('))
        self.window.bind('log', lambda event: self.expression_updater('+log('))
        self.window.bind('ln', lambda event: self.expression_updater('+ln('))
        self.window.bind('hcf', lambda event: self.expression_updater('+HCF('))
        self.window.bind('lcm', lambda event: self.expression_updater('+LCM('))
        self.window.bind(',', lambda event: self.expression_updater(','))
        self.window.bind('!', lambda event: self.expression.set(f'fact({self.expression.get()})'))
        self.window.bind('(', lambda event: self.expression_updater(')'))
        self.window.bind(')', lambda event: self.expression_updater(')'))
        self.window.bind('<BackSpace>',
                         lambda event: self.expression.set(self.expression.get()[:len(self.expression.get()) - 1]))
        self.window.bind('<Return>', lambda event: self.evaluate())
        self.window.bind('=', lambda event: self.evaluate())
        self.window.bind('<space>', self.change_mode)
        self.window.bind('<Tab>', self.change_mode)
        self.window.bind('<Control-x>', lambda event: self.window.destroy())
        self.window.bind('<Escape>', lambda event: self.window.destroy())


calculator = Window()
calculator.create_layout()
calculator.handle_events_and_run()
