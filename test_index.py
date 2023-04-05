from index import sum
import sys

def test_sum(mocker):
    mocker.patch.object(sys, 'argv', ['test_index.py', '2', '3'])
    result = sum(int(sys.argv[1]), int(sys.argv[2]))
    assert result == 5

    result = sum(2,3)
    assert result == 5