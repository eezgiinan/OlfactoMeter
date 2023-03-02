# Function that display the data from the inputted excel file in a new window

def DisplayData():
    # Create a new window
    data_window = Toplevel(window)
    data_window.title("Data")
    data_window.geometry("600x450")

    # Create a text box to display the data
    data_text = Text(data_window)
    data_text.pack(fill=BOTH, expand=YES)

    # Check if data exists
    if 'data' in globals():
        # Convert data to a string and insert it into the text box
        data_str = str(data)
        data_text.insert(END, data_str)
    else:
        # If no data exists, display a message in the text box
        data_text.insert(END, "No data available")
