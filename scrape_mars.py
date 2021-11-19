#Import Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

   

# Full Scrape function.
def scrape():

    # Run browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)




    # Visit news url.
    news_url = "https://redplanetscience.com"
    browser.visit(news_url)

    # HTML Object.
    html = browser.html

    # Parse HTML with Beautiful Soup
    news_soup = BeautifulSoup(html, "html.parser")

    # Retrieve the most recent article's title and paragraph.
    # Store in news variables.
    news_title = news_soup.find("div", class_="content_title").get_text()
    news_paragraph = news_soup.find("div", class_="article_teaser_body").get_text()

    # Exit Browser.
    browser.quit()


    print(f'Title: {news_title}\nText: {news_paragraph}')


    # Run browser
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the url for  Image.
    jpl_url = "https://spaceimages-mars.com"
    browser.visit(jpl_url)

    # Select "FULL IMAGE".
    browser.click_link_by_partial_text("FULL IMAGE")


    # HTML Object.
    html = browser.html

    # Parse HTML with Beautiful Soup
    image_soup = BeautifulSoup(html, "html.parser")

    # Scrape image URL.
    image_url = "/image/featured/mars3.jpg"

    # Concatentate https://www.jpl.nasa.gov with image_url.
    featured_image_url = f'https://spaceimages-mars.com{image_url}'

    # Exit Browser.
    browser.quit()

    print(featured_image_url)






    # URL for Mars Facts.
    facts_url = "https://galaxyfacts-mars.com/"

    # Use Panda's `read_html` to parse the URL.
    facts_tables = pd.read_html(facts_url)

    # Required table stored in index "1".
    # Save as DF.
    df_mars_facts = facts_tables[1]

    # Rename columns.
    df_mars_facts.columns = ['Description', 'Value']

    # Set index to 'Description'.
    df_mars_facts.set_index('Description', inplace=True)

    # df_mars_facts

    # Convert DF to html and save in Resources Folder.
    df_mars_facts.to_html('mars_facts.html')

    # Convert DF to HTML string.
    mars_facts = df_mars_facts.to_html(header=True, index=True)
    print(mars_facts)




    # Run init_browser/driver.
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the url 
    astrogeo_url = "https://marshemispheres.com/"
    browser.visit(astrogeo_url)

    # HTML Object.
    html = browser.html

    # Parse HTML with Beautiful Soup
    astrogeo_soup = BeautifulSoup(html, "html.parser")

    # Store main URL in a variable so that 'href' can be appended to it after each iteration.
    main_astrogeo_url = "https://marshemispheres.com/"

    # Each link is located in 'div' tag, class "item".
    # Locate all 4 and store in variable.
    hems_url = astrogeo_soup.find_all("div", class_="item")

    # Create empty list for each Hemisphere URL.
    hemis_url = []

    for hem in hems_url:
        hem_url = hem.find('a')['href']
        hemis_url.append(hem_url)

    browser.quit()

    print(hemis_url)

    # Create list of dictionaries called hemisphere_image_urls.
    # Iterate through all URLs saved in hemis_url.
    # Concatenate each with the main_astrogeo_url.
    # Confirm the concat worked properly: confirmed.
    # Visit each URL.

    hemisphere_image_urls = []
    for hemi in hemis_url:
        hem_astrogeo_url = main_astrogeo_url + hemi
        print(hem_astrogeo_url)
        
        # Run init_browser/driver.
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(hem_astrogeo_url)
        
        # HTML Object.
        html = browser.html

        # Parse HTML with Beautiful Soup
        hemi_soup = BeautifulSoup(html, "html.parser")

        # Locate each title and save to raw_title, to be cleaned.
        raw_title = hemi_soup.find("h2", class_="title").text
        
        # Remove ' Enhanced' tag text from each "title" via split on ' Enhanced'.
        title = raw_title.split(' Enhanced')[0]
        
        # Locate each 'full.jpg' for all 4 Hemisphere URLs.
        img_url = hemi_soup.find("li").a['href']

        imgs_url = main_astrogeo_url + img_url
        
        # Append both title and img_url to 'hemisphere_image_url'.
        hemisphere_image_urls.append({'title': title, 'img_url': imgs_url})
        
        browser.quit()

        print(hemisphere_image_urls)


    mars_data = {}

    # Append news_title and news_paragraph to mars_data.
    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_paragraph
    # Append featured_image_url to mars_data.
    mars_data['featured_image_url'] = featured_image_url
    # Append mars_facts to mars_data.
    mars_data['mars_facts'] = mars_facts
    # Append hemisphere_image_urls to mars_data.
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_data






