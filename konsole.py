import tkinter as tk
from tkinter import ttk
import shlex
import getpass
import socket
import sys
from datetime import datetime

APP_NAME = "BERKOV"

class ShellEmulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.title(f"{APP_NAME} - [{self.username}@{self.hostname}]")
        self.geometry("640x480")

        self.output = tk.Text(self, wrap="word", state="disabled", font=("JetBrains Mono", 11))
        self.output.pack(side="top", fill="both", expand=True, padx=8, pady=8)

        input_frame = ttk.Frame(self)
        input_frame.pack(side="bottom", fill="x", padx=8, pady=(0,8))

        self.prompt_var = tk.StringVar(value=self._make_prompt())
        self.prompt_label = ttk.Label(input_frame, textvariable=self.prompt_var, width=30)
        self.prompt_label.pack(side="left")

        self.entry = ttk.Entry(input_frame)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.focus_set()

        self.run_btn = ttk.Button(input_frame, text="↵", width=3, command=self.on_enter)
        self.run_btn.pack(side="left", padx=(6,0))

        self.entry.bind("<Return>", self.on_enter)

        self._writeln(f"{APP_NAME} Версия 1.0. Используйте 'exit' для выхода.\n")
        self._writeln("Поддерживаемые команды: ls, cd (как заглушки), exit.\n")
        self._writeln("Используйте кавычки, например: ls \"Мои документы\".\n")

    #отображение приглашения
    def _make_prompt(self) -> str:
        return f"{self.username}@{self.hostname}$ "

    def _write(self, text: str):
        self.output.configure(state="normal")
        self.output.insert("end", text)
        self.output.configure(state="disabled")
        self.output.see("end")

    def _writeln(self, text: str = ""):
        self._write(text + "\n")

    #обработка ввода
    def on_enter(self, event=None):
        raw = self.entry.get()
        self.entry.delete(0, "end")

        self._write(self._make_prompt() + raw + "\n")

        try:
            #парсер для кавычек
            argv = shlex.split(raw, posix=True)
        except ValueError as e:
            self._writeln(f"Ошибка парсинга аргументов: {e}")
            return

        if not argv:
            return
        cmd, *args = argv

        #обработка команд
        if cmd == "exit":
            self._writeln("Завершение работы…")
            self.after(150, self.destroy)
            return

        if cmd in ("ls", "cd"):
            self._writeln(self._format_stub_output(cmd, args))
            return
        
        self._writeln(f"{APP_NAME}: команда не найдена: {cmd}")

    #красивый вывод даты-времени
    def _format_stub_output(self, cmd: str, args: list[str]) -> str:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if args:
            joined = ", ".join([repr(a) for a in args])
        else:
            joined = "—"
        return f"[{ts}] {cmd} → args: {joined}"

def main():
    app = ShellEmulator()
    app.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
