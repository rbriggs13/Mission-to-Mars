#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import splinter and Beautiful soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


#Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
#Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


#Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


#find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


# visit url
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


#find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


#parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[13]:


df = pd.read_html('http://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[14]:


df.to_html()


# ### Scrape the hemisphere data

# In[15]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[16]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemi_soup = soup(html, 'html.parser')
hemisphere_soup = hemi_soup.find_all('div', {'class' : 'item'})
hemisphere_soup


# In[17]:


#loop through to grab the titles and image urls
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


# In[18]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[19]:


browser.quit()

