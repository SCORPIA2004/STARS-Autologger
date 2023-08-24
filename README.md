# STARS-Autologger
Python script to automatically sign you into Bilkent STARS and Webmail with a single click. Made using Python and Selenium.
<br><br>
<i>Note: This software only works for Windows devices. Support for other platforms is WIP</i>
<br><br>
<b><i>*** 23/08/2023: New update for chromedriver.exe for Chrome v116.0.5845.96. Download latest version from <a href="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/win64/chromedriver-win64.zip">here</a> and place in dist folder ***</i></b>
## How to use:
1. Click on code button code button
<img src="src/code button.png"><br>
2. Select "Download ZIP" from the drop down menu
3. Extract to the folder of your choice
4. Go to "dist" folder
5. Enter your login details in the "loginDetails.txt" file
6. Click on "STARS Autologger v1.3"
7. A new Chrome window will open that will automatically sign you in to STARS.
8. You can safely close the console window after it logs you into the SRS system
9. (Optional) Click and drag the "STARS Autologger v1.3" shortcut to your taskbar to pin it there

## Known issues:
Chrome keeps updating their chromedriver and it's possible you might get a version conflict (similiar to below). Just follow the steps below to fix it:
<br><br>
<p align="center"><img src="src/chromeDriver error.png"></p>
<br>

1. Download the latest version from <a href="https://chromedriver.chromium.org/downloads">here</a>
2. Extract "chromedriver.exe" and place it in the "dist" folder (replace the old one)

## Releases:
- v1.3: Added support for inputting loginDetails in txt file instead of hardcode
- v1.4: Auto installs chromedriver 

If there are any other problems, reach me at: mshayanalwaha@gmail.com
