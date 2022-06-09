# Bitly url shorterer

Console utility for shortening web links using [bit.ly](https://[bit.ly) service and counting clicks on shortened links.

### How to install

Python3 (required minimum version is `3.6`) should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### How to use

1. Launch `main.py` script.
2. Enter a long URL to create a bitlink (short URL made with Bitly service).
3. Or enter a bitlink URL to get a number of clicks done on it.
4. If either of those URLs were wrong or contained a typo, script will exit with an error message. Inspect the URL you had entered and try again.
5. You can enter as many URLs as you need. To exit the script just press `Enter` without typing anything.

### Usage exapmple

```
Enter a link (or just press "Enter" to quit): https://dvmn.org/encyclopedia
Bitlink: https://bit.ly/3tkfIKW

Enter a link (or just press "Enter" to quit): https://bit.ly/3tkfIKW
Number of clicks: 2

Enter a link (or just press "Enter" to quit): : https://dvmn.org/encyclopedia
HTTP error: 400 Client Error: Bad Request for url: https://api-ssl.bitly.com/v4/shorten
It is possible that your link contains a typo.

Enter a link (or just press "Enter" to quit): https://bit.ly/3tkfIKWW
HTTP error: 404 Client Error: Not Found for url: https://api-ssl.bitly.com/v4/bitlinks/bit.ly/3tkfIKWW/clicks/summary?units=-1
It is possible that your link contains a typo.

Enter a link (or just press "Enter" to quit): 

Process finished with exit code 0
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
