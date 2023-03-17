import enum


# Define the different modes of operation and the corresponding pin values
# 0 ON / 1 OFF
CLOSE = 1
OPEN = 0

ODOR_1 = 'Mint'
ODOR_2 = 'Almond'


class Modes(enum.Enum):
    """
    Enumeration of the different modes that the system can be IN
    """
    Resting = (CLOSE, CLOSE, CLOSE, CLOSE)  # No valves activated
    Purging = (OPEN, OPEN, CLOSE, CLOSE)  # Valve SA and SB activated to purge the system
    Odor_1 = (OPEN, CLOSE, OPEN, CLOSE)  # Valve SB and S1 activated to deliver odor 1
    Odor_2 = (OPEN, CLOSE, CLOSE, OPEN)  # Valve SB and S2 activated to deliver odor 2
    # The XLSX file needs to have the same names as here, you call the function with user input


class Odors(enum.Enum):
    """
    Different odors that the user can use
    """
    Odor_1 = ODOR_1
    Odor_2 = ODOR_2
