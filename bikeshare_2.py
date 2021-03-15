import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new_york_city': 'new_york_city.csv',
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please select one of the following cites (chicago, new_york_city, washington): ').lower()
    while city not in ['chicago', 'new_york_city', 'washington']:
        city = input('Please re-enter one of (chicago, new_york_city, washington): ').lower()
        
        
    # get user input for month (all, january, february, ... , june)
    month = input('Please enter month that you need to filter by (all, january, february, ... , june): ').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']:
        month = input('Please re-enter correct month: ').lower()
        
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please enter day that you need to filter by (all, monday, tuesday, ... sunday): ').lower()
    while day not in ['all', 'saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
        day = input('Please re-enter correct day: ').lower()

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()  #.weekday_name
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = pd.value_counts(df['month']).idxmax() 

    # display the most common day of week
    most_common_day = pd.value_counts(df['day_of_week']).idxmax() 

    # display the most common start hour
    most_common_hour = pd.value_counts(df['hour']).idxmax()
    
    print('The most common moth {}, day {} and hour {} '. format(most_common_month, most_common_day, most_common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = pd.value_counts(df['Start Station']).idxmax() 

    # display most commonly used end station
    most_common_end_station = pd.value_counts(df['End Station']).idxmax() 

    # display most frequent combination of start station and end station trip
    most_common_start_end = df[['Start Station', 'End Station']].mode().loc[0]
    
    print('The most common start, end and both start-end stations are {}, {} and {}, respectively'. format(most_common_start_station, most_common_end_station, most_common_start_end))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print('Total and mean travelling time are {} and {}'. format(total_travel_time, mean_travel_time))    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_user_types = df['User Type'].value_counts()
    for idx, num in counts_user_types.items():
        print('{} = {}'. format(idx, num) )

    # Display counts of gender
    if city != 'washington'.lower():
        counts_gender = df['Gender'].value_counts()
        for idx, num in counts_gender.items():
            print('{} = {}'. format(idx, num) )

    # Display earliest, most recent, and most common year of birth
    if city != 'washington'.lower():
        early_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].value_counts().idxmax()
        print('The earliest, most recent, and most common year of birth are {}, {}, and {} respectively'. format(early_birth, recent_birth, common_birth_year))

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def data_disp(df):
    """
    ask the user whether he wants to see 5 rows of data

    Returns: chunk of dataframe
    -------
    """
    view_data = input('\nWould you like to first 5 rows of trip data? Enter yes or no\n').lower()
    start_loc = 0
    view_display = view_data
    while view_display == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_display = input("Do you wish to continue?: ").lower()





def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        
        data_disp(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
