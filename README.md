# Climate Analysis
This project looks at Honolulu, Hawaii temperature observations and precipitation measurements between 2010 and 2017. What follows is a brief comment on different code functions. These comments do not cover everything provided in the notebook and the API. 

#### Structure of Repo
- Resources (sqlite reference)
- images (images of all graphs)
- app.py (api returning json)
- climate_queries.ipynb (main code for query / graphs)

## Climate Queries
The initial setup is straigt-forward. All libraries needed are imported, and `automap_base()` is used to reflect the tables in the sqlite database.

For the initial **Exploratory Climate Analysis**, I found the most recent date in the database and then queried for all data starting one year prior through the most recent date:

    last_date = session.query(measurement_ref.date).order_by(measurement_ref.date.desc()).first()

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    last_12_months = session.query(measurement_ref.date, measurement_ref.prcp).filter(measurement_ref.date >= query_date).all()

This is then shown as a dataframe, which is used to plot a time searies of the data: `precip_df.plot(figsize=(12, 6))`. 

For the summary statistics, I used a simple `.agg` to find the mean, median, variance, standard deviation, and standard error of the mean. This is all concerning only the precipitation data.

## Temperature Analysis II: Daily Normals
There's probably a simpler way to do this, but I used a `while` loop to calculate the dates, then a `for` loop to go through the dates and convert them to a month-day string for the `daily_normals` function. 

    # Use the start and end date to create a range of dates
    dates = []
    trip_days = []

    while start_date <= end_date:
        dates.append(start_date)
        start_date += dt.timedelta(days=1)

    # Remove the year and save a list of %m-%d strings
    for date in dates:
        change = dt.datetime.strftime(date, "%m-%d")
        trip_days.append(change)

I then looped through the `trip_days` and used the `daily_normals` function, then appended those calculations to a dictionary: 

    daily_dict = {}

    for date in trip_days:
        daily_calc = daily_normals(f"{date}")
        d_min = daily_calc[0][0]
        d_avg = daily_calc[0][1]
        d_max = daily_calc[0][2]
        daily_dict[f"{date}"] = [d_min, d_avg, d_max]

This made the dataframe easy to set up, and put the dates as the index. The only update needed was for the column names. Then, using the dataframe, I plotted the findings as an area chart. 