import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    city = ""
    list_of_cities = ["chicago", "new york city", "washington"]
    while (city not in list_of_cities):
        city = input("Which city would you like statistics on?  Enter \"Chicago\", \"New York City\", or \"Washington\": ").lower()

    # get user input for month (all, january, february, ... , june)
    month = ""
    list_of_months = ["all", "january", "february", "march", "april", "may", "june"]
    while (month not in list_of_months):
        month = input("Which month would you like statistics on?  Enter \"January\", \"February\", \"March\", \"April\", "\
            "\"May\", \"June\", or \"All\" for all months January through June: ").lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    list_of_days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    while (day not in list_of_days):
        day = input("Which day would you like statistics on?  Enter \"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", "\
            "\"Friday\", \"Saturday\", \"Sunday\", or \"All\" for everyday: ").lower()


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # create a new column that combines start and end stations
    df['start_and_end_stations'] = df['Start Station'] + ' to ' + df['End Station']
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month + 1]

    # filter by day of week if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    list_of_months = ["January", "February", "March", "April", "May", "June"]
    most_common_month = list_of_months[df['month'].mode()[0] - 1]
    print("The most common month of travel is {}".format(most_common_month))

    # display the most common day of week
    list_of_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    most_common_day = list_of_days[df['day_of_week'].mode()[0]]
    print("The most common day of travel is {}".format(most_common_day))

    # display the most common start hour
    most_common_start_hour = df['Start Time'].dt.hour.mode()[0]
    print("The most common start hour is {}".format(most_common_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is {}".format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is {}".format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    most_frequent_start_and_end_station = df['start_and_end_stations'].mode()[0]
    print("The most frequent combination of start station and end station trip is {}".format(most_frequent_start_and_end_station))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time of all trips is {} seconds".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is {} seconds".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The counts of each user type:")
    print(df['User Type'].value_counts())
    print()

    # Display counts of gender
    if "Gender" in df:
        print("The counts of each gender:")
        print(df['Gender'].value_counts())
    print()

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        print("Birth year statistics:")
        print("The earliest birth year: {}".format(int(df['Birth Year'].min())))
        print("The most recent birth year: {}".format(int(df['Birth Year'].max())))
        print("The most common birth year: {}".format(int(df['Birth Year'].mode()[0])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # See if user wants to see raw data
        row_start = 0
        see_data = ""
        see_data = input("Would you like to see some of the raw data? ")
        while see_data.lower() in ["yes", "y"]:
            print(df.iloc[row_start:row_start + 5,:])
            row_start = row_start + 5
            see_data = input("Would you like to see more raw data? ")

        

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
