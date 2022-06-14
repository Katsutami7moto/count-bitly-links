# Bitly URL shortener

Console utility for shortening web links using [bit.ly](https://bit.ly) service and counting clicks on shortened links.

### How to install

Python3 (required minimum version is `3.6`) should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
Before you start using the utility, you will need an access token. Here is how to set it up:

1. If you haven't, download the [ZIP archive](https://github.com/Katsutami7moto/count_bitly_links/archive/refs/heads/main.zip) of the script and unzip it.
2. Go to the directory where `main.py` file is and create a file with the name `.env` (yes, it has only the extension). It is the file to contain environmental variables that usually store data unique to each user, thus you will need to create your own.
3. Copy this string: `ACCESS_TOKEN='{token}'` and paste it to `.env` file.
4. Sign up for [bit.ly](https://bit.ly) service (or log in to it, if you already had).
5. Go to ["API" section of "Settings" page](https://app.bitly.com/settings/api/).
6. Enter your password and click `Generate token` button.
7. Copy the token and substitute `{token}` portion of `.env` file with it. Token has to remain inside `' '` quotation marks and without `{ }` curly brackets.
8. That's it! Now the script will use your token to access [bit.ly](https://bit.ly) service in order to run script's functions.

### How to use

1. You can run this script in two modes:
   - Without arguments to use `loop mode` if you need to process more than one link.
     - ```commandline
       python3 main.py
       ```
   - Or with URL as optional positional argument, like this:
     - ```commandline
       python3 main.py -u URL
       ```
3. Enter a long URL to create a bitlink (short URL made with [bit.ly](https://bit.ly) service).
4. Or enter a bitlink URL to get a number of clicks done on it.
5. If either of those URLs were wrong or contained a typo, the script will show an error message. Inspect the URL you had entered and try again.
6. In `loop mode` you can enter as many URLs as you need. To exit the script, just press `Enter` without typing anything.

### Usage example

With command line argument:
```commandline
python3 main.py -u https://dvmn.org/encyclopedia
Bitlink: https://bit.ly/3tkfIKW

python3 main.py --url https://bit.ly/3tkfIKW
Number of clicks: 2

python3 main.py -u https://bit.ly/3tkfIKWW
HTTP error: 400 Client Error: Bad Request for url: https://api-ssl.bitly.com/v4/shorten
It is possible that your link contains a typo.

```

In loop mode:
```
Enter a link (or just press "Enter" to quit): https://dvmn.org/encyclopedia
Bitlink: https://bit.ly/3tkfIKW

Enter a link (or just press "Enter" to quit): https://bit.ly/3tkfIKW
Number of clicks: 2

Enter a link (or just press "Enter" to quit): https://bit.ly/3tkfIKWW
HTTP error: 400 Client Error: Bad Request for url: https://api-ssl.bitly.com/v4/shorten
It is possible that your link contains a typo.

Enter a link (or just press "Enter" to quit): 

Process finished with exit code 0
```

### Project Goals

The code is written for educational purposes on the online-course for web-developers, [dvmn.org](https://dvmn.org/).
