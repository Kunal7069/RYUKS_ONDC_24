# RYUKS_ONDC_24
This project can analyse the products and catalogue of different shopping sites and can analyse whether the information given about the product is valid or not.

The show stoppers of this project are:-

1. Web Scrapper: This helps us to compare images of products with similar category images on the web.  
                Also, it gives our website the flexibility to evaluate catalogues of already listed products and websites. It automatically scrawl the web page and extract the required information and can be use for further analysis. It can work on any web page. The tech stack used in it are web driver, beautifulsoup, bs4.

2. Machine Learning – For product evaluation we use Homography. This eliminates the need of training and 
                     does not require any heavy resources.It doesnot require training data and it can work on low resource computer.Despite no training and low computation, homography has a high accuracy.

3. Elasticsearch Database - We have used elastic search as a database as indexing and searching is far  
                            better than any other database.

Criteria For Rating the products:

1. Our scrapper will check whether all essential and required attribites are present in product detail or not.
2. For different category of products, different attributes are used, For Ex- In medicine category expiry date is required and in clothes category size is required.
3. Photo given on the catalogue will be compared with other photos which we will get from the product name and photo will be rated out of 5 as per the correctness.
4. Total grading will be done out of 15 where 5 points are for photo especially and other 10 points for all other attributes.

LINK FOR DEMO SHOPPING WEB PAGE WE USED FOR WEB SCRAPPING : https://kunal7069.github.io/shopping_webpage/

LINK FOR LIVE DEMO : https://testryuks1.el.r.appspot.com/

LOGIN CREDENTIALS FOR ACCESSING THE WEBSITE

USERNAME : domo

PASSWORD : demo
