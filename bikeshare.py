from calendar import month
from importlib import import_module
from statistics import mode
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'newyorkcity': 'new_york_city.csv',
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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago','newyorkcity','washington']
    city = None
    while(city == None):
        city = input("Would you like to see data for Chicago, New York, or Washington ? \n")
        if city.lower().replace(" ", "") not in cities:
            print("Oh! invaild input please try again")
            city = None
        else:
            city = city.lower().replace(" ", "")
            break
        
    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['all','january', 'february', 'march', 'april', 'may', 'june']
    month = None
    while(month == None):
        month = input("Which month - January, February, March, April, May, June, or all ? \n")
        if month.lower().replace(" ", "") not in months:
            print("Oh! invaild input please try again")
            month = None
        else:
            month = month.lower().replace(" ", "")
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    day = None
    while(day == None):
        day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all ? \n")
        if day.lower().replace(" ", "") not in days:
            print("Oh! invaild input please try again")
            day = None
        else:
            day = day.lower().replace(" ", "")
            break

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
    #load the data into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday

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
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        day = days.index(day)

        # filter by month to create the new dataframe
        df = df[df['day'] == day]
        

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    df['month'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['month'].dt.month
    pop_month = df['month'].mode()[0]
    print("The most popular month is {}".format(months[pop_month - 1]).title())

    # TO DO: display the most common day of week
    days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    df['day'] = pd.to_datetime(df['Start Time'])
    df['day'] = df['Start Time'].dt.weekday
    pop_day = df['day'].mode()[0]
    print("The most popular day is {}".format(days[pop_day].title()))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    pop_hour = df['hour'].mode()[0]
    print("The most popular hour is {}".format(pop_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    pop_startstation = df['Start Station'].mode()[0]
    print("The most popular Start station is {}".format(pop_startstation))

    # TO DO: display most commonly used end station
    pop_endstation = df['End Station'].mode()[0]
    print("The most popular End station is {}".format(pop_endstation))

    # TO DO: display most frequent combination of start station and end station trip
    pop_station = (df['Start Station']+' to '+df['End Station']).mode()[0]
    print("The most popular start to end trip is {}".format(pop_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    trip_total = df['Trip Duration'].sum()
    print("The total trip duration is {}".format(trip_total))

    # TO DO: display mean travel time
    trip_mean = df['Trip Duration'].mean()
    print("The mean trip duration is {}".format(trip_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    type_count = pd.value_counts(df['User Type'])
    print("The number of each user type:\n",type_count)

    # TO DO: Display counts of gender
    if "Gender" in df:
        gend_count = pd.value_counts(df['Gender'])
        print("The number of each Gender:\n",gend_count)
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')

    # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        max_birth = df['Birth Year'].max()
        min_birth = df['Birth Year'].min()
        com_birth = df['Birth Year'].mode()[0]
        print("The oldest user is born in {} ,and the youngest user is born in {} while the most common year of birth is {}".format(int(min_birth),int(max_birth),int(com_birth)))
    else:
        print('Birth stats cannot be calculated because Birth Year does not appear in the dataframe')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        view_choice = input("Do you want to view the data? y/n \n")
        view_numb = 5
        while(view_choice == 'y'):
            print(df.iloc[:view_numb])
            view_numb += 5
            view_choice = input("Do you want to continue? y/n \n")
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
