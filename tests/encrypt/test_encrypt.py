import pytest
from challenges.challenge_encrypt_message import encrypt_message


def test_encrypt_message():
    assert encrypt_message("TypeScript", 4) == "tpircS_epyT"
    assert encrypt_message("Test", 1) == "T_tse"
    assert encrypt_message("Pitanga", 3) == "tiP_agna"
    assert encrypt_message("Crocodilo", 0) == "olidocorC"
    assert encrypt_message("Trem", 7) == "merT"
    assert encrypt_message("", 9) == ""

    with pytest.raises(TypeError) as e:
        encrypt_message(123, 2)
    assert str(e.value) == "tipo inválido para message"

    with pytest.raises(TypeError) as e:
        encrypt_message("m4dr0g4d4", "ésolidao")
    assert str(e.value) == "tipo inválido para key"
