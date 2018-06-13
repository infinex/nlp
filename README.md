
# NLP Guide

1. [Introduction](#introduction)
2. [Preprocessing](#preprcoessing)
3. [Text Statistics](#statistics)
4. [Text Comparsion](#comparsion)
10. [Conda Guide](#conda)


## 1. Introduction

This is a series of file collection to assist in nlp preprocssing

## 2. Preprocessing

[ngram.py](ngram.py) : Function to compute n-gram & n-term


## 3. Text Statistics


## 4. Text Comaprsion

## 10. Conda helpful Guide <a name="conda"/>

[Conda Cheat sheet](https://conda.io/docs/_downloads/conda-cheatsheet.pdf)

Export conda enviroment to yml file

```
conda env export > <environment-name>.yml
```

Export python requrement.txt environment
```
conda list -e > requirements.txt
```


Create a new conda enviroment
```
conda env create -f <environment-name>.yml
```

Update an existing enviroment
```
conda env update -f <environment-name>.yml
```



