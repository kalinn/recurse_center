# Practice working with pandas while reading "Python for Data Analysis"

import pandas as pd

years = range(1880, 2015)

pieces = []
columns = ['names', 'sex', 'births']

for year in years:
    path = '~/Desktop/pydata-book-master/ch02/names/yob%d.txt' % year
    frame = pd.read_csv(path, names=columns)
    frame['year'] = year
    pieces.append(frame)

names = pd.concat(pieces, ignore_index=True)

# Separate by sex
names_f = names[names['sex']=='F']
names_m = names[names['sex']=='M']

# I want to see how many new names are created each year by sex
# Use the first year as baseline
baseline_names_f = list(pd.DataFrame(names_f[names_f['year']==1880],
    columns=['names', 'sex', 'births', 'year'])['names'])
baseline_names_m = list(pd.DataFrame(names_m[names_m['year']==1880],
    columns=['names', 'sex', 'births', 'year'])['names'])

# new_names will store the year and all unique new names that have not been given in previous years
new_names_m = dict()
new_names_f = dict()
concat_names_m = baseline_names_m
concat_names_f = baseline_names_f

for year in years[1:]:
    # Get all boy names in year
    year_names_m = list(pd.DataFrame(names_m[names_m['year']==year],
    columns=['names', 'sex', 'births', 'year'])['names'])
    # Get all girl names in year
    year_names_f = list(pd.DataFrame(names_f[names_f['year']==year],
    columns=['names', 'sex', 'births', 'year'])['names'])
    # Which ones are new?
    new_names_m['%d' % year] = list(set(year_names_m) - set(concat_names_m))
    new_names_f['%d' % year] = list(set(year_names_f) - set(concat_names_f))
    # Add the new ones to the running total list of names
    concat_names_m = concat_names_m + new_names_m.get('%d' % year)
    concat_names_f = concat_names_f + new_names_f.get('%d' % year)

# Counts new names in each year by sex
counts_m = {}
counts_f = {}
for k, v in new_names_m.items():
    counts_m[k] = len(v)

for k, v in new_names_f.items():
    counts_f[k] = len(v)

# Need to index by year for the plot
years_m = [int(x) for x in counts_m.keys()]
data_m = pd.DataFrame(index=years_m)
data_m['New'] = counts_m.values()
years_f = [int(x) for x in counts_f.keys()]
data_f = pd.DataFrame(index=years_f)
data_f['New'] = counts_f.values()
# The list comprehension doesn't return sorted list!
sorted_data_m = data_m.sort_index()
sorted_data_m.plot(title='Number of New Baby Names: Male')
sorted_data_f = data_f.sort_index()
sorted_data_f.plot(title='Number of New Baby Names: Female')





