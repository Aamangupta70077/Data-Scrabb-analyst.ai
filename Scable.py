import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_listings(pages_to_scrape):
    base_url = "https://www.amazon.in/s"
    params = {
        "k": "bags",
        "crid": "2M096C61O4MLT",
        "qid": "1653308124",
        "sprefix": "ba%2Caps%2C283",
        "ref": "sr_pg_"
    }

    all_products = []
    
    for page in range(1, pages_to_scrape + 1):
        params["ref"] = f"sr_pg_{page}"
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("div", {"data-asin": True})

        for product in products:
            product_url = "https://www.amazon.in" + product.find("a", class_="a-link-normal")["href"]
            product_name = product.find("span", class_="a-size-medium").text.strip()
            product_price = product.find("span", class_="a-offscreen").text.strip()
            rating = product.find("span", class_="a-icon-alt")
            rating = rating.text.split()[0] if rating else "Not available"
            num_reviews = product.find("span", {"aria-label": True})
            num_reviews = num_reviews.text.split()[0] if num_reviews else "0"
            
            product_info = {
                "Product URL": product_url,
                "Product Name": product_name,
                "Product Price": product_price,
                "Rating": rating,
                "Number of Reviews": num_reviews
            }
            all_products.append(product_info)
    
    return all_products

# Example usage:
products_data = scrape_product_listings(pages_to_scrape=20)

# Now you can proceed with Part 2 to scrape additional information and then export the data to a CSV file.
