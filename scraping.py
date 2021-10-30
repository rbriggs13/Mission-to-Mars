#import splinter and Beautiful soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)

    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'hemispheres': hemisphere_images(browser),
        'last_modified': dt.datetime.now()
    
    }

    browser.quit()
    return data

def mars_news(browser):
    #Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    #Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:
        slide_elem = news_soup.select_one('div.list_text')

        slide_elem.find('div', class_='content_title')

        #Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
    
        #find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):

    # visit url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    #find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    #parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')


    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    

    return img_url


def mars_facts():
    
    try:
 
        df = pd.read_html('http://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    return df.to_html()

def hemisphere_images(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    hemisphere_image_urls = []

    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    hemisphere_soup = hemi_soup.find_all('div', {'class' : 'item'})

    for items in hemisphere_soup:
        hemisphere = {}
    
        img_url = items.find('a').get('href')
        front_url = 'https://marshemispheres.com/'
        full_url = front_url+img_url

    
        browser.visit(full_url)
        img_soup = soup(browser.html,'html.parser')
        image_soup = img_soup.find('div', class_='downloads')
        pic_url = image_soup.find('a').get('href')
        picture_url = front_url+pic_url
        hemisphere['img_url'] = picture_url
    
        browser.back()
    
        title = items.find('h3').text
        hemisphere['title'] = title
        hemisphere_image_urls.append(hemisphere)

    return hemisphere_image_urls

if __name__ == '__main__':
    print(scrape_all())