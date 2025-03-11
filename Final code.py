#
# File: Assignment2.py
# Author: Ajith Kumar Balamurugan
# Student ID: 110404235
# Email ID: balay044@mymail.unisa.edu.au
# This is my own work as defined by
# the University's Academic Misconduct Policy.
#
def main():
    """
    The purpose of the main function to handle the timetable management by presenting a menu and 
    performs actions according to the user's selection by executing corresponding functions
    """
    print("Title: Assignment -2\nAuthor: Ajith Kumar Balamurugan\nEmail ID: balay044@mymail.unisa.edu.au")
    # timetable dictionary to store events
    timetable = {
        "Sun": [],
        "Mon": [],
        "Tue": [],
        "Wed": [],
        "Thu": [],
        "Fri": [],
        "Sat": []
    }

    # list to store standard work hours
    work_hours = ["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm"]
    # list to store days
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    # start_day to store default start day
    start_day = "Sun"

    start = True # Flag
    while start:
        menu_print()
        # command to store the user option
        command = input("Please choose any one of the above options to proceed: ")
        if command == '1':
            create_event(timetable, days)
        elif command == '2':
            update_event(timetable, days)
        elif command == '3':
            delete_event(timetable, days)
        elif command == '4':
            print_timetable(timetable, start_day, work_hours, days)
        elif command == '5':
            print_day_schedule(timetable)
        elif command == '6':
            start_day = set_start_day(days)
        elif command == '7':
            search_event(timetable, days)
        elif command == '8':
            save_timetable(timetable)
        elif command == '9':
            timetable = load_timetable()
        elif command == '10':
            start = False
        else:
            print("The provided option is incorrect. Please provide the correct option.")

def menu_print():
    """
    This function prints the menu options for the user.
    """
    print("\n Timetable options:")
    print("1. Create event")
    print("2. Update event")
    print("3. Delete event")
    print("4. Print week schedule")
    print("5. Print day schedule")
    print("6. Set start day")
    print("7. Search event")
    print("8. Save timetable")
    print("9. Load timetable")
    print("10. Quit")

def create_event(timetable, days):
    """
    This function creates a new event in the timetable.
    It takes parameters timetable and days.
    """
    print("Create Event:")
    # day to store the input from the user for given day
    day = input("Enter the day (Sun, Mon, Tue, Wed, Thu, Fri, Sat): ")
    while day not in timetable:
        print("The provided day is incorrect. Please provide the correct option.")
        day = input("Enter the day (Sun, Mon, Tue, Wed, Thu, Fri, Sat): ")
    # title to store the user title of the event
    title = input("Please enter the title of the scheduled event: ")
    # start_time to store the given start time from the user
    start_time = input("Please enter the start time: ")
    while not is_valid_time_format(start_time):
        print("The provided time is in incorrect format or not valid. Please provide the correct time.")
        start_time = input("Please enter the start time: ")
    # end_time to store the given end time from the user
    end_time = input("Please enter the end time: ")
    while not is_valid_time_format(end_time) or time_sort_key(end_time) <= time_sort_key(start_time):
        print("The provided time is in incorrect format or end time before start time. Please provide the correct time.")
        end_time = input("Please enter the end time: ")
    # location to store the given location from the user
    location = input("Please enter where it is held (optional): ")
    # event dictionary to store the title, start and end time, location
    event = {
        "title": title,
        "start_time": start_time,
        "end_time": end_time,
        "location": location
    }

    if not check_overlap(timetable[day], event):
        timetable[day].append(event)
        print("Event created successfully.")
    else:
        print("Sorry, the event overlaps with an existing event. Please try with different timings.")

def update_event(timetable, days):
    """
    This function updates an existing event in the timetable. 
    It takes parameters timetable and days.
    """
    print("Update Event:")

    day = input("Enter the day (Sun, Mon, Tue, Wed, Thu, Fri, Sat): ")
    while day not in timetable:
        print("The provided day is incorrect. Please provide the correct option.")
        day = input("Enter the day (Sun, Mon, Tue, Wed, Thu, Fri, Sat): ")

    # search_method to store option from user to search by start time or keyword
    search_method = input("Please enter '1' to search the event for update by start time or '2' by keyword? ").strip()
    while search_method not in ['1', '2']:
        print("Invalid option. Please choose '1' to search by start time or '2' by keyword.")
        search_method = input("Please enter '1' to search the event for update by start time or '2' by keyword? ").strip()

    found = False  # Flag
    if search_method == '2':
        keyword = input("Please enter the keyword in event titles or locations: ").strip().lower()
        events_matched = [event for event in timetable[day] if keyword in event["title"].lower() or keyword in event["location"].lower()]
        if not events_matched:
            print(f"No events found matching '{keyword}' on {day}.")
        elif len(events_matched) == 1:
            event = events_matched[0]
            found = True
        else:
            print(f"Multiple events found matching '{keyword}' on {day}:")
            for i in range(len(events_matched)):
                event = events_matched[i]
                print(f"{i + 1}. Title: {event['title']}, Start Time: {event['start_time']}, Location: {event['location']}")
            choice = int(input("Please choose the event number to update: "))
            event = events_matched[choice - 1]
            found = True
    else:
        start_time = input("Please enter the start time of the event to update: ")
        while not is_valid_time_format(start_time):
            print("The provided time is in incorrect format or not valid. Please provide the correct time.")
            start_time = input("Please enter the start time of the event to update: ")
        events_matched = [event for event in timetable[day] if event["start_time"] == start_time]
        if not events_matched:
            print(f"No events found with start time '{start_time}' on {day}.")
        else:
            event = events_matched[0]
            found = True

    if found:
        print("Please update new details for the event:")
        # new_title to store the updated title from the user
        new_title = input(f"Current title of the event is ({event['title']}). Update new title if any, otherwise please press enter: ")
        # new_start_time to store the updated start time from the user
        new_start_time = input(f"Current start time is ({event['start_time']}). Update new start time if any, otherwise please press enter: ")
        if new_start_time:
            while not is_valid_time_format(new_start_time):
                print("The provided time is in incorrect format or not valid. Please provide the correct time.")
                new_start_time = input(f"Current start time is ({event['start_time']}). Update new start time if any, otherwise please press enter: ")
        # new_end_time to store the updated end time from the user
        new_end_time = input(f"Current end time is ({event['end_time']}). Update new end time if any, otherwise please press enter: ")
        if new_end_time:
            while not is_valid_time_format(new_end_time) or time_sort_key(new_end_time) <= time_sort_key(new_start_time if new_start_time else event["start_time"]):
                print("The provided time is in incorrect format or end time before start time. Please provide the correct time.")
                new_end_time = input(f"Current end time is ({event['end_time']}). Update new end time if any, otherwise please press enter: ")
        new_location = input(f"Current location is ({event['location']}). Update new location if any, otherwise please press enter: ")

        # dictionary to store updated details
        updated_event = {
            "title": new_title if new_title else event["title"],
            "start_time": new_start_time if new_start_time else event["start_time"],
            "end_time": new_end_time if new_end_time else event["end_time"],
            "location": new_location if new_location else event["location"]
        }

        timetable[day].remove(event)
        if not check_overlap(timetable[day], updated_event):
            timetable[day].append(updated_event)
            print("The event is updated successfully.")
        else:
            print("Sorry, the updated event overlaps with an existing event. Please try with different timings.")
            timetable[day].append(event)

def delete_event(timetable, days):
    """
    This function deletes an event from the timetable.
    It takes parameters timetable and days.
    """
    print("Delete Event:")

    day = input("Enter the day (Sun, Mon, Tue, Wed, Thu, Fri, Sat): ")
    while day not in timetable:
        print("The provided day is incorrect. Please provide the correct option.")
        day = input("Enter the day (Sun, Mon, Tue, Wed, Thu, Fri, Sat): ")

    search_method = input("Please enter '1' to search the event for delete by start time or '2' by keyword? ").strip()
    while search_method not in ['1', '2']:
        print("Invalid option. Please choose '1' to search by start time or '2' by keyword.")
        search_method = input("Please enter '1' to search the event for delete by start time or '2' by keyword? ").strip()

    found = False  # Flag 

    if search_method == '2':
        keyword = input("Please enter the keyword in event titles or locations: ").strip().lower()
        events_matched = [event for event in timetable[day] if keyword in event["title"].lower() or keyword in event["location"].lower()]
        if not events_matched:
            print(f"No events found matching '{keyword}' on {day}.")
        elif len(events_matched) == 1:
            event = events_matched[0]
            found = True
        else:
            print(f"Multiple events found matching '{keyword}' on {day}:")
            for i in range(len(events_matched)):
                event = events_matched[i]
                print(f"{i + 1}. Title: {event['title']}, Start Time: {event['start_time']}, Location: {event['location']}")
            choice = int(input("Please choose the event number to delete: "))
            event = events_matched[choice - 1]
            found = True
    else:
        start_time = input("Please enter the start time of the event to delete: ")
        while not is_valid_time_format(start_time):
            print("The provided time is in incorrect format or not valid. Please provide the correct time.")
            start_time = input("Please enter the start time of the event to delete: ")
        events_matched = [event for event in timetable[day] if event["start_time"] == start_time]
        if not events_matched:
            print(f"No events found with start time '{start_time}' on {day}.")
        else:
            event = events_matched[0]
            found = True

    if found:
        timetable[day].remove(event)
        print("The event is deleted successfully.")

def print_timetable(timetable, start_day, work_hours, days):
    """
    This function prints the entire timetable for the week, starting from the specified day.
    It takes parameters timetable, start_day, work_hours and days.
    """
    # start_index to store starting index of week based on specified start day
    start_index = days.index(start_day)
    # ordered_days contains orders of days of the week
    ordered_days = days[start_index:] + days[:start_index]
    
    # list to hold all events
    all_events = []
    for day in timetable:
        for event in timetable[day]:
            all_events.append((day, event))
    # This function sorts all events by day and time
    def event_sort_key(event):
        day, evt = event
        day_index = days.index(day)
        return (day_index, get_time_index(evt))

    all_events.sort(key=event_sort_key)
    # unique_times to store time outside work hours 
    unique_times = work_hours.copy()
    for day_event in all_events:
        time_slot = day_event[1]["start_time"]
        if time_slot not in unique_times:
            unique_times.append(time_slot)
    unique_times.sort(key=time_sort_key)

    print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format("", *ordered_days))
    print("-" * 90)

    for time_slot in unique_times:
        print("{:<10}".format(time_slot if time_slot in work_hours else ""), end="")
        for day in ordered_days:
            event_printed = False
            for day_event in all_events:
                if day_event[0] == day and day_event[1]["start_time"] == time_slot:
                    event = day_event[1]
                    title = event["title"][:8] + '...' if len(event["title"]) > 8 else event["title"]
                    print("{:<10}".format(title), end="")
                    event_printed = True
            if not event_printed:
                print("{:<10}".format(""), end="")
        print()

        print("{:<10}".format(""), end="")
        for day in ordered_days:
            event_printed = False
            for day_event in all_events:
                if day_event[0] == day and day_event[1]["start_time"] == time_slot:
                    event = day_event[1]
                    time_range = f"{event['start_time']}-{event['end_time']}"[:10]
                    print("{:<10}".format(time_range), end="")
                    event_printed = True
            if not event_printed:
                print("{:<10}".format(""), end="")
        print()

        print("{:<10}".format(""), end="")
        for day in ordered_days:
            event_printed = False
            for day_event in all_events:
                if day_event[0] == day and day_event[1]["start_time"] == time_slot:
                    event = day_event[1]
                    location = event["location"][:8] + '...' if len(event["location"]) > 8 else event["location"]
                    print("{:<10}".format(location), end="")
                    event_printed = True
            if not event_printed:
                print("{:<10}".format(""), end="")
        print()

        print("-" * 90)

def print_day_schedule(timetable):
    """
    This function prints the schedule for a specific day.
    It takes parameter timetable.
    """
    day = input("Please enter the day (Sun, Mon, Tue, Wed, Thu, Fri, Sat): ")
    while day not in timetable:
        print("The provided day is incorrect. Please provide the correct option.")
        day = input("Please enter the day (Sun, Mon, Tue, Wed, Thu, Fri, Sat): ")
    if not timetable[day]:
        print(f"\nNo events scheduled for {day}.")
    else:
        sorted_events = sorted(timetable[day], key=get_time_index)
        print(f"\nEvents scheduled for {day}:")
        for event in sorted_events:
            print(f"Title: {event['title']}")
            print(f"Start Time: {event['start_time']}")
            print(f"End Time: {event['end_time']}")
            print(f"Location: {event['location']}\n")

def set_start_day(days):
    """
    This function sets the starting day of the week for the timetable.
    It takes parameter days.
    """
    day = input("Please enter the start day of the week (Sun or Mon): ")
    while day not in days:
        print("The provided day is incorrect. Please provide the correct option.")
        day = input("Please enter the start day of the week (Sun or Mon): ")
    print(f"Start day set to {day}.")
    return day

def search_event(timetable, days):
    """
    This function search for an event in the timetable by keyword.
    It takes parameters timetable and days.
    """
    keyword = input("Please enter the keyword to search for in event titles or locations: ").strip().lower()
    events_matched = []

    for day in timetable:
        for event in timetable[day]:
            if keyword in event["title"].lower() or keyword in event["location"].lower():
                events_matched.append((day, event))

    def event_sort_key(event):
        day, evt = event
        day_index = days.index(day)
        return (day_index, get_time_index(evt))
    if events_matched:
        events_matched.sort(key=event_sort_key)
        print(f"\nEvents matching '{keyword}':")
        for day, event in events_matched:
            print(f"Day: {day}")
            print(f"Title: {event['title']}")
            print(f"Start Time: {event['start_time']}")
            print(f"End Time: {event['end_time']}")
            print(f"Location: {event['location']}\n")
    else:
        print(f"No events found matching '{keyword}'.")

def save_timetable(timetable):
    """
    This function saves the timetable to a file.
    It takes parameter timetable.
    """
    # filename to store the user given name for the file
    filename = input("Please enter the filename to save the timetable: ")
    try:
        with open(filename, 'w') as file:
            for day, events in timetable.items():
                for event in events:
                    file.write(f"{day},{event['title']},{event['start_time']},{event['end_time']},{event['location']}\n")
        print("Timetable saved successfully.")
    except:
        print("An error occurred while saving the timetable. Please try again.")

def load_timetable():
    """
    This function loads the timetable from a file.
    It returns the timetable dictionary.
    """
    filename = input("Please enter the filename to load the timetable: ")
    try:
        timetable = { "Sun": [], "Mon": [], "Tue": [], "Wed": [], "Thu": [], "Fri": [], "Sat": [] }
        with open(filename, 'r') as file:
            for line in file:
                day, title, start_time, end_time, location = line.strip().split(',')
                event = {
                    "title": title,
                    "start_time": start_time,
                    "end_time": end_time,
                    "location": location
                }
                timetable[day].append(event)
        print("Timetable loaded successfully.")
        return timetable
    except:
        print("Filename does not exists. Please check the file name and try again")
        return { "Sun": [], "Mon": [], "Tue": [], "Wed": [], "Thu": [], "Fri": [], "Sat": [] }
    
def time_sort_key(time):
    """
    This function sort key for times in the format of '11am', '8:30pm', etc.
    It takes parameter time and returns hour and minute for sorting.
    """
    period = time[-2:]
    if ':' in time[:-2]:
        hour, minute = time[:-2].split(':')
        hour = int(hour)
        minute = int(minute)
    else:
        hour = int(time[:-2])
        minute = 0

    if period == 'pm' and hour != 12:
        hour += 12
    if period == 'am' and hour == 12:
        hour = 0
    return (hour, minute)

def is_valid_time_format(time):
    """
    This function checks if the provided time string follows a valid format.
    It takes parameter time. It returns True if valid, otherwise False.
    """
    if len(time) < 3 or time[-2:] not in ["am", "pm"]:
        return False
    try:
        parts = time[:-2].split(':')
        if len(parts) == 2:
            hour, minute = parts
            hour, minute = int(hour), int(minute)
        elif len(parts) == 1:
            hour = int(parts[0])
            minute = 0
        else:
            return False
        return 1 <= hour <= 12 and 0 <= minute < 60
    except:
        return False

def get_time_index(event):
    """
    This function retrieves the sorting key for an event based on its start time.
    It takes parameter event and returns hour and minute for sorting.
    """
    return time_sort_key(event["start_time"])

def check_overlap(day_events, new_event):
    """
    This function checks whether a new event overlaps with existing events.
    It takes parameter days_events, new_event.
    """
    new_start = time_sort_key(new_event["start_time"])
    new_end = time_sort_key(new_event["end_time"])

    for event in day_events:
        start = time_sort_key(event["start_time"])
        end = time_sort_key(event["end_time"])

        if not (new_end <= start or new_start >= end):
            return True
    return False

# Calling the main function
main()

