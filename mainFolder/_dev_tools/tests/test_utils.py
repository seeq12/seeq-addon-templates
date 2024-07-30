import stat
from pathlib import Path

import pytest
from mock import mock
from mock.mock import patch

from _dev_tools.utils import topological_sort, file_matches_criteria


@pytest.mark.unit
def test_topological_sort():
    graph = {
        'a': ['b', 'c'],
        'd': [],
        'b': ['c', 'd'],
        'c': ['d']
    }
    assert topological_sort(graph) == ['d', 'c', 'b', 'a']

    graph = {
        'a': ['b', 'c'],
        'b': ['c', 'd'],
        'c': ['d'],
        'd': ['e'],
        'e': []
    }
    assert topological_sort(graph) == ['e', 'd', 'c', 'b', 'a']


@pytest.mark.unit
def test_file_matches_criteria():
    root = Path('home') / 'username'
    assert file_matches_criteria(str(root), str(root / 'file.txt'))
    assert file_matches_criteria(str(root), str(root / '.config' / 'Code' / 'User' / 'settings.json'))

    file = root / '.config' / 'Code' / 'User' / '.settings.json'
    assert not file_matches_criteria(str(root), str(file), exclude_dot_files=True)

    file = root / '.config' / 'Code' / 'User' / '.settings.json'
    with patch('os.stat', return_value=mock.Mock(st_file_attributes=stat.FILE_ATTRIBUTE_HIDDEN)):
        assert file_matches_criteria(str(root), str(file), exclude_hidden_files=False)
        assert not file_matches_criteria(str(root), str(file), exclude_hidden_files=True)

    file = root / '.config' / 'Code' / 'User' / 'settings.json'
    assert not file_matches_criteria(str(root), str(file),
                                     excluded_files={str(Path('.config') / 'Code' / 'User' / 'settings.json')})
    assert file_matches_criteria(str(root), str(file),
                                 excluded_files={str(Path('.config') / 'Code' / 'User' / 'another.json')})
    assert file_matches_criteria(str(root), str(file),
                                 excluded_files={str(Path('.config') / 'Code' / 'User' / '.settings.json')})

    file = root / '.config' / 'Code' / 'User' / 'settings.json'
    assert file_matches_criteria(str(root), str(file), excluded_folders={'Code'})
    assert not file_matches_criteria(str(root), str(file), excluded_folders={str(Path('.config') / 'Code')})

    file = root / '.config' / 'Code' / 'User' / 'settings.json'
    assert file_matches_criteria(str(root), str(file), file_extensions={'.json'})
    assert not file_matches_criteria(str(root), str(file), file_extensions={'.txt'})
    assert file_matches_criteria(str(root), str(file), file_extensions={'.json', '.txt'})
