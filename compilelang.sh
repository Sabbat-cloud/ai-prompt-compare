pybabel extract -F babel.cfg -o messages.pot app.py ai_models/ templates/

pybabel init -i messages.pot -d translations -l en

pybabel update -i messages.pot -d translations

pybabel compile -d translations
