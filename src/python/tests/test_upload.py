import pytest
import platform
from os.path import dirname, join
from rabbie import DriveService, DriveServiceError, google_auth, GoogleAuthError


@pytest.fixture(scope='module')
def credentials():
    return google_auth()


@pytest.fixture(scope='module')
def service(credentials):
    return DriveService(credentials)


def test_folder_not_found_error(service):

    with pytest.raises(FileNotFoundError):
        service.get_folder_id('bad_folder_name')


def test_make_directory(service):

    hostname = platform.node()

    folder_id = service.create_folder(hostname)

    queried_id = service.get_folder_id(hostname)

    assert queried_id == folder_id


@pytest.mark.parametrize('folder_name, file_name', [(None, 'test_image_1.jpeg'),
                                                    (platform.node(), 'test_image_2.jpeg')])
def test_upload_image(service, folder_name, file_name):

    file_path = join(
        dirname(__file__),
        'resources',
        file_name
    )

    service.upload_image(file_path, folder_name)

    files = service.list_files()
    assert file_name in files.values()
