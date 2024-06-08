import requests, random
import tkinter as tk

WEB = "https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json"
FILE = "words_5.txt"
LETTERS = 5


class GUI:
    def __init__(self, words):
        self.window = tk.Tk()
        self.words = words
        self.inex = {"Include": tk.StringVar(), "Exclude": tk.StringVar()}

        self.window.geometry('800x500')
        self.window.title("Wordle Helper")

        self.letters = tk.Frame(self.window)
        self.letters_entries = [0] * LETTERS
        for i in range(LETTERS):
            self.letters_entries[i] = tk.Entry(self.letters, borderwidth=5, width=3)
            self.letters_entries[i].grid(row=0, column=i)


        self.btn_return = tk.Button(self.window, text="Enter")
        
        self.generate = tk.Frame(self.window)
        self.generate_comps = {"Include": [0, 0], "Exclude": [0, 0]}
        for i, key in enumerate(self.generate_comps):
            for j in range(2):
                self.generate_comps[key][j] = tk.Label(self.generate, text=key) if j == 0 else tk.Entry(self.generate, textvariable=self.inex[key])
                self.generate_comps[key][j].grid(row=i, column=j)
        
        self.btn_search = tk.Button(self.window, text="Search", command=self.search)
        self.letters.pack()
        self.btn_return.pack()
        self.generate.pack()
        self.btn_search.pack()

        self.message = tk.Text(self.window, width=500, state=tk.DISABLED)

        self.scrollbar = tk.Scrollbar(self.window, command=self.message.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message.pack()

        self.message.config(yscrollcommand=self.scrollbar.set)

        self.window.mainloop()

    def search(self):
        def check_exclude(list, word):
            for char in list:
                if char in word:
                    return False
            return True

        def check_include(list, word):
            for char in list:
                if char not in word:
                    return False
            return True
        
        self.message.config(state=tk.NORMAL)
        self.message.delete(1.0, tk.END)
        
        
        include = set(self.inex["Include"].get())
        exclude = set(self.inex["Exclude"].get())
        
        string = ''
        for word in self.words:
            if check_exclude(exclude, word) and check_include(include, word):
                string += word + '\n'
        self.message.insert(tk.END, string)
        self.message.config(state=tk.DISABLED)


def write_file():
    words = {}
    if web := requests.get(WEB).json():
        words = web
    with open(FILE, 'w') as file:
        for word in words:
            if len(word) == 5:
                file.write(word + '\n')


def read_file():
    words = {}
    with open(FILE) as file:
        for row in file:
            words[row[:-1]] = 1
    return words


def main():
    words = {}

    while True:
        try:
            words = read_file()
        except FileNotFoundError:
            write_file()
        else:
            break
    GUI(words)


if __name__ == "__main__":
    main()