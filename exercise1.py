# Author Jaspreet
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Setting up the Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Running in headless mode (no browser window)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the webpage
url = "https://www.centennialcollege.ca/programs-courses/full-time/artificial-intelligence-online/"
driver.get(url)


time.sleep(5) 


soup = BeautifulSoup(driver.page_source, 'html.parser')

# %%
title = soup.title.string.strip() if soup.title else "Title not found."

# %%
program_highlights_section = soup.find("h3", string="Program Highlights")

if program_highlights_section:
    highlights_list = program_highlights_section.find_next("ul")  
    
    if highlights_list:
        highlights = [li.get_text(strip=True) for li in highlights_list.find_all("li")]
    else:
        highlights = ["Program Highlights list not found."]
else:
    highlights = ["Program Highlights not found."]

# %%
# Find all paragraph <p> tags in the document
all_paragraphs = soup.find_all("p")

# Extract first two meaningful paragraphs (skip empty ones)
program_overview_paragraphs = [p.get_text(strip=True) for p in all_paragraphs if p.get_text(strip=True)]

# Get first two non-empty paragraphs if available
first_paragraph = program_overview_paragraphs[2] if len(program_overview_paragraphs) > 2 else "First paragraph not found."
second_paragraph = program_overview_paragraphs[3] if len(program_overview_paragraphs) > 3 else "Second paragraph not found."

# Close Selenium WebDriver
driver.quit()

# %%
print("\n🔹 *Website Title:*")
print(title)

print("\n🔹 *Program Highlights:*")
for highlight in highlights:
    print("-", highlight)

print("\n🔹 *Program Overview:*")
print("1", first_paragraph)
print("2", second_paragraph)


# %%
txt_filename = "jaspreet_my_future.txt"
with open(txt_filename, "w", encoding="utf-8") as txt_file:
    txt_file.write(f"Title: {title}\n\n")
    txt_file.write("Program Highlights:\n")
    for highlight in highlights:
        txt_file.write(f"- {highlight}\n")
    txt_file.write("\nProgram Overview:\n")
    txt_file.write(f"1. {first_paragraph}\n")
    txt_file.write(f"2. {second_paragraph}\n")

print(f"\n Data successfully saved to {txt_filename}")