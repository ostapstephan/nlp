from tkinter import Tk, scrolledtext, Menu, filedialog, END, messagebox
import os

class Text_Editor:

    def __init__(self):
        self.root = Tk(className = "Text Editor")
        self.textPad = scrolledtext.ScrolledText(self.root)
        self.textPad.pack(fill='both', expand=1)
        self.root.wm_iconbitmap('./favicon.ico')

        self.TITLE = "Coral Text Editor"
        self.filepath = None
        self.set_title()

        menu = Menu(self.root)
        self.root.config(menu=menu)

        fileMenu = Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New", command=self.newFile, accelerator="Ctrl+N")
        fileMenu.add_command(label="Open...", command=self.openFile, accelerator="Ctrl+O")
        fileMenu.add_command(label="Save", command=self.saveFile, accelerator="Ctrl+S")
        fileMenu.add_command(label="Save As...", command=self.saveAsFile, accelerator="Ctrl+Alt+S")
        fileMenu.add_command(label="Find", command=self.findInFile, accelerator="Alt+F4")
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.exitRoot, accelerator="Alt+F4")

        helpMenu = Menu(menu)
        menu.add_cascade(label="About", command=self.about)

        self.textPad.pack()

    def text_retrieve(self):
        return self.textPad.get('1.0', END+'-1c')

    def newFile(self):
            if len(self.textPad.get('1.0', END+'-1c')) > 0:
                if messagebox.askyesno("Save current file?", "Would you like to save?"):
                    self.saveFile()
                else:
                    self.textPad.delete('1.0', END)

    def openFile(self, event=None):
        file = filedialog.askopenfile(parent=self.root, title="Select a text file", filetypes=(("Text_File", "*.txt"),("All Files", "*.*")))

        self.root.title(os.path.basename(file.name))

        if file != None:
            contents = file.read()
            self.textPad.insert('1.0', contents)
            file.close()
            self.filepath = file
            self.set_title()

    def saveFile(self, event=None):
        if self.filepath != None:
            self.saveAsFile()
        else:
            self.saveAsFile(self.filepath)

    def saveAsFile(self, event=None, file=None):
        if self.filepath == None:
            file = filedialog.asksaveasfile(mode='w', defaultextension=".txt", filetypes=(("Text_File", "*.txt"),("All Files", "*.*")))
        if file != None:
            data = self.textPad.get('1.0', END+'-1c')
            file.write(data)
            file.close()
            self.filepath = file
            self.set_title()

    def set_title(self, event=None):
        if self.filepath != None:
            title = os.path.basename(self.filepath) #figure out why this doesnt work
        else:
            title = "Untitled"
        self.root.title(title + " - " + self.TITLE)

    def findInFile(self, event=None):
        return

    def exitRoot(self, event=None):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            root.destroy()

    def about(self):
        label = messagebox.showinfo("About", "Python Based text editor with word correction")

    #highlight all misspelled words
    def highlight_misspelling(self, misspellings):
        self.textPad.tag_remove('highlight', '1.0', END)

        for word in misspellings:
            start_index = '1.0'
            while start_index:
                start_index = self.textPad.search(word, start_index, nocase=1, stopindex=END)
                if start_index:
                    end_index = '%s+%dc' % (start_index, len(word))
                    self.textPad.tag_add('highlight', start_index, end_index)
                    start_index = end_index

            self.textPad.tag_config('highlight', background='blue')
