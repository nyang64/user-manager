from test.flask_app1 import create_test_app
from unittest import TestCase

import pytest
from model.patient import Patient
from services.repository.db_repositories import DbRepository
from werkzeug.exceptions import InternalServerError


class Model:
    pass


class TestDbRepo(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.db_repo = DbRepository()
        # self.populate_data = PopulateData()

    def test_save_db(self):
        model = Model()
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                print(e)
                self.db_repo.save_db(model)

    def test_save_db_raise_exception(self):
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                print(e)
                self.db_repo.save_db(Patient())
            self.assertIsInstance(e.value, InternalServerError)

    def test_flush_db(self):
        model = Model()
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                print(e)
                self.db_repo.flush_db(model)

    def test_flush_db_raise_exception(self):
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                print(e)
                self.db_repo.flush_db(Patient())
            self.assertIsInstance(e.value, InternalServerError)

    def test_delete_obj(self):
        model = Model()
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                print(e)
                self.db_repo.delete_obj(model)

    def test_delete_obj_raise_exception(self):
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                print(e)
                self.db_repo.delete_obj(Patient())
            self.assertIsInstance(e.value, InternalServerError)

    def test_update_db(self):
        app = create_test_app()
        with app.app_context():
            self.db_repo.update_db(None)
