#function to take the data from the excel file and start the experiment

def start_Experiment():
    if 'data' not in globals():
        print("Please select a data file first")
        return
    for index, row in data.iterrows():
        set_mode(Modes[row['mode'].title()], row['duration'])