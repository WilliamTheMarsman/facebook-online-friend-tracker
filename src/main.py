# The Facebook Online Friend Tracker
# Author: Baraa Hamodi

import csv
import getpass
import os
import time

from datetime import datetime
from selenium import webdriver

# Enable tab completion for raw input.
try:
  import readline
  readline.parse_and_bind('tab: complete')
except ImportError:
  pass

# Support both Python 2.x and 3.x user input functions.
try:
  input = raw_input
except NameError:
  pass

def main():
  # Prompt user for Facebook credentials.
  print('\nFacebook Online Friend Tracker starting...')
  facebook_username = 'username'
  facebook_password = 'password-or-getpass'

  # Prompt user for script interval time and convert to seconds.
  interval_time = 3;
  interval_time = interval_time * 60

  # Prompt user for total run time and convert to seconds.
  total_time = 720000
  total_time = total_time * 3600

  # Prompt for the CSV file path and verify that the CSV file exists before scraping.
  path_to_csv_file = 'facebook-friends-online-tracker.csv'
  print('Verifying that the CSV file exists...')
  if os.path.exists(path_to_csv_file):
    print(path_to_csv_file + ' has been found.')
  else:
    print('[WARNING] ' + path_to_csv_file + ' does not exist. Creating a new CSV file now...')
    with open(path_to_csv_file, 'w') as f:
      writer = csv.writer(f, lineterminator='\n')
      writer.writerow(['Timestamp', 'Number of Online Friends'])
      print('New CSV file created at: ' + path_to_csv_file)

  # Compute total number of iterations and initialize iteration counter.
  number_of_iterations = total_time / interval_time
  iteration = 0

  # Initialize Chrome WebDriver.
  print('\nInitializing Chrome WebDriver...')
  chrome_options = webdriver.ChromeOptions();
  chrome_options.add_argument('--headless');
  driver = webdriver.Chrome(chrome_options=chrome_options)

  # Change default timeout and window size.
  driver.implicitly_wait(120)
  driver.set_window_size(1300, 8000)

  # Go to www.facebook.com and log in using the provided credentials.
  print('Logging into Facebook...')
  driver.get('https://www.facebook.com/')
  emailBox = driver.find_element_by_id('email')
  emailBox.send_keys(facebook_username)
  passwordBox = driver.find_element_by_id('pass')
  passwordBox.send_keys(facebook_password)
  driver.find_element_by_id('loginbutton').click()

  print('Logged in successfully!')

  while iteration < number_of_iterations:
    # Wait for Facebook to update the number of online friends.
    print('\nFinding currently online facebook friends...')

    # Scrape the number of online friends.

    friends_active_now = driver.find_elements_by_xpath('//div[div[div[span[@aria-label="Active Now"]]]]/div[3]')
    today = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    friends_timestamps = [[str(iteration), today, 'friends_found_' + str(friends_active_now.__len__())]]
    if friends_active_now.__len__():
      friends_timestamps = friends_timestamps + map(lambda friend: [str(iteration), today, friend.text], friends_active_now)

    f = open(path_to_csv_file, 'a')
    writer = csv.writer(f, lineterminator='\n')
    for frien in friends_timestamps:
      print(frien)
      writer.writerow(frien)
    f.close()

    print('\nAdded all detected friends to the spreadsheet.')

    # Wait for next interval and increment iteration counter.
    print('\nWaiting for Facebook to update friends list... (This takes approximately 3 minutes.)')
    time.sleep(interval_time)
    iteration += 1

  # Close Chrome WebDriver.
  driver.quit()
