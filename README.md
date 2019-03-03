# emailsettings

# Task:
Read the txt file which containts following pattern of emails list: Login@Domain:Password (for example: rickoshet.averin@gmail.com:qwerty).
Parse 'Domain' value to the website emailsettings.email then extract values from the grid and save them to the set.txt file.

# Solution:
With closure inspection I noticed that after we press the 'Find' button on the website, system link user to the webpage with following pattern:
https://www.emailsettings.email/search/pop3-imap-smtp-{searchboxvalue}-email-settings. So I dont need to actually parse data to the website but use this pattern for my advantage instead. So I created this alghoritm:
  1. Load data from txt file
  2. Filter only unique values of domains
  3. Create url emailsettings.email/search/pop3-imap-smtp- + domain + -email-settings for each one of unique domans.
  4. Use those urls as url list for scrapy Spider and extract data from a webpage
  5. Save excracted data to set.txt file.

# What I've learned:
  * Using Pandas to filter ordered data
  * Creating new strings using variables
  * Correct way of using scrapy 
# After project I realised that I need to learn:
  * To use classes instead of separate functions and variables.
  * Combining different methods with same purpose in one class
  * To trying not use additional frameworks if it will be used only few times in a script
