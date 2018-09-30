import tkinter as tk
from tkinter import scrolledtext

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.status = tk.Label(anchor="w", text="woot")
        self.text = scrolledtext.ScrolledText(self.status)
        self.status.pack(side="bottom", fill="x")
        self.text.pack(side="top", fill="both", expand=True)

        self.text.insert("1.0", "Move your cursor around to see what " +
                         "index is under the cursor, and what " +
                         "text is selected\n")
        self.text.tag_add("sel", "1.10", "1.16")

        # when the cursor moves, show the index of the character
        # under the cursor
        self.text.bind("<Any-Motion>", self.on_mouse_move)

    def on_mouse_move(self, event):
        index = self.text.index("@%s,%s" % (event.x, event.y))
        ch = self.text.get(index)
        pos = "%s/%s %s '%s'" % (event.x, event.y, index, ch)
        sel = "%s-%s" % (self.text.index("sel.first"), self.text.index("sel.last"))
        self.status.configure(text="cursor: %s selection: %s" % (pos, sel))


if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()
