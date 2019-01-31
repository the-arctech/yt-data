#!/usr/bin/python3
# Basic scraping template for YouTube that 
# does not require using the API or OAuth.

from bs4 import BeautifulSoup
import requests
import collections # Used in common word parsing

titles = []
watch_links = []
view_count = []
likes = []
dislikes = []

# Get search terms from user
search_terms = input("Enter search terms (eg. 'current+events')\n> ")
search_filter = input("Search by 'recent' or 'views'?  (leave blank for standard search)\n> ")
    
# Get search data from youtube
if str(search_filter) == 'recent':
    r = requests.get(
        "https://www.youtube.com/results?sp=CAISAhAB&search_query=" 
        + str(search_terms))
    data = r.text
elif str(search_filter) == 'views':
    r = requests.get(
        "https://www.youtube.com/results?sp=CAMSAhAB&search_query=" 
        + str(search_terms))
    data = r.text
else:
    r = requests.get(
        "https://www.youtube.com/results?search_query=" 
        + str(search_terms))
    data = r.text

# Soupify the data
soup = BeautifulSoup(data, 'html.parser')


# Parse every video in the page (by title)
for vid in soup.find_all(attrs={"aria-describedby": True}):
    # Add the 20 titles to list
    titles.append(vid.get('title'))
    watch_links.append(vid.get('href'))

# Getting common words in TITLES
words = []
for title in titles:
    words.extend(title.strip().split(' '))
counter = collections.Counter(words).most_common()
common_title_words = counter[0:10]

# Pull information from individual videos
for href in watch_links:
    r = requests.get("https://www.youtube.com"+href)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    view_count.append(
        soup.find('div', class_='watch-view-count').text.strip(' views'))
    likes.append(
        soup.find(attrs={"title": "I like this"}).find('span', class_="yt-uix-button-content").text)
    dislikes.append(
        soup.find(attrs={"title": "I dislike this"}).find('span', class_="yt-uix-button-content").text)


###### DISPLAYING GATHERED INFORMATION ######

# Printing common Words
print("\n"+("*"*70)+"\n")
print("Most commonly used words in titles: ")
for i in common_title_words:
    print(str(i[0]) + " ("+str(i[1])+")")
print("\nMost commonly used words in descriptions: ")

# Printing averages
print("\n"+("*"*70)+"\n")
#print("Combined number of views: " + total_views)
print("Average like/dislike ratio: ")

# Printing list of scraped videos	
print("\n"+("*"*70)+"\n")
for i in range(0,16):
    print('"'+titles[i]+'"')
    print("https://www.youtube.com"+watch_links[i]+"")
    print('Like/Dislike: ' + str(likes[i]) + ' / ' + str(dislikes[i]))
    print("Number of views: "+view_count[i]+"\n")
