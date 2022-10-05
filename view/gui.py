from __future__ import annotations

import tkinter.constants as tk
from tkinter import Tk, Frame, Button, Label, Entry, StringVar, Toplevel
from tkinter.messagebox import showerror, showinfo
from tkinter.simpledialog import askstring

import controller.guiController as Ctrl
from PIL import ImageTk,Image


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
        width = 32
        self.sv_name = StringVar()
        self.sv_login = StringVar()
        self.sv_password = StringVar()
        self.sv_search = StringVar()
        self.sv_user = StringVar(value="Not connected")

        # IMAGES
        previous_img = ImageTk.PhotoImage(Image.open("images/angle-left.png"))
        next_img = ImageTk.PhotoImage(Image.open("images/angle-right.png"))
        new_img = ImageTk.PhotoImage(Image.open("images/add-document.png"))
        add_img = ImageTk.PhotoImage(Image.open("images/check.png"))
        edit_img = ImageTk.PhotoImage(Image.open("images/pencil.png"))
        delete_img = ImageTk.PhotoImage(Image.open("images/trash.png"))
        login_img = ImageTk.PhotoImage(Image.open("images/login.png"))
        logout_img = ImageTk.PhotoImage(Image.open("images/logout.png"))
        new_user_img = ImageTk.PhotoImage(Image.open("images/user-add.png"))
        delete_user_img = ImageTk.PhotoImage(Image.open("images/remove-user.png"))
        quit_img = ImageTk.PhotoImage(Image.open("images/quit.png"))
        search_img = ImageTk.PhotoImage(Image.open("images/search.png").resize((16,16)))
        clipboard_img = ImageTk.PhotoImage(Image.open("images/clipboard.png"))

        # WIDGETS
        top_frame = Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, anchor=tk.N)
        top_frame.columnconfigure(6, weight=2)
        top_frame.rowconfigure(3, weight=1)

        self.btn_pi = Button(
            top_frame,
            text="Previous item",
            width=width,
            height=width,
            state=tk.DISABLED,
            command=self.goto_previous,
            image=previous_img,
        )
        self.btn_pi.grid(row=0, column=0, padx=padx)
        self.btn_pi.image = previous_img

        self.btn_newi = Button(
            top_frame,
            text="New Item",
            width=width,
            height=width,
            state=tk.DISABLED,
            command=self.do_new_item,
            image=new_img,
        )
        self.btn_newi.grid(row=0, column=1, padx=padx)
        self.btn_newi.image = new_img

        self.btn_ai = Button(
            top_frame,
            text="Add Item",
            width=width,
            height=width,
            state=tk.DISABLED,
            command=self.do_add_item,
            image=add_img,
        )
        self.btn_ai.grid(row=0, column=2, padx=padx, sticky=tk.W)
        self.btn_ai.image = add_img

        self.btn_ei = Button(
            top_frame,
            text="Edit Item",
            width=width,
            height=width,
            state=tk.DISABLED,
            command=self.do_edit_item,
            image=edit_img,
        )
        self.btn_ei.grid(row=0, column=3, padx=padx)
        self.btn_ei.image = edit_img

        self.btn_di = Button(
            top_frame,
            text="Delete Item",
            width=width,
            height=width,
            state=tk.DISABLED,
            command=self.do_delete_item,
            image=delete_img,
        )
        self.btn_di.grid(row=0, column=4, padx=padx)
        self.btn_di.image = delete_img

        self.btn_ni = Button(
            top_frame,
            text="Next item",
            width=width,
            height=width,
            state=tk.DISABLED,
            command=self.goto_next,
            image=next_img,
        )
        self.btn_ni.grid(row=0, column=5, padx=padx)
        self.btn_ni.image = next_img

        Label(top_frame).grid(row=0, column=6, sticky=tk.EW)  # Spacer

        Label(top_frame, textvariable=self.sv_user).grid(row=0, column=7, sticky=tk.E)

        login_btn = Button(top_frame, text="Login", width=width, height=width, command=self.log_in, image=login_img)
        login_btn.grid(row=0, column=8, sticky=tk.E)
        login_btn.image = login_img

        na_btn = Button(top_frame, text="New account", width=width, height=width, command=self.new_account,image=new_user_img)
        na_btn.grid(row=0, column=9, padx=padx)
        na_btn.image = new_user_img

        ra_btn = Button(top_frame, text="Remove account", width=width, height=width, command=self.remove_account,image=delete_user_img)
        ra_btn.grid(row=0, column=10, padx=padx)
        ra_btn.image = delete_user_img

        logout_btn = Button(top_frame, text="Logout", width=width,height=width, command=self.log_out,image=logout_img)
        logout_btn.grid(row=0, column=11, padx=padx)
        logout_btn.image = logout_img

        quit_btn = Button(top_frame, text="Quit", width=width,height=width, command=self.close,image=quit_img)
        quit_btn.grid(row=0, column=12, padx=padx)
        quit_btn.image = quit_img

        main_frame = Frame(self)
        main_frame.pack(expand=True, fill=tk.BOTH, after=top_frame)

        main_frame.columnconfigure(1, weight=2)

        Label(main_frame, text="Search For", anchor=tk.E).grid(
            row=0, column=0, sticky=tk.EW, pady=5
        )

        Entry(main_frame, textvariable=self.sv_search).grid(
            row=0, column=1, sticky=tk.EW
        )

        search_btn = Button(main_frame, text="Search", anchor=tk.E, width=width/2,height=width/2, command=self.do_search,image=search_img)
        search_btn.grid(row=0, column=2)
        search_btn.image = search_img

        Label(main_frame, text="Name", anchor=tk.E).grid(
            row=1, column=0, sticky=tk.EW, pady=5
        )
        Entry(main_frame, textvariable=self.sv_name).grid(row=1, column=1, sticky=tk.EW)

        Label(main_frame, text="Login", anchor=tk.E).grid(
            row=2, column=0, sticky=tk.EW, pady=5
        )
        Entry(main_frame, textvariable=self.sv_login).grid(
            row=2, column=1, sticky=tk.EW
        )

        Label(main_frame, text="Password", anchor=tk.E).grid(
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
            #width=width,
            height=width,
            image=clipboard_img,
            compound=tk.LEFT,
        )

        cpc = Button(
            bottom_frame,
            text="Copy password to clipboard",
            command=self.copy_password,
            #width=width,
            height=width,
            image=clipboard_img,
            compound=tk.LEFT
        )

        clc.image = clipboard_img
        cpc.image = clipboard_img

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
        if self.controller.reset():
            self.toggle_buttons(False)
            self.info("Logged out")
            self.show_username("")

    def new_account(self):
        account = LoginWindow(self, self.controller, True)
        account.mainloop()

    def remove_account(self):
        if self.controller.current_user is None:
            self.error("You are not connected")
            return
        if self.controller.remove_user(
            askstring("Confirmation", "Please enter your password to delete", show="*")
        ):
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
