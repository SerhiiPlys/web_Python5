import pytest
import os
from sort_garbage import make_trans_dict
from sort_garbage import check_name
from sort_garbage import check_empty_dir
from sort_garbage import del_empty_dir

TRANS = {}
make_trans_dict()


@pytest.fixture
def path_empty():
    path_tst = "C:\\Users\\Ultra\\Desktop\\garbage"
    return path_tst


def test_check_name():
    assert check_name("фишинг") == "fishing"
    assert check_name("video") == "video"
    assert check_name("12&qwa*") == "12_qwa_"
    assert check_name("шото_14") == "shoto_14"


def test_check_empty_dir(path_empty):
    assert check_empty_dir(path_empty) is True


@pytest.mark.asyncio
async def test_del_empty_dir(path_empty):
    assert os.path.exists(path_empty) is True
    await del_empty_dir(path_empty)
    assert os.path.exists(path_empty) is False

