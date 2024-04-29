# web_scraping_poc
This is a simple proof of the concept for web data scraper to parse all products from https://fr.louisvuitton.com/fra-fr/homepage site.
The results of data scraping can be added to CSV file with the following columns:
1. **name**
2. **sku**
3. **brand**
4. **market**
5. **category**
6. **price**
7. **currency**
8. **material**
9. **color**
10. **url**

### Stack of technologies ###
1. **Python 3.10**
2. **PIP 3**
3. **Python libraries**
   1. *beautifulsoup4*
   2. *requests*
   3. *csv*
   4. *tqdm*

### Setup testing
To get started you might need to create Virtual Env, where you can install all Python dependencies and modules just running the following command:

    pip3 install -r requirements.txt

### Configure testing
There are a lot of unstructured data about the products on Louis Vuitton site. Many products exist in different categories and there are no the exact numbers of available structured categories.
So the decision was made to store the list about product categories that will take part in data scraping. You can find this in [config.py](https://github.com/rigagent/web_scraping_poc/blob/main/config.py) file.
There is pretty huge list of product categories that takes long time for web data scraping (several hours), but you can comment out the unneeded categories and to leave just that you need

### Run testing
If you want to start web scraping, just run this command:

    python3 start_web_scraping.py

After that you can track the process using progress bar:
![](https://github.com/rigagent/web_scraping_poc/blob/main/screenshots/progress_bar_screenshot.jpg)

Also, you may monitor the progress in the **scraping.log** file in the project root directory:
![](https://github.com/rigagent/web_scraping_poc/blob/main/screenshots/scraping_log_screenshot.jpg)

### Get scraping results
At the end after web data scraping process completed, you will be able to find **products.csv** file with results in the project root directory:
![](https://github.com/rigagent/web_scraping_poc/blob/main/screenshots/scraping_results_screenshot.jpg)
