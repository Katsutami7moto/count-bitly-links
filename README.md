# Bitly url shorterer

Console utility for shortening web links using [bit.ly](https://[bit.ly) service and counting clicks on shortened links.

### How to install

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### How to use

1. Launch `main.py` script.
2. Enter a long URL to create a bitlink (short URL made with Bitly service).
3. Or enter a bitlink URL to get a number of clicks done on it.
4. If either of those URLs were wrong or contained a typo, script will exit with an error message. Inspect the URL you had entered and try again.

### Usage exapmples

```
Введите ссылку: https://dvmn.org/encyclopedia
Битлинк: https://bit.ly/3tkfIKW

Process finished with exit code 0
```

```
Введите ссылку: https://bit.ly/3tkfIKW
Количество переходов: 1

Process finished with exit code 0
```

```
Введите ссылку: https://dvmn.org/encyclopedi
HTTP error: 404 Client Error: Not Found for url: https://dvmn.org/encyclopedi
It is possible that your link contains a typo.

Process finished with exit code 1
```

```
Введите ссылку: https://bit.ly/3tkfIKWW
HTTP error: 404 Client Error: Not Found for url: https://api-ssl.bitly.com/v4/bitlinks/bit.ly/3tkfIKWW/clicks/summary?units=-1
It is possible that your link contains a typo.

Process finished with exit code 1
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
