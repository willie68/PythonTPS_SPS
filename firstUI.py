import tkinter as tk
 
# Create our master object to the Application
master = tk.Tk()
 
# Create the text widget
text_widget = tk.Text(master, height=5, width=40)
 
# Create a scrollbar
scroll_bar = tk.Scrollbar(master)
 
# Pack the scroll bar
# Place it to the right side, using tk.RIGHT
scroll_bar.pack(side=tk.RIGHT)
 
# Pack it into our tkinter application
# Place the text widget to the left side
text_widget.pack(side=tk.LEFT)
 
long_text = """This is a multiline string.
We can write this in multiple lines too!
Hello from AskPython. This is the third line.
This is the fourth line. Although the length of the text is longer than
the width, we can use tkinter's scrollbar to solve this problem!
"""
 
# Insert text into the text widget
text_widget.insert(tk.END, long_text)
 
# Start the mainloop
tk.mainloop()