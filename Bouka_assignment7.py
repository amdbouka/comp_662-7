### Assignment 7 - Database Analysis
### Ahmad Bouka


import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import logging
import os


#Configures the logging level and format for debugging
def debug_config():
    logging.basicConfig(level=logging.DEBUG,
    format = "[Artists]:%(asctime)s:%(levelname)s:%(message)s")  #DEBUG,INFO,ERROR,WARNING,CRITICAL
    logging.getLogger('matplotlib.font_manager').disabled = True


# Checks the existence and size of the database file.
def db_checkfile(dbfile):
    if os.path.exists(dbfile) and os.path.getsize(dbfile) > 0:
        logging.debug("{a} found and not zero size".format(a=dbfile))
    else:
        logging.error("{a} not found or zero size".format(a=dbfile))

#Establishes a connection to the SQLite database.
def db_connect(dbfile):
    con = sqlite3.connect(dbfile)
    logging.debug("DB Connected".format())
    return con

#Prints the entire DataFrame
def print_full(df):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', None)
    print(df)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')

def main():
    dbfile = "beers.db"
    programname = "Database Analysis"

    # Configure logging for debugging
    debug_config()

    # Print program name
    print(programname,"\n")

    # Check database file existence and size
    db_checkfile(dbfile)

    try:
        # Establish database connection
        con = db_connect(dbfile)
        # Read the "reviews" table into a DataFrame
        df = pd.read_sql_query("SELECT * FROM reviews", con)


        print("#Question 1: How many rows are in the table?")
        num_rows = str(len(df))
        print(f"Number of rows: {num_rows}.\n")

        print("#Question 2: Describe the table")
        describe = df.describe()
        print_full(describe)
        print()

        print("#Question 3: How many entries are there for each brewery")
        count_entry = df.groupby(['brewery_name']).size()
        print(count_entry,"\n")

        print("#Question 4: Find all entries are low alcohol.  Alcohol by volume (ABV) less than 1%")
        low_abv = df[df.beer_abv < 1]
        print_full(low_abv)
        print()

        print("#Question 5:How many reviews are there for low ABV beers?")
        count_low_abv = len(low_abv)
        print(f"There are {count_low_abv} review for low ABV beer.\n")

        print("#Question 6:Group the AVB beers by beer and count")
        grouping = low_abv.groupby("beer_name").size()
        print(grouping,"\n")

        print("#Question 7:How consistent are the O'Douls overall scores?")
        odouls = low_abv[low_abv.beer_name == "O'Doul's"]['review_overall']
        print(odouls,"\n")

        print("#Question 8:Plot a histogram of O'Douls overall scores")
        odouls.hist()
        plt.show()
        print()

        print("#Question 9:For O'Douls, what are the mean and standard deviation for the O'Doul's overall scores?")
        print(odouls.mean())
        print(odouls.std(),"\n")

        print("#Question 10:Draw a boxplot of the low_abv data")
        low_abv.boxplot(figsize=(12, 10))
        plt.show()
        print()


    except sqlite3.Error as error:
        logging.error("Error executing query", error)

    finally:
        if con:
            con.close()
            logging.debug("[Info] DB Closed".format())

    print('Done - check completed')
    logging.info("Completed.")



if __name__=="__main__":
    main()