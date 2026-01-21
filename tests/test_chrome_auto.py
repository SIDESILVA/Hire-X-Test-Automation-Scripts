from selenium import webdriver
import time

# This will automatically download and use ChromeDriver
driver = webdriver.Chrome()

# Open a website
driver.get("https://www.google.com")

# Wait 5 seconds so you can see it
time.sleep(5)

# Close the browser
driver.quit()
