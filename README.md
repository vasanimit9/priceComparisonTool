# Price Compaison Tool
## For Software Engineering Project

### Setting Up The Virtual Environment
If you don't have the <code>virualenv</code> python package, you can install it by

```zsh
pip install virutalenv --user
```

If you the package installed, go to the root folder of the app, and run the following commands on bash

```zsh
virutalenv -p python3 venv
source venv/bin/activate
```

Now, you're in your virual environment. Next run

```zsh
pip install -r requirements.txt
```

### Credentials
You'll need to create a _credentials.py_ file in the root folder with the following format for your app to work properly. (We only have gmail support)
```python
login_ = 'your_email@gmail.com'
password_ = 'your_password'
secret_key = "your_secret_key"
```

### Run the flask app
Enter your virual environment (by <code>source venv/bin/activate</code>) if you're not already in it and run the following command

```zsh
flask run
```