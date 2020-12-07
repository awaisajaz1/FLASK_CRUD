import pytest
from crud_ops import db, create_app

  
def sums(x):
    return x+1


def test_method():
    assert sums(1) == 2

def test_check_db():
    app = create_app()

    with app.app_context():
        db.create_all()
