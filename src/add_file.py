# Define a function to be able to select a file from the computer and use it
import pandas as pd
def add_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                          filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if filename:
        global data
        data = pd.read_excel(filename)
        # Update the label to display the name of the selected file
        file_label.config(text=filename.split("/")[-1])
