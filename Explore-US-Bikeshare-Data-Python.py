import time
import pandas as pd
import numpy as np

    #loading csv files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
def city_input():
    '''
    This function starts the user interface by introduction and
    asking the user with the desired city to analyze
    '''
    print('Hey! Let\'s explore some US bikeshare data!')
    print('  ')
    print('Enter the city you want to explore the data for:')
    print('Chicago')
    print('New York')
    print('Washington')
    print('  ')

    city = ''
    while city.lower() not in ['chicago', 'new york', 'washington']:
        city = input('\nWould you like to see data for Chicago, New York, or Washington?\n')
        if city.lower() == 'chicago':
            print("\nChicago City! Oh great\n")
            return 'chicago'
        elif city.lower() == 'new york':
            print("\nNew York City City! Lovely (:\n")
            return 'new york city'
        elif city.lower() == 'washington':
            print("\nWashington City! the great capital in the world\n")
            return 'washington'
        else:
            print('Sorry, I do not understand your input. Please input either '
                  'Chicago, New York or Washington.')

def get_time():
    '''
    the code below asks the user to choose between month and day of month,
    day of the week or no filters
    '''
    period = input('\nDo you want to filter the data by month and day of the month, day of the week, or you do not want to filter at all? Type "no" for no period filter\n')
    period = period.lower()

    while True:
        if period == "month":
            while True:
                day_month = input("\nDo you want to filter the data by day of the month too? Type 'YES' or 'NO'\n").lower()
                if day_month == "no":
                    print('\n The data is now being filtered by month...\n')
                    return 'month'
                elif day_month == "yes":
                   print ('\n The data is now being filtered by month and day of the month...\n')
                   return 'day_of_month'

        if period == "day":
            print('\n The data is now being filtered by the day of the week...\n')
            return 'day_of_week'
        elif period == "no":
            print('\n No period filter is being applied to the data\n')
            return "none"
        period = input("\n Please choose a period filter option between 'month', 'day' of the week, or none (no) \n").lower()
    # get user input for month (all, january, february, ... , june)
def month_info(m):
    if m == 'month':
        month = input('\nChoose month! January, February, March, April, May, or June? Please type the full month name.\n')
        while month.strip().lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('\nPlease choose between January, February, March, April, May, or June? Please type the full month name.\n')
        return month.strip().lower()
    else:
        return 'none'

def month_day_info(df, day_m):     # Asks the user for a month and a day of month,
    month_day = []
    if day_m == "day_of_month":
        month = month_info("month")
        month_day.append(month)
        maximum_day_month = max_day_month(df, month)

        while (True):
            ask = """ \n Which day of the month? \n
            Please type your response as an integer between 1 and """
            ask  = ask + str(maximum_day_month) + "\n"
            day_m = input(ask)

            try:
                day_m = int(day_m)
                if 1 <= day_m <= maximum_day_month:
                    month_day.append(day_m)
                    return month_day
            except ValueError:
                print("That's not a numeric value")
    else:
        return 'none'

    # Asks the user for a day and returns the specified day
def day_info(d):
    if d == 'day_of_week':
        day = input('\nWhich day? Please type a day M, Tu, W, Th, F, Sa, Su. \n')
        while day.lower().strip() not in ['m', 'tu', 'w', 'th', 'f', 'sa', 'su']:
            day = input('\nPlease type a day as a choice from M, Tu, W, Th, F, Sa, Su. \n')
        return day.lower().strip()
    else:
        return 'none'



def load_data(city):
    # Loads data for the specified city
    print('\nLoading the data...\n')
    df = pd.read_csv(CITY_DATA[city])

    #extracting from Start Time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    df["day_of_month"] = df["Start Time"].dt.day
    return df


def time_filters(df, time, month, week_day, md):
    '''
    Filters the data according to the criteria specified by the user.
    Local Variables:
    df         - city dataframe
    time       - indicates the specified time (either "month", "day_of_month", or "day_of_week")
    month      - indicates the month used to filter the data
    week_day   - indicates the week day used to filter the data
    md         - list that indicates the month (at index [0]) used to filter the data
                    and the day number (at index [1])
    Result:
    df - dataframe to be used for final calculation
    '''
    print('Data loaded. Now computing statistics... \n')
    #Filter by Month
    if time == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #Filter by day of week
    if time == 'day_of_week':
        days = ['Monday', 'Tuesday',
        'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday']
        for d in days:
            if week_day.capitalize() in d:
                day_of_week = d
        df = df[df['day_of_week'] == day_of_week]
    #Filter by day of month
    if time == "day_of_month":
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = md[0]
        month = months.index(month) + 1
        df = df[df['month']==month]
        day = md[1]
        df = df[df['day_of_month'] == day]

    return df


def max_day_month(df, month):
    '''Gets the max day of the month '''

    months = {"january": 1, "february": 2, "march": 3, "april":4, "may": 5, "june":6}
    df = df[df["month"] == months[month]]
    max_day = max(df["day_of_month"])
    return max_day



    # TO DO: display the most common month
def month_freq(df):
    '''What is the most popular month for bike traveling?
    '''
    # df - dataframe returned from time_filters
    print('\n* Q1. What is the most popular month for bike traveling?')
    m = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[m - 1].capitalize()
    return popular_month

    # TO DO: display the most common day of week
def day_freq(df):
    '''What is the most popular day of the week for bike rides?
    '''
    # df - dataframe returned from time_filters
    print('\n* Q2. What is the most popular day of the week for bike rides?')
    return df['day_of_week'].value_counts().reset_index()['index'][0]

    # TO DO: display the most common start hour
def hour_freq(df):
    '''What is the most popular hour of the day for bike rides?
    '''
    # df - dataframe returned from time_filters
    print('\n* Q3. What is the most popular hour of the day for bike rides?')
    df['hour'] = df['Start Time'].dt.hour
    return df.hour.mode()[0]


    # TO DO: display most commonly used start station
def start_stations_freq(df):
    '''What is the most popular start station?
    '''
    # df - dataframe returned from time_filters
    print("\n* Q4. What is the most popular start station?\n")
    start_station = df['Start Station'].value_counts().reset_index()['index'][0]
    return start_station

    # TO DO: display most commonly used end station
def end_stations_freq(df):
    '''What is the most popular end station?
    '''
    # df - dataframe returned from time_filters
    print("\n* Q5. What is the most popular end station?\n")
    end_station = df['End Station'].value_counts().reset_index()['index'][0]
    return end_station

    # TO DO: display most frequent combination of start station and end station trip
def common_trip(df):
    '''What is the most popular trip?
    '''
    # df - dataframe returned from time_filters
    result = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\n* Q6. What was the most popular trip from start to end?')
    return result


def total_ride_duration(df):
    '''
    What is the total ride duration and average ride duration?

    '''

    # TO DO: display total travel time
    '''
    What is the total ride duration?

    '''
    # df - dataframe returned from time_filters
    print('\n* Q7. What was the total travel time?')
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    #sum for total trip time, mean for avg trip time
    total_ride_time = np.sum(df['Travel Time'])
    total_days = str(total_ride_time).split()[0]

    print ("\nThe total travel time on: " + total_days + " days \n")
    return total_ride_time

def average_ride_duration(df):
    '''
    What is the average travel time?

    '''
    # TO DO: display mean travel time

     # df - dataframe returned from time_filters
    print('\n* Q8. What was the average travel time?')
    avg_ride_time = np.mean(df['Travel Time'])
    avg_days = str(avg_ride_time).split()[0]
    print("The average travel time on: " + avg_days + " days \n")

    return avg_ride_time



    # TO DO: Display counts of user types
def bike_users(df):
    print('\n* Q9. Types of users:\n')
    return df['User Type'].value_counts()

    # TO DO: Display counts of gender
def gender_data(df):
    try:
        print('\n* Q10. What is the common gender among the user?\n')
        return df['Gender'].value_counts()

    except KeyError:
      print("\nGender Types:\nNo data available for this month.")

    # TO DO: Display earliest, most recent, and most common year of birth
def birth_years(df):
    try:
        print('\n* Q11. What is the earlist, latest and most common year of birth?')
        earliest = np.min(df['Birth Year'])
        print ("\nThe earliest year of birth is " + str(earliest) + "\n")
        latest = np.max(df['Birth Year'])
        print ("The latest year of birth is " + str(latest) + "\n")
        most_common= df['Birth Year'].mode()[0]
        print ("The most common year of birth is " + str(most_common) + "\n")
        return earliest, latest, most_common
    except:
        print('No available birth date data for this period.')


def process(f, df):
    '''Calculates the time it takes to commpute a statistic
    '''
    start_time = time.time()
    statToCompute = f(df)
    print(statToCompute)
    print("Computing this stat took %s seconds." % (time.time() - start_time))

def disp_raw_data(df):
    '''
    Displays the data used to compute the stats
    Input:
        the df with all the bikeshare data
    Returns:
       none
    '''
    #omit irrelevant columns from visualization
    df = df.drop(['month', 'day_of_month'], axis = 1)
    row_index = 0

    see_data = input("\nDo you like to see rows of the data used to compute the stats? Please write 'yes' or 'no' \n").lower()
    while True:
        if see_data == 'no':
            return
        if see_data == 'yes':
            print(df[row_index: row_index + 5])
            row_index = row_index + 5
        see_data = input("\nDo you like to see five more rows of the data used to compute the stats? Please write 'yes' or 'no' \n").lower()


def main():
    '''The main function calculates and prints out the
    descriptive statistics about a desired city
    '''
    # calling all the functions step by step
    city = city_input()
    df = load_data(city)
    period = get_time()
    month = month_info(period)
    day = day_info(period)
    month_day = month_day_info(df, period)

    df = time_filters(df, period, month, day, month_day)
    disp_raw_data(df)

    # all the conclusions
    stats_funcs_list = [month_freq, day_freq, hour_freq,
     start_stations_freq, end_stations_freq, common_trip,
     total_ride_duration, average_ride_duration,
     bike_users, gender_data, birth_years]

    for x in stats_funcs_list:	# displays processing time for each function block
        process(x, df)

     # Restarting option
    restart = input("\n *Would you like to do it again and perform another analysis? Type \'yes\' or \'no\'.\n")
    if restart.upper() == 'YES' or restart.upper() == "Y":
        main()


if __name__ == "__main__":
	main()
