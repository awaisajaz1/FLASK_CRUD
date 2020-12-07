from crud_ops import create_app, db

app = create_app()

# with app.app_context():
#     db.create_all()

if __name__ == '__main__':
<<<<<<< HEAD
    app.run(host='0.0.0.0', port=5000, debug=True)
=======
    app.run(debug=True)
>>>>>>> 46b729796325f1d6c68644d23977873d778a83f3
