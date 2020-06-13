# In[1]:


from Functions_and_Classes import *

import pytest


# In[2]:


def test_get_wikitable_source():
    """Test function for get_wikitable_source()"""
    url1 = 'https://en.wikipedia.org/wiki/List_of_colleges_and_universities_in_California'
    
    # test if the function is callable
    assert callable(get_wikitable_source(url1)) 
    
    # Checking if function returns the correct table by checking the 4th column first row of the table
    assert str(get_wikitable_source(url1).findAll('td')[3]) == '<td align="center">42,519\n</td>'
    
    url2 = "https://en.wikipedia.org/wiki/Help:Table"
    # Checking if function properly returns the first row which is the one with all the labels
    assert str(get_wikitable_source(url2).find('tr')) == \
    '<tr>\n<th scope="col">Episode\n</th>\n<th scope="col">Date\n</th>\n<th scope="col">Summary\n</th></tr>'

    
    
test_get_wikitable_source()


# In[3]:


def test_sort_wikitable_column():
    """Test function for sort_wikitable_column()"""
    test_table = get_wikitable_source('https://en.wikipedia.org/wiki/List_of_colleges_and_universities_in_California')
    
    #Test if function properly returns a list
    assert type(sort_wikitable_column(test_table, 2)) == list
    
    # Test if function properly returns expected column
    assert sort_wikitable_column(test_table, 1) == ['Berkeley', 'Davis', 'Irvine', 'Los Angeles',
                                                     'Merced', 'Riverside', 'San Diego', 'Santa Barbara', 'Santa Cruz']
        # Test if inputting a nonexistent column properly raises an error when out of range index
    with pytest.raises(IndexError):
        sort_wikitable_column(test_table, 81930)
    
    # Test if pytest properly raises a Attribution error when non bs4 object is inputted/wikipages without tables
    with pytest.raises(AttributeError):
        sort_wikitable_column('Invalidtable', 0)
        
   
    # Testing if this function works with alternative wikipages
    assert sort_wikitable_column(get_wikitable_source('https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average'),
                                 0) == ['3M', 'American Express',
 'Apple Inc.',
 'Boeing',
 'Caterpillar Inc.',
 'Chevron Corporation',
 'Cisco Systems',
 'The Coca-Cola Company',
 'Dow Inc.',
 'ExxonMobil',
 'Goldman Sachs',
 'The Home Depot',
 'IBM',
 'Intel',
 'Johnson & Johnson',
 'JPMorgan Chase',
 "McDonald's",
 'Merck & Co.',
 'Microsoft',
 'Nike',
 'Pfizer',
 'Procter & Gamble',
 'Raytheon Technologies',
 'The Travelers Companies',
 'UnitedHealth Group',
 'Verizon',
 'Visa Inc.',
 'Walmart',
 'Walgreens Boots Alliance',
 'The Walt Disney Company']
  
 
# In[4]:


def test_class_CityPopulation():
    """Test function for class CityPopulation()"""
    test = CityPopulation('San Diego', 'California', '192083', '2090')
    test.addpopulation({'787':'10'})
    
    # test if the intialization and calling of addpopulation method works as intended
    assert test.getpop() == {'192083' : '2090',
                            '787' : '10'}
    
    assert test.getcity() == 'San Diego'
    
    # test if getinfo() properly returns a list and proper values
    assert test.getinfo() == ['San Diego', 'California', {'192083' : '2090',
                            '787' : '10'}]
    
    # test if getinfo() works with objects missing populationdict
    assert CityPopulation('Houston', 'Texas').getinfo()[0] == 'Houston'
    
    # testing with other index of list
    assert CityPopulation('Philadelphia', 'Pennsylvania').getinfo()[1] == 'Pennsylvania'
    
    

