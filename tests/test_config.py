import pytest
from Akeso.config import challenge_mapper


@pytest.mark.parametrize("challenge, expected_ret", [
    ('maze', ('maze', ['mazeAttack'], ['maze'], 31337)),
    ('SQL', ('sqlisimple', ['SQLi'], ['SQLiSimple'], 80)),
    ('shell', ('shell', ['shellAttack'], ['shell'], 4001)),
    ('nginx', ('nginx', ['DirectoryTraversal'], ['ApacheDirectoryTraversal'], 80))
])
def test_challenge_mapper(challenge, expected_ret):
    ret = challenge_mapper(challenge)
    assert ret == expected_ret
