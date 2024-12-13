import pandas as pd
import numpy as np

# Load and prepare the data
def prepare_data(file_path):
    # Read the CSV file
    barc_data = pd.read_csv('Program_Level_hsm_Aug24.csv')
    
    # Create separate dataframes for Level 2 and Level 4
    program_data = barc_data[barc_data['Level'] == 'Level 2']
    minute_data = barc_data[barc_data['Level'] == 'Level 4']
    
    return program_data, minute_data

def calculate_rating_drops(program_name, program_data, minute_data):
    # Filter data for specific program
    prog_breaks = program_data[program_data['Master Programme'] == program_name]
    prog_minutes = minute_data[minute_data['Master Programme'] == program_name]
    
    # Initialize a list to store drops for each break
    break_drops = []
    
    # Process each ad break
    for break_num, ad_break in prog_breaks.iterrows():
        break_start = ad_break['Start Time']
        break_end = ad_break['End Time']
        break_rating = ad_break['F 22-40 ABC']
        
        # Get minute-by-minute ratings during this break
        break_minutes = prog_minutes[
            (prog_minutes['Start Time'] >= break_start) & 
            (prog_minutes['End Time'] <= break_end)
        ]
        
        if not break_minutes.empty:
            # Calculate percentage drop for each minute
            minute_drops = ((break_minutes['F 22-40 ABC'] - break_rating) / break_rating) * 100
            break_drops.append(minute_drops.mean())
    
    return break_drops

# Main execution
def main():
    # Load the data
    program_data, minute_data = prepare_data('Program_Level_hsm_Aug24.csv')
    
    # Get unique programs
    programs = program_data['Master Programme'].unique()
    
    # Calculate drops for each program
    for program in programs:
        drops = calculate_rating_drops(program, program_data, minute_data)
        if drops:
            print(f"\nProgram: {program}")
            print(f"Average rating drops: {drops}")

if __name__ == "__main__":
    main()
