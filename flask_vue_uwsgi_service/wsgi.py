from flask_vue_uwsgi_service.app import app

print(__name__)
if __name__ == "__main__":

    app.run()


# [uwsgi]
# http=:5000
# wsgi-file=/root/Github/flask_vue_pro/flask_vue_uwsgi_service/wsgi.py
# callable=app
# processes=4
# threads=2
