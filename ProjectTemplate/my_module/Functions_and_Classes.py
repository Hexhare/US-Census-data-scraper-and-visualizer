"""All my Functions and Classes for my project"""
# In[1]:
import requests
import bs4 as bs
import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


def get_wikitable_source(url, only_first_instance = True):
    """Takes in a wiki page url and outputs the table page source code.
    Only outputs the first instance unless only_first_instance
    is set to false then outputs all instances of tables as a list.
    
    Parameters
    ----------
    url : string
        Website url that will have the page source code returned
        
    only_first_instance : Boolean
        defaults to True, if set to false takes all tables from
        the wiki page.
    
    Returns
    -------
    
    table : wikitable source code"""
    # Gets webpage source code which will soon be spliced
    page_source = requests.get(url).text 
    parsed_source = bs.BeautifulSoup(page_source,'lxml')
    
    # Finds only first instance of HTML "table" tags with the class "wikitable sortable" and returns as a list
    if only_first_instance:
        table = parsed_source.find("table", {"class":"wikitable sortable"} )
    # Finds all instance of HTML "table" tags with the class "wikitable sortable" and returns as a list
    else:
        table = parsed_source.findAll("table", {"class":"wikitable sortable"} )
    return table


# In[3]:


def sort_wikitable_column(wikitable_source, column):
    """Takes in a single wikitable sorce code as a bs4 element list or singular object and stores the column number    inputted.
        
         Parameters
        ----------
        wikitable_source : bs4 element
            Takes in wikitable sorce code as a single bs4 element list 
        
    
        Returns
        -------
    
        table_column : list
            returns the table column as a list"""
    table_column = []    
    
    # looping through the individual rows of the table skipping the header
    for row in wikitable_source.findAll("tr")[1:]: 
       
        # takes solely the text of the column and removes excessive characters like \n
        table_column.append(row.findAll("td")[column].text.strip())

    return table_column


# In[4]:


def US_census_data(current_year):
    """collects US_census_data by scraping every census wikipage from 1790 to before
    current year
    
    Parameters
    ----------
    current_year : int or string
    The year you want to collect census data to
    (Note that census data is taken every 10 years and when inputting a year 
    divisable by 10 such as 2010 then it will stop the year before and only get data from 1790-2000)
    
    Returns
    -------
    city_list : list of CityPopulation objects
    The City Population class stores City, State, as strings 
    and Population:Year as a dictionary. It is an organized way
    to access the census data"""
    
    city_list = []
    
    # Note that the for loop stops before current_year, as the data for that year isn't complete
    # The census is taken every 10 years which is why we have a step size of 10
    for year in range(1790, current_year, 10):
        # adjusting the wikipedia link to get the data from
        url = 'https://en.wikipedia.org/wiki/%s_United_States_Census' % (year) 
        tables = get_wikitable_source(url, only_first_instance = False) 
        
        if year == 1790:
            # on every census wikipage, the last table is the City Rank table
            city = sort_wikitable_column(tables[-1], 1)
            state = sort_wikitable_column(tables[-1], 2)
            
            for pair in zip(city, state):                
                city_list.append(CityPopulation(*pair))
                
        # census 1870 has differing HTML formatting which otherwise breaks the code
        # Must skip this year as the HTML on this page labels the table wrong
        if year != 1870:
            # If I do the sort_wikitable_column before my if statements then it will cause an error
            # due to the function running for 1870 and bugging out
            city = sort_wikitable_column(tables[-1], 1)
            state = sort_wikitable_column(tables[-1], 2)
            population = sort_wikitable_column(tables[-1],3)
            
            for info in zip(city, state, population):
                temp = None
                
                for place in city_list:
                    # if the city is in the city list then adding to the dictionary population:year aspect
                    if place.getcity().lower() == info[0].lower():
                        place.addpopulation({info[2]:year})
                        temp=None
                        break
                        
                        
                    # This else statement is incase the city is not in the city_list then it will be added    
                    else:
                        temp = CityPopulation(*info, year)
                # adding the city that isn't in the city list        
                if temp!=None:  
                    city_list.append(temp)
           
    return city_list


# In[5]:


class CityPopulation():
    """Class that stores the ciy and state and the population/year
    as a key value pair. Easy way to sort the information collected
    from webscraping."""
    # requires taking in a city and state for the initial set up, 
    # and I added the functionality to take in a population and year for flexibility
    def __init__(self, city, state, population = None, year = None):
        self.city = city
        self.state = state
        self.populationdict = {}
        if population!=None and year!=None:
            self.addpopulation({population:year})
    # Overloading the printed representation of object for easier readability        
    def __repr__(self):
        return self.city + '-' + self.state  
    
    # method to add to the population year dictionary
    def addpopulation(self, dictionary):
        self.populationdict.update(dictionary)
    
    # returns the city
    def getcity(self):
        return self.city
    
    # returns the population dictionary
    def getpop(self):
        return self.populationdict
    
    # returns the state
    def getstate(self):
        return self.state
    
    # returns all of the information as a list
    def getinfo(self):
        return [self.city, self.state, self.populationdict]


# In[6]:


def create_dataframe(data_list, city):
    """returns dataframe of a city
    by taking in data as a list and combing
    through the data to find the specific city
    that you want data for
    
    Parameter
    ---------
    data_list : list of CityPopulation Objects
    The easies way to generate this is by inputting
    the output of US_census_data() 
    
    Returns
    -------
    df: pandas dataframe
    is a pandas dataframe with 
    the Population and Year as the two columns
    """
    dflist = []
    year_population = None
    
    for info in data_list:
        if city.lower() == info.getcity().lower():
            citys = (info.getinfo()[0])
            states = (info.getinfo()[1])
            year_population = (info.getinfo()[2])
    # If the city is not in the data list which is checkable by the dictionary
    # population:year being empty
    if year_population == None:
        return 'This city is not on the list'
    
    population_keys = year_population.keys()
    years = []
    converted_keys = []
    
    for date in population_keys:
        # converting it first to a str to use replace method to remove commas 
        # then a float into an int so the data will be graphable
        years.append(int(float(str(year_population[date]).replace(',','')))) 
        converted_keys.append(int(float(str(date).replace(',',''))))
        
    df = pd.DataFrame(list(zip(years, converted_keys)), columns = ["Year", city+"'s Population Size"])
    return df


# In[7]:


def create_graph(dataframe, city):
    """Create a graph for a single city by taking
    the city's dataframe and city name
    
    Parameters
    ----------
    dataframe: pandas dataframe
    the first column is the x axis and 
    the second is the y axis
    
    city: string
    the city name used for labels
    and the title of the graph"""
    # Setting the figure size to larger so graph is readable
    plt.figure(figsize = (30, 10))
    plt.plot(dataframe.iloc[:,0], dataframe.iloc[:,1], label = city)
    
    # Setting the title and labels and location of the legend
    plt.title("Population Size of " + city)
    plt.xlabel("Population Size")
    plt.ylabel("Year")
    plt.legend(loc="best")

# In[8]:

def create_graphs(cities, font_size_legend = "xx-large"):
    """takes in a list of cities to create a graph
    using U.S. Census Data from the US_census_data function
    
    Parameters
    ----------
    cities: list of City names(Strings)
    
    font_size_legend: Sets the font size of
    the legend, defaults to extra large
    to make it more readable"""
    # setting the figure size to larger
    plt.figure(figsize = (30, 10))
    # Initializes the variable before the loop to reduce run time
    census_data = US_census_data(2020)
    # looping through each city in the city list and checks if the city is in the data
    for city in cities:
        
        dataframe = create_dataframe(census_data, city)
        
        # checks if creating the dataframe works, in the create_dataframe function-
        # if the city is not in the list it returns 'This city is not on the list' and will be a string
        if type(create_dataframe(census_data, city)) == str:
            # only runs if create_dataframe outputs This city is not on the list' 
            print(dataframe)
            # breaks out of the loop to avoid errors in trying to plot a string
            break

        plt.plot(dataframe.iloc[:,0], dataframe.iloc[:,1], label = city)

    # Setting the title and labels and location of the legend
    plt.title("Population Size of Several Cities")
    plt.ylabel("Population Size")
    plt.xlabel("Year")
    plt.legend(loc = "upper left", fontsize = font_size_legend)
    plt.show()
    
# In[9]

def graph_all_census():
    """Graphs every city in the US_censuus_data(2020)
    Does not have any parameters or return.
    """
    city = []
    census_data = US_census_data(2020)
    
    # loops through every city in census_data and adds it to a list
    # then it calls the create_graphs on all the cities
    for place in census_data:
        city.append(place.getinfo()[0])

    create_graphs(city)
    