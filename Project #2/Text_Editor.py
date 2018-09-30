from tkinter import Tk, scrolledtext, Menu, filedialog, END, messagebox, Label
import os

class Text_Editor:

    def __init__(self, unigramDictionary):
        self.root = Tk(className = "Text Editor")
        self.textPad = scrolledtext.ScrolledText(self.root)
        self.textPad.pack(fill='both', expand=1)
        #self.root.wm_iconbitmap('favicon.ico')

        self.TITLE = "Coral Text Editor"
        self.filepath = None
        self.set_title()

        #Top bar Menu
        menu = Menu(self.root)
        self.root.config(menu=menu)

        fileMenu = Menu(menu, tearoff=False)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New", command=self.newFile, accelerator="Ctrl+N")
        fileMenu.add_command(label="Open...", command=self.openFile, accelerator="Ctrl+O")
        fileMenu.add_command(label="Save", command=self.saveFile, accelerator="Ctrl+S")
        fileMenu.add_command(label="Save As...", command=self.saveAsFile, accelerator="Ctrl+Alt+S")
        fileMenu.add_command(label="Find", command=self.findInFile, accelerator="Alt+F4")
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.exitRoot, accelerator="Alt+F4")

        editMenu = Menu(menu, tearoff=False)
        menu.add_cascade(label="Edit", menu=editMenu)
        editMenu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        editMenu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        editMenu.add_separator()
        editMenu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        editMenu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        editMenu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        editMenu.add_command(label="Select All", command=self.selectAll, accelerator="Ctrl+A")

        helpMenu = Menu(menu, tearoff=False)
        menu.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_cascade(label="About", command=self.about)

        #Popup menu word correction dictionary
        self.suggestionDict = {}
        self.addedWords = []
        self.dictionaryPath = unigramDictionary

        self.bindings()

        #status bar
        #self.status = Label(self.root, text = "Lines: 0 Words: 0 Characters: 0", bd=1, anchor='w')
        #self.status.pack(side='bottom', fill='x')

        self.textPad.pack()

    def text_retrieve(self):
        return self.textPad.get('1.0', END+'-1c')

    def newFile(self, event=None):
            if len(self.textPad.get('1.0', END+'-1c')) > 0:
                if messagebox.askyesno("Save current file?", "Would you like to save?"):
                    self.saveFile()

            self.textPad.delete('1.0', END)

            self.filepath = None
            self.set_title()

    def openFile(self, event=None):
        file = filedialog.askopenfile(parent=self.root, title="Select a text file", filetypes=(("Text_File", "*.txt"),("All Files", "*.*")))

        if file != None:
            contents = file.read()
            self.textPad.insert('1.0', contents)
            file.close()
            self.filepath = file
            self.set_title()

    def saveFile(self, event=None):
        if self.filepath == None:
            self.saveAsFile()
        else:
            self.saveAsFile(file=self.filepath)

    def saveAsFile(self, event=None, file=None):
        if file==None:
            file = filedialog.asksaveasfile(mode='w', defaultextension=".txt", filetypes=(("Text_File", "*.txt"),("All Files", "*.*")))
        with open(file.name, 'wb') as f:
            data = self.textPad.get('1.0', END+'-1c')
            f.write(bytes(data, 'UTF-8'))
            self.filepath = file
            self.set_title()

    def set_title(self, event=None):
        if self.filepath != None:
            title = os.path.basename(self.filepath.name) #figure out why this doesnt work
        else:
            title = "Untitled"
        self.root.title(title + " - " + self.TITLE)

    def findInFile(self, event=None):
        return

    def exitRoot(self, event=None):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            root.destroy()

    def about(self, event=None):
        label = messagebox.showinfo("About", "Python Based text editor with word correction")

    def undo(self, event=None):
        self.textPad.edit_undo()

    def redo(self, event=None):
        self.textPad.edit_redo()

    def cut(self, event=None):
        self.copy()
        self.delete


    def copy(self, event=None):
        text = self.textPad.get("sel.first", "sel.last")
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def paste(self, event=None):
        text = self.root.selection_get(selection='CLIPBOARD')
        self.textPad.insert('insert', text)

    def selectAll(self, event=None):
        self.textPad.tag_add("sel",'1.0','end')

    def delete(self, event=None):
        self.textPad.delete("sel.first", "sel.last")

    #highlight all misspelled words
    def highlight_misspelling(self, misspellings, color):#fix this so it only highlight full words
        self.textPad.tag_remove('highlight', '1.0', END)

        for word in misspellings:
            start_index = '1.0'
            while start_index:
                start_index = self.textPad.search('\\y' + word + '\\y', start_index, forwards=True, nocase=False, stopindex=END, regexp=True) #regex '\\y' to only find complete words
                if start_index:
                    end_index = '%s+%dc' % (start_index, len(word))
                    self.textPad.tag_add('highlight', start_index, end_index)
                    start_index = end_index

            self.textPad.tag_config('highlight', foreground=color, underline=True)

    def wordUnderCursor(self, x_position, y_position):
        start_index = self.textPad.index('@%s,%s wordstart' % (x_position, y_position))
        end_index = self.textPad.index('@%s,%s wordend' % (x_position, y_position))

        word = self.textPad.get(start_index, end_index)

        return word, start_index, end_index

    def correctMispelling(self, correction, start_index, end_index):
        self.textPad.delete(start_index, end_index)
        self.textPad.insert(start_index, correction)

    def addWord(self, word):
        self.addedWords.append(word)

        with open(self.dictionaryPath, 'a') as f:
            f.write('\n%s %d' % (word, 1))

    #def statusBar(self, event=None):
    #    text = self.text_retrieve()
    #    self.status.config(text="Lines: %s Words: %s Characters: %s" % (str(textPad.index('end').split('.')[0]), str(len(text)), str(len(text))))


    def rightClickMenu(self, event=None):
        word, start_index, end_index = self.wordUnderCursor(event.x, event.y)

        popupMenu = Menu(self.root, tearoff=False)

        if word in self.suggestionDict:

            for suggestion in self.suggestionDict[word]:
                popupMenu.add_command(label=suggestion, command=lambda correction=suggestion: self.correctMispelling(correction, start_index, end_index))

            popupMenu.add_command(label=("Add '" + word + "' to the dictionary..." ), command=lambda: self.addWord(word))
            popupMenu.add_separator()

        popupMenu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        popupMenu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        popupMenu.add_separator()
        popupMenu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        popupMenu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        popupMenu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        popupMenu.add_command(label="Delete", command=self.delete, accelerator="Del")
        popupMenu.add_command(label="Select All", command=self.selectAll, accelerator="Ctrl+A")

        #Popup popup menu
        popupMenu.post(event.x_root, event.y_root)


    def bindings(self):
        #File menu bindings
        self.textPad.bind("<Control-n>", self.newFile)
        self.textPad.bind("<Control-N>", self.newFile)
        self.textPad.bind("<Control-o>", self.openFile)
        self.textPad.bind("<Control-O>", self.openFile)
        self.textPad.bind("<Control-s>", self.saveFile)
        self.textPad.bind("<Control-S>", self.saveFile)
        self.textPad.bind("<Control-Alt-s>", self.saveAsFile)
        self.textPad.bind("<Control-Alt-S>", self.saveAsFile)
        self.textPad.bind("<Alt-F4>", self.exitRoot)

        #Edit menu bindings
        self.textPad.bind("<Control-y>", self.redo)
        self.textPad.bind("<Control-Y>", self.redo)
        self.textPad.bind("<Control-Z>", self.undo)
        self.textPad.bind("<Control-z>", self.undo)

        #Popup menu binding
        self.textPad.bind("<Button-3>", self.rightClickMenu)

        #Status bar binding
        #self.textPad.bind("<Key>", self.statusBar)
