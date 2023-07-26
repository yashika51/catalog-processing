# Catalog Processing

This project processes a catalog with shoes. There are two different files : pricat.csv and mappings.csv present in `raw_files`
that I use to process and map data.

The goal is to transform `pricat.csv` in a better format and for this repo I chose JSON.


The results can be tested by using the API by making a request on endpoint `http://localhost:8000/catalog`. Prior to that, you need
to run the sever with `uvicorn main:app --reload` command.

In case of testing additional `combine_fields`, it can be passed as string to the endpoint request
for example like `http://localhost:8000/catalog?combine_fields=price_buy_net,currency`


There are some basic test cases to test the overall functionality and can be run using `pytest test.py`

There is also `catalog.json` present which contains the output result data in JSON format.