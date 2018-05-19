# translates

This is a small web-based application that helps you to exercise in Russian to English translations.


![alt text](https://raw.githubusercontent.com/generall/translates/master/docs/screen.png)

# Description

Clone this repo, [register](https://tech.yandex.com/translate/) Yandex transtation API key service (optional) and run:

```
YANDEX_API_KEY=<YOUR_KEY> FLASK_APP=server.py flask run
```
Now you can open [localhost:5000/page/index.html](http://localhost:5000/page/index.html).

You can put additional phrases translations into `data/stories`.
It will also save your commited texts into `data/saved.tsv`.

