from __future__ import annotations

import tkinter.constants as tk
from tkinter import Tk, Frame, Button, Label, Entry, StringVar, Toplevel
from tkinter.messagebox import showerror, showinfo
from tkinter.simpledialog import askstring

import controller.guiController as Ctrl


class LoginWindow(Toplevel):
    def __init__(self, master, control: Ctrl.GuiController, new_account: bool = False):
        super().__init__(master)
        self.resizable(False, False)
        self.new_account = new_account
        self.controller = control

        # VARIABLES
        self.sv_login = StringVar()
        self.sv_password = StringVar()
        self.sv_confirm = StringVar()

        # WIDGETS
        Label(self, text="Enter your login:").grid(row=0, column=0, pady=2)
        Entry(self, textvariable=self.sv_login).grid(row=0, column=1, pady=2)

        Label(self, text="Enter your password:").grid(row=1, column=0, pady=2)
        Entry(self, textvariable=self.sv_password, show="*").grid(
            row=1, column=1, pady=2
        )

        if self.new_account:
            Label(self, text="Confirm your password:").grid(row=2, column=0, pady=2)
            Entry(self, textvariable=self.sv_confirm, show="*").grid(
                row=2, column=1, pady=2
            )

        Button(
            self,
            text="Create Account" if self.new_account else "Log in",
            command=self.log_in,
            width=20,
        ).grid(row=3, column=0, columnspan=2, pady=2)
        Button(self, text="Cancel", command=self.cancel, width=20).grid(
            row=4, column=0, columnspan=2, pady=2
        )

    def log_in(self):
        if self.new_account:
            self.controller.register(
                self.sv_login.get(), self.sv_password.get(), self.sv_confirm.get()
            )
        else:
            self.controller.login(self.sv_login.get(), self.sv_password.get())

        self.destroy()

    def cancel(self):
        self.destroy()


class MainGui(Tk):
    """ """

    def __init__(self):
        super().__init__()
        self._controller = None
        self.title("PassMan - Password Manager")

        # VARIABLES
        padx = 1
        width = 12
        self.sv_name = StringVar()
        self.sv_login = StringVar()
        self.sv_password = StringVar()
        self.sv_search = StringVar()
        self.sv_user = StringVar(value="Not connected")

        # WIDGETS
        top_frame = Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, anchor=tk.N)
        top_frame.columnconfigure(6, weight=2)
        top_frame.rowconfigure(3, weight=1)

        self.btn_pi = Button(
            top_frame,
            text="Previous item",
            width=width,
            state=tk.DISABLED,
            command=self.goto_previous,
        )
        self.btn_pi.grid(row=0, column=0, padx=padx)

        self.btn_newi = Button(
            top_frame,
            text="New Item",
            width=width,
            state=tk.DISABLED,
            command=self.do_new_item,
        )
        self.btn_newi.grid(row=0, column=1, padx=padx)

        self.btn_ai = Button(
            top_frame,
            text="Add Item",
            width=width,
            state=tk.DISABLED,
            command=self.do_add_item,
        )
        self.btn_ai.grid(row=0, column=2, padx=padx, sticky=tk.W)

        self.btn_ei = Button(
            top_frame,
            text="Edit Item",
            width=width,
            state=tk.DISABLED,
            command=self.do_edit_item,
        )
        self.btn_ei.grid(row=0, column=3, padx=padx)

        self.btn_di = Button(
            top_frame,
            text="Delete Item",
            width=width,
            state=tk.DISABLED,
            command=self.do_delete_item,
        )
        self.btn_di.grid(row=0, column=4, padx=padx)

        self.btn_ni = Button(
            top_frame,
            text="Next item",
            width=width,
            state=tk.DISABLED,
            command=self.goto_next,
        )
        self.btn_ni.grid(row=0, column=5, padx=padx)

        Label(top_frame).grid(row=0, column=6, sticky=tk.EW)  # Spacer

        Label(top_frame, textvariable=self.sv_user).grid(row=0, column=7, sticky=tk.E)

        Button(top_frame, text="Login", width=width, command=self.log_in).grid(
            row=0, column=8, sticky=tk.E
        )

        Button(
            top_frame, text="New account", width=width, command=self.new_account
        ).grid(row=0, column=9, padx=padx)

        Button(
            top_frame, text="Remove account", width=width, command=self.remove_account
        ).grid(row=0, column=10, padx=padx)

        Button(top_frame, text="Logout", width=width, command=self.log_out).grid(
            row=0, column=11, padx=padx
        )

        Button(top_frame, text="Quit", width=width, command=self.close).grid(
            row=0, column=12, padx=padx
        )

        main_frame = Frame(self)
        main_frame.pack(expand=True, fill=tk.BOTH, after=top_frame)

        main_frame.columnconfigure(1, weight=2)

        Label(main_frame, text="Search For", anchor=tk.E, width=width).grid(
            row=0, column=0, sticky=tk.EW, pady=5
        )

        Entry(main_frame, textvariable=self.sv_search).grid(
            row=0, column=1, sticky=tk.EW
        )

        Button(main_frame, text="Search", anchor=tk.E, command=self.do_search).grid(
            row=0, column=2
        )

        Label(main_frame, text="Name", anchor=tk.E, width=width).grid(
            row=1, column=0, sticky=tk.EW, pady=5
        )
        Entry(main_frame, textvariable=self.sv_name).grid(row=1, column=1, sticky=tk.EW)

        Label(main_frame, text="Login", anchor=tk.E, width=width).grid(
            row=2, column=0, sticky=tk.EW, pady=5
        )
        Entry(main_frame, textvariable=self.sv_login).grid(
            row=2, column=1, sticky=tk.EW
        )

        Label(main_frame, text="Password", anchor=tk.E, width=width).grid(
            row=3, column=0, sticky=tk.EW, pady=5
        )
        Entry(main_frame, textvariable=self.sv_password).grid(
            row=3, column=1, sticky=tk.EW
        )

        bottom_frame = Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, anchor=tk.S)

        clc = Button(
            bottom_frame,
            text="Copy login to clipboard",
            command=self.copy_login,
            width=25,
        )
        cpc = Button(
            bottom_frame,
            text="Copy password to clipboard",
            command=self.copy_password,
            width=25,
        )

        clc.pack(side=tk.LEFT, padx=padx)
        cpc.pack(side=tk.LEFT, padx=padx)

    def do_new_item(self):
        self.sv_name.set("")
        self.sv_login.set("")
        self.sv_password.set("")

    def do_add_item(self):
        self.controller.add_item(
            self.sv_name.get(), self.sv_login.get(), self.sv_password.get()
        )

    def do_edit_item(self):
        self.controller.edit_item(
            self.sv_name.get(), self.sv_login.get(), self.sv_password.get()
        )

    def do_delete_item(self):
        self.controller.remove_item()

    def goto_previous(self):
        self.controller.previous()

    def goto_next(self):
        self.controller.next()

    def log_in(self):
        login = LoginWindow(self, self.controller)
        login.mainloop()

    def log_out(self):
        self.toggle_buttons(False)
        self.controller.reset()
        self.info("Logged out")
        self.show_username("")

    def new_account(self):
        account = LoginWindow(self, self.controller, True)
        account.mainloop()

    def remove_account(self):
        self.controller.remove_user(
            askstring("Confirmation", "Please enter your password to delete", show="*")
        )
        self.controller.reset()
        self.toggle_buttons(False)

    def copy_login(self):
        self.clipboard_clear()
        self.clipboard_append(self.sv_login.get())

    def copy_password(self):
        self.clipboard_clear()
        self.clipboard_append(self.sv_password.get())

    def close(self):
        self.destroy()

    def toggle_buttons(self, activate: bool):
        state = tk.NORMAL if activate else tk.DISABLED
        self.btn_ai.config(state=state)
        self.btn_di.config(state=state)
        self.btn_ei.config(state=state)
        self.btn_newi.config(state=state)
        self.btn_ni.config(state=state)
        self.btn_pi.config(state=state)

    def do_search(self):
        self.controller.search(self.sv_search.get())

    @staticmethod
    def error(message: str):
        showerror("Error", message)

    @staticmethod
    def info(message: str):
        showinfo("Info", message)

    @property
    def controller(self) -> Ctrl.GuiController:
        return self._controller

    @controller.setter
    def controller(self, value: Ctrl.GuiController) -> None:
        self._controller = value

    def show(self, name: str, login: str, password: str):
        self.sv_name.set(name)
        self.sv_login.set(login)
        self.sv_password.set(password)

    def show_username(self, user_name: str):
        if user_name == "":
            text = "Not connected"
        else:
            text = f"Connected as {user_name}"
        self.sv_user.set(text)
