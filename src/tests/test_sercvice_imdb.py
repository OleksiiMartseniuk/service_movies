import pytest
from src.service.imdb import service
from unittest import mock


class TestServiceIMDB:
    @mock.patch('src.service.imdb.collection_table.ServiceDBIMDB')
    def test_delete(self, MockServiceDBIMDB):
        print(type(MockServiceDBIMDB))
        db = MockServiceDBIMDB()
        service.delete(db)
        db.delete_tables.assert_called_once()
        db.close_db.assert_called_once()

    @mock.patch('src.service.imdb.collection_table.ServiceDBIMDB')
    def test_init(self, MockServiceDBIMDB):
        db = MockServiceDBIMDB()
        service.init(db)
        db.write_table.assert_called_once()
        db.close_db.assert_called_once()

    @mock.patch('src.service.imdb.write_file.ServiceJsonWrite')
    @mock.patch('src.service.imdb.imdb_api.ClientIMDB')
    def test_write_prem_account(self, MockClientIMDB, MockServiceJsonWrite):
        client = MockClientIMDB()
        writer = MockServiceJsonWrite()
        client.user_count.return_value = {'maximum': 600, 'count': 0}
        service.write(client, writer)
        client.collection_data.assert_called_once()
        writer.write_file_group.assert_called_once()
        writer.write_file_movie.assert_called_once()

    @mock.patch('src.service.imdb.write_file.ServiceJsonWrite')
    @mock.patch('src.service.imdb.imdb_api.ClientIMDB')
    def test_write_error(self, MockClientIMDB, MockServiceJsonWrite):
        client = MockClientIMDB()
        writer = MockServiceJsonWrite()
        client.user_count.return_value = {'maximum': 100, 'count': 95}
        with pytest.raises(ValueError) as excinfo:
            service.write(client, writer)
        assert "Not enough service requests." in str(excinfo.value)

    @mock.patch('src.service.imdb.write_file.ServiceJsonWrite')
    @mock.patch('src.service.imdb.imdb_api.ClientIMDB')
    def test_write_star_stop_error(self, MockClientIMDB, MockServiceJsonWrite, monkeypatch):
        answers = iter([1, 30])

        client = MockClientIMDB()
        writer = MockServiceJsonWrite()
        client.user_count.return_value = {'maximum': 100, 'count': 80}
        with pytest.raises(ValueError) as excinfo:
            monkeypatch.setattr('builtins.input', lambda number: next(answers))
            service.write(client, writer)
        assert "Not enough service requests." in str(excinfo.value)

    @mock.patch('src.service.imdb.service.error_path')
    @mock.patch('src.service.imdb.write_file.ServiceJsonWrite')
    @mock.patch('src.service.imdb.imdb_api.ClientIMDB')
    def test_write_star_stop_error_path_true(self, MockClientIMDB, MockServiceJsonWrite, mock_error_path, monkeypatch):
        answers = iter([1, 30])

        client = MockClientIMDB()
        writer = MockServiceJsonWrite()
        mock_error_path.return_value = True
        client.user_count.return_value = {'maximum': 100, 'count': 30}

        monkeypatch.setattr('builtins.input', lambda number: next(answers))
        service.write(client, writer)
        writer.before_recording.assert_called_once()

    @mock.patch('src.service.imdb.service.error_path')
    @mock.patch('src.service.imdb.write_file.ServiceJsonWrite')
    @mock.patch('src.service.imdb.imdb_api.ClientIMDB')
    def test_write_star_stop_error_path_false(self, MockClientIMDB, MockServiceJsonWrite, mock_error_path, monkeypatch):
        answers = iter([1, 30])

        client = MockClientIMDB()
        writer = MockServiceJsonWrite()
        mock_error_path.return_value = False
        client.user_count.return_value = {'maximum': 100, 'count': 30}

        monkeypatch.setattr('builtins.input', lambda number: next(answers))
        service.write(client, writer)
        writer.before_recording.assert_called_once()
        writer.write_file_group.assert_called_once()

    @mock.patch('src.service.imdb.service.ServiceDBIMDB')
    @mock.patch('src.service.imdb.service.ServiceJsonWrite')
    @mock.patch('src.service.imdb.service.ClientIMDB')
    @mock.patch('src.service.imdb.service.write')
    def test_collection_data_write(self, ServiceDBIMDB, ServiceJsonWrite, ClientIMDB, moke_write, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'write')
        service.collection_data()
        moke_write.assert_called_once()

    @mock.patch('src.service.imdb.service.ServiceDBIMDB')
    @mock.patch('src.service.imdb.service.ServiceJsonWrite')
    @mock.patch('src.service.imdb.service.ClientIMDB')
    @mock.patch('src.service.imdb.service.delete')
    def test_collection_data_delete(self, ServiceDBIMDB, ServiceJsonWrite, ClientIMDB, moke_delete, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'delete')
        service.collection_data()
        moke_delete.assert_called_once()

    @mock.patch('src.service.imdb.service.ServiceDBIMDB')
    @mock.patch('src.service.imdb.service.ServiceJsonWrite')
    @mock.patch('src.service.imdb.service.ClientIMDB')
    def test_collection_data_error(self, ServiceDBIMDB, ServiceJsonWrite, ClientIMDB, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'sdsdad')
        with pytest.raises(SyntaxError) as excinfo:
            service.collection_data()
        assert "Invalid command!" in str(excinfo.value)

    @mock.patch('src.service.imdb.service.ServiceDBIMDB')
    @mock.patch('src.service.imdb.service.ServiceJsonWrite')
    @mock.patch('src.service.imdb.service.ClientIMDB')
    @mock.patch('src.service.imdb.service.init')
    def test_collection_data_init(self, ServiceDBIMDB, ServiceJsonWrite, ClientIMDB, moke_init, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'init')
        service.collection_data()
        moke_init.assert_called_once()
