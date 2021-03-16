import pytest
from model.group import Group
from model.utils import random_string

testdata = [
    Group(name="" if name else random_string("name", 10),
          header="" if header else random_string("header", 20),
          footer="" if footer else random_string("footer", 20))
    for name in [True, False]
    for header in [True, False]
    for footer in [True, False]
]


@pytest.mark.parametrize("group", testdata, ids=[repr(g) for g in testdata])
def test_add_group(app, group):
    old_groups = app.group.get_group_list()
    app.group.create(group)

    # new list is longer, because we added 1 element
    assert app.group.count() == len(old_groups) + 1

    # if new list length is correct, then we can compare lists.
    # so we can get new list
    new_groups = app.group.get_group_list()

    # built expected list for equalizing NEW and EXPECTED
    # expected = old _list + new_group. And sort()
    # sort() will use method __lt__, which was overridden
    old_groups.append(group)
    assert sorted(new_groups) == sorted(old_groups)