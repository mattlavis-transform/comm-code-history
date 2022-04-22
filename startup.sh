source venv/bin/activate
kill -9 $(lsof -t -i:5000)
cd "/Users/mattlavis/sites and projects/1. Online Tariff/ott-admin"
killall node
npm start &
cd "/Users/mattlavis/sites and projects/1. Online Tariff/commodity_periods_flask"
python3 app.py
