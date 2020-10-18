# urnie

# Purpose

Urnie was built to have a non-browser-dependent means of managing keywords for accessing websites. 

At its core, it is a service for managing associations between URLs and submitted keywords. The service will then expose a web endpoint named after the keyword which can be used to redirect to the destination URL.

For example, a keyword of `example` associated with a URL of `https://www.example.com` will result in the endpoint `$URNIE_HOST/urn/example`, which when accessed will direct the browser to `https://www.example.com`.

Submissions for keywords head into a review queue. The service administrator approves, rejects and/or edits submissions accordingly before they become usable keywords.

# Dependencies

- Python 3
- A SQLAlchemy-compatible database (eg PostgreSQL, MariaDB)

# Initialisation

```bash
# Installing dependencies
pip install -r requirements.txt
export FLASK_APP=urnie

# Initialising database for first-time use
export DATABASE_URI=(database URI)
flask db init
flask db migrate
flask db upgrade

# Running the application
python app.py
```

# License

See [LICENSE](LICENSE)

