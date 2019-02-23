import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'nyc': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHowdyyy!! Let me take you on a fun adventurous exploration into some US bikeshare data!')
    err_msg = "\nOopsie! Something doesn\'t look right in the \"{}\" name. I\'ll let you try the {} again, cause I\'m cool like that!!\nFollow these helpful instructions below, You Can Do It!!\n"
    #Getting user input for city (chicago, nyc, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nFirst up! Enter one of the following city names,\nChicago (or) NYC (or) Washington:\nYour Entry for City: ").lower()
        if city in ['chicago', 'nyc', 'washington']:
            break
        print(err_msg.format(city, 'city'))

    #Getting user input for month (all, january, february, ... , june)
    while True:
        month = input("\nGreat Choice!\nNow, tell me which month in this city would you like to see data by entering one of the following month names,\nALL (or) january (or) february (or) march (or) april (or) may (or) june:\nYour Entry for Month: ").lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        print(err_msg.format(month, 'month'))

    #Getting user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nAlrighty then!!! We are almost there!!\nEnter one of the following day-of-the-week names,\nALL (or) sunday (or) monday (or) tuesday (or) wednesday (or) thursday (or) friday (or) saturday:\nYour Entry for Day-of-the-Week: ").lower()
        if day in ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
            break
        print(err_msg.format(day, 'day of the week'))

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time_x'] = pd.to_datetime(df['Start Time'])

    # extract month day and day of week from Start Time to create new columns
    df['month'] = df['Start Time_x'].dt.month
    df['day_name'] = df['Start Time_x'].dt.weekday_name
    df['hour'] = df['Start Time_x'].dt.hour
    df['day'] = df['Start Time_x'].dt.day

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_name'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n\n~~Brace Yourselves, Data Is Coming~~')
    print('-'*40)
    print('\n\nThe Most Frequent Times of Travel:')
    start_time = time.time()

    #Display the most common month
    com_mon = df['Start Time_x'].dt.strftime('%B')
    print("Most Common Month is, ", com_mon.mode()[0])

    #Display the most common day of week
    print("Most Common Day of the Week is, ", df['day_name'].mode()[0])

    #Display the most common start hour
    com_hr = df['Start Time_x'].dt.strftime('%I:00 %p')
    print("Most Common Hour is, ", com_hr.mode()[0])

    #Display the most common day of month
    print("Most Common Day of the Month is, ", df['day'].mode()[0])

    print("\nThat just took %s seconds! Awesome huh?!?" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n\nThe Most Popular Stations and Trip:\n')
    start_time = time.time()

    #Display most commonly used start station
    print("Most common start station used is, ", df['Start Station'].mode()[0])

    #Display most commonly used end station
    print("Most common end station used is, ", df['End Station'].mode()[0])

    #Display most frequent combination of start station and end station trip
    df['combo_stations'] = df['Start Station'] + '$' + df['End Station']
    most_com_combo = df['combo_stations'].mode().loc[0]
    print("\nCommonly used start and stop combination stations are, \nStart Station: ", most_com_combo.split('$')[0])
    print("Stop Station: ", most_com_combo.split('$')[1])

    print("\nThat just took %s seconds! Great right?!?" % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n\nTrip Duration Stats:')
    start_time = time.time()

    #Display total travel time
    print("Total Travel Time is, ", df['Trip Duration'].sum())

   #Display mean travel time
    print("Mean Travel Time is, ", df['Trip Duration'].mean())

    print("\nThat just took %s seconds! Easy Peasy!!" % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n\nUser Stats:\n')
    start_time = time.time()

    #Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of User Types are,\n", user_types.to_string())

    #Display counts of gender
    if 'Gender' in df.columns:
        df['Gender'] = df['Gender'].fillna('Unkown')
        gender_types = df['Gender'].value_counts()
        print("\nGender Counts are,\n",  gender_types.to_string())

    #Display earliest, most recent, average and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nEarliest Birth Year is, ", int(np.min(df['Birth Year'])))
        print("Most recent Birth Year is, ", int(np.max(df['Birth Year'])))
        print("The Average Birth Year is, ", int(np.average(df['Birth Year'])))
        print("Most common Birth Year is, ", int(df['Birth Year'].mode()[0]))

    print("\nThat just took %s seconds! Im a data genie!!" % (time.time() - start_time))
    print('-'*40)

def format_output(df):
    """Edits dataframe values ready for desired display."""

    df.drop(['month', 'day_name', 'hour', 'Start Time_x', 'combo_stations'], axis=1, inplace=True)
    if 'Birth Year' in df.columns:
        df['Birth Year'] = int(np.min(df['Birth Year']))

def individual_trips(df):
    """Displays individual trip data."""
    indv_trip = input("Would you like to view individual trips? Type yay (or) nay.\n").lower()
    row_num = 0

    while True:
        if indv_trip != 'nay':
            print('\nDisplaying Individual Trip data...\n')
            print(str(df.iloc[row_num : row_num + 5, :].to_dict('records')).replace(", ", ",\n").replace("{'Unnamed: 0", "\n{ "))
            row_num += 5
            indv_trip = input("\nWanna see more trips? Type yay (or) nay.\n").lower()
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        format_output(df)
        individual_trips(df)

        restart = input('\nWould you like to restart the program and see stats for another city? Enter yay (highly recommended!) (or) nay.\n').lower()
        if restart != 'yay':
            print("See you again soon! GoodBye!")
            break

if __name__ == "__main__":
	main()
