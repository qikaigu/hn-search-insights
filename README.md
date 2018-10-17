# Finding Trending Searches

A trending search detector for [HN Search](https://hn.algolia.com/).

## Getting started

Begin by using `pip` to install [Pipenv](http://docs.pipenv.org/) and its dependencies

```pip install pipenv```

Install required libraries

```pipenv install```

To test

```python -m unittest discover```


**`build` mode**

1. Download the provided data and put it in the `input` folder
2. Run the Python program with build mode `$ python main.py -mode build`, a model will be built based on 28-day-window data and a list of trending searches on the latest day (2018-07-14) will be displayed.

**`detect` mode**

1. Run the Python program with detect mode by providing a query and an observation `$ python main.py -mode detect -query bitcoin -obs 100`. It determines if the observation is considered as a trending search.


## Approaching The Question

In this section, I will explain how I approached the question.

### How to define trending searches?

The provided dataset contains on month of aggregated searches coming from [HN Search](https://hn.algolia.com/). The most frequent search query was searched hundreds of times per day. For this particular case, I defined that a trending search has the following characteristics:
- The frequency of the query is above 300 times per month
- Assume that the daily search count follows a normal distribution, the search count on the target day should be a high value which is not likely to happen based on its historical data.

### Main steps

* Query cleaning

   Remove special characters, turn all characters to minuscule and strip white spaces.

* Query aggregation and filter low frequent queries

   Filter queries having less than 300 searches, then aggregate by date to find daily search counts.

* Find mean and standard deviation of daily search counts for each query

   Fill with zeros if there are missing dates in the date range, then compute mean and standard deviation for each query. in most cases, recent activities have more impact than previous activities. So a decay is added while doing this computation. 

* Based on mean and standard deviation, determine if a search is trending by providing the search count on the target day

   Calculate the z-score of the given search count with the pre-computed mean and standard deviation. It is a trending search if the z-score is above 2.0 (configurable threshold).


## Some Visual Check

Let's do some visual check.

For the query `bitcoin`, it was searched about 50 times on the latest day (2018-07-14). Based on the trend detector, it wasn't a trending search.
```
Query: [bitcoin](0.429985) is not a trending search for the given observation.
```

From the graph below, it doesn't seem to be a trending search either.

![not a trending search][bitcoin-1]

However, if the query `bitcoin` was searched 100 times instead of 50, then it should be a trending search.

```
Query: [bitcoin](3.381475) is a trending search for the given observation.
```

![a trending search][bitcoin-2]

[bitcoin-1]: img/bitcoin-1.png

[bitcoin-2]: img/bitcoin-2.png


## Conclusion

This repo gives a simple solution for finding trending searches. It is based on the distribution of daily search counts.
