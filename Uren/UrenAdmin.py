'''
Created on Dec 28, 2020
Script to analyze working hours from a Google Calendar ICS file.
@author: wimz
https://docs.google.com/spreadsheets/d/1W-PMcJUuFpVckV7ScBmmIBxrBChOw_Lk1IHXgyk8szU/edit?usp=sharing
'''

from copy import deepcopy
from datetime import datetime
import pandas as pd

# Constants
ICS_FILE_PATH = "UREN_hom21kum9j6s2s59jtkk6gijn8@group.calendar.google.com.ics"
STANDARD_YEARLY_HOURS = 1818  # Standard number of working hours per year

def calculate_fraction_of_year():
    """
    Calculate what fraction of the year has passed so far.

    Returns:
        float: Fraction of the year that has passed (0.0 to 1.0)
    """
    date_obj = datetime.now()
    year = date_obj.year

    # Calculate the total number of days in the year (accounting for leap years)
    days_in_year = 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365

    # Calculate the day of the year for the given date
    day_of_year = (date_obj - datetime(year, 1, 1)).days + 1

    # Calculate the fraction of the year
    return day_of_year / days_in_year


def parse_ics_file(file_path):
    """
    Parse an ICS file and extract calendar items.

    Args:
        file_path (str): Path to the ICS file

    Returns:
        list: List of calendar items, where each item is a list of lines
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    calendar_items = []
    current_item = []

    for line in lines:
        if line.startswith("BEGIN:"):
            current_item = []

        current_item.append(line)

        if line.startswith("END:"):
            calendar_items.append(deepcopy(current_item))

    return calendar_items


def extract_work_hours(calendar_items):
    """
    Extract work hours from calendar items.

    Args:
        calendar_items (list): List of calendar items

    Returns:
        list: List of dictionaries with date and hours information
    """
    work_records = []
    work_details = []

    for item in calendar_items:
        hours = 0.0
        date_str = ""
        summary_text = ""

        for line in item:
            if line.startswith("DTSTART"):
                date_str = line.split(":")[1].strip()[:8]  # Extract date in format YYYYMMDD

            if line.startswith("SUMMARY"):
                summary_text = line.split(":")[1].strip()
                first_word = summary_text.split()[0].lower()

                if first_word in ["ziek", "werkuren"]:
                    try:
                        hours_str = summary_text.split(" ")[1]
                        hours_str = hours_str.replace(",", ".").replace("\\", "")
                        hours = float(hours_str)
                    except (ValueError, IndexError):
                        print(f"Error parsing hours: '{hours_str}' in line: {line}")

        if hours > 0.0:
            work_details.append(f"{date_str} : {summary_text:20} = {hours:.1f}")
            work_records.append({"date": date_str, "hours": hours})

    return work_records


def analyze_yearly_hours(df, current_year=None):
    """
    Analyze working hours by year.

    Args:
        df (DataFrame): DataFrame containing work records
        current_year (str, optional): Current year to analyze in detail. Defaults to None.
    """
    years_to_analyze = ["2020", "2021", "2022", "2023", "2024", "2025"]

    for year in years_to_analyze:
        print(f"________ Overzicht {year}")

        # Filter data for the current year
        df_year = df[df.date.str[:4] == year]

        # Handle duplicates
        duplicates = df_year[df_year.duplicated()]
        if len(duplicates) > 0:
            print("ERROR duplicates found (Google Calendar bug - events appear twice in log)")
            print(duplicates)
            print("Removing duplicates...")
            df_year = df_year.drop_duplicates()

        # Calculate total hours worked
        hours_worked = df_year["hours"].sum()
        print(f"Totaal uren {year}: {hours_worked:.1f}")

        # Additional analysis for the current year
        if year == current_year:
            df_year_sorted = df_year.sort_values("date")
            print("\nRecent work records:")
            print(df_year_sorted.tail(20))

            # Calculate expected hours
            today = datetime.now()
            jan_1 = datetime(today.year, 1, 1)
            days_since_jan_1 = (today - jan_1).days

            print(f"Days since January 1st this year: {days_since_jan_1}")

            expected_hours = calculate_fraction_of_year() * STANDARD_YEARLY_HOURS
            print(f"Verwachte uren {year}: {expected_hours:.1f}")
            print(f"Gewerkte uren {year}: {hours_worked:.1f}")
            print(f"Verschil (uren): {hours_worked - expected_hours:.1f}")
            print()


def main():
    """Main function to run the hours analysis."""
    # Parse the ICS file
    calendar_items = parse_ics_file(ICS_FILE_PATH)

    # Extract work hours
    work_records = extract_work_hours(calendar_items)

    # Create DataFrame
    df = pd.DataFrame(work_records)

    # Analyze hours by year
    current_year = str(datetime.now().year)
    analyze_yearly_hours(df, current_year)


if __name__ == '__main__':
    main()
