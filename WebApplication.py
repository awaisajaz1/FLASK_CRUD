from crud_ops import create_app, db

app = create_app()

# with app.app_context():
#     db.create_all()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5666, debug=True)
