import pytest
import big_o
import re
from time import sleep
from challenges.challenge_anagrams import is_anagram

from tests.complexities import (
    NOTATIONS,
    ComplexityInferenceData,
    infer_complexity,
    measure_execution_times,
)
from tests.generators import generate_anagrams


class RequirementViolated(Exception):
    pass


def check_usage_of_builtin_sorting():
    with open("challenges/challenge_anagrams.py", "r") as python_file:
        source = python_file.read()
        if "sorted(" in source or ".sort(" in source or "Counter(" in source:
            raise RequirementViolated(
                "Você deve fazer sua própria implementação "
                "do algoritmo de ordenação!"
            )

        if re.findall(r"^import", source):
            raise RequirementViolated(
                "Você não pode importar nada no challenge_anagrams.py!"
            )


@pytest.mark.parametrize(
    "input_first_string, input_second_string",
    [
        pytest.param(
            "pedra",
            "perdaaa",
            marks=pytest.mark.dependency(name="not_anagram_1"),
        ),
        pytest.param(
            "camelo",
            "cameeelo",
            marks=pytest.mark.dependency(name="not_anagram_2"),
        ),
        pytest.param(
            "rio", "ryo", marks=pytest.mark.dependency(name="not_anagram_3")
        ),
        pytest.param(
            "f", "u", marks=pytest.mark.dependency(name="not_anagram_4")
        ),
        pytest.param(
            "aeiouaeiou",
            "aiiouaiiou",
            marks=pytest.mark.dependency(name="not_anagram_5"),
        ),
    ],
)
@pytest.mark.dependency()
def test_words_are_not_anagrams(input_first_string, input_second_string):
    check_usage_of_builtin_sorting()

    first_string = input_first_string
    second_string = input_second_string
    ordered_first_string = "".join(sorted(first_string))
    ordered_second_string = "".join(sorted(second_string))
    assert is_anagram(first_string, second_string) == (
        ordered_first_string,
        ordered_second_string,
        False,
    )


@pytest.mark.parametrize(
    "input_first_string, input_second_string",
    [
        pytest.param(
            "pedra", "perda", marks=pytest.mark.dependency(name="anagram_1")
        ),
        pytest.param(
            "amor", "roma", marks=pytest.mark.dependency(name="anagram_2")
        ),
        pytest.param(
            "alegria",
            "alergia",
            marks=pytest.mark.dependency(name="anagram_3"),
        ),
        pytest.param(
            "muro", "rumo", marks=pytest.mark.dependency(name="anagram_4")
        ),
        pytest.param("f", "f", marks=pytest.mark.dependency(name="anagram_5")),
    ],
)
@pytest.mark.dependency()
def test_words_are_anagrams(input_first_string, input_second_string):
    check_usage_of_builtin_sorting()

    first_string = input_first_string
    second_string = input_second_string
    ordered_first_string = "".join(sorted(first_string))
    ordered_second_string = "".join(sorted(second_string))
    assert is_anagram(first_string, second_string) == (
        ordered_first_string,
        ordered_second_string,
        True,
    )


@pytest.mark.parametrize(
    "input_first_string, input_second_string",
    [
        pytest.param(
            "", "perda", marks=pytest.mark.dependency(name="empty_1")
        ),
        pytest.param("amor", "", marks=pytest.mark.dependency(name="empty_2")),
        pytest.param(
            "", "alergia", marks=pytest.mark.dependency(name="empty_3")
        ),
        pytest.param("muro", "", marks=pytest.mark.dependency(name="empty_4")),
        pytest.param("", "", marks=pytest.mark.dependency(name="empty_5")),
    ],
)
@pytest.mark.dependency()
def test_empty_string_anagram(input_first_string, input_second_string):
    check_usage_of_builtin_sorting()

    first_string = input_first_string
    second_string = input_second_string
    ordered_first_string = "".join(sorted(first_string))
    ordered_second_string = "".join(sorted(second_string))
    assert is_anagram(first_string, second_string) == (
        ordered_first_string,
        ordered_second_string,
        False,
    )


@pytest.mark.parametrize(
    "input_first_string, input_second_string",
    [
        pytest.param(
            "PEDRA",
            "perda",
            marks=pytest.mark.dependency(name="case_insensitive_1"),
        ),
        pytest.param(
            "amor",
            "RomA",
            marks=pytest.mark.dependency(name="case_insensitive_2"),
        ),
        pytest.param(
            "ALEgria",
            "alergia",
            marks=pytest.mark.dependency(name="case_insensitive_3"),
        ),
        pytest.param(
            "muro",
            "RuMo",
            marks=pytest.mark.dependency(name="case_insensitive_4"),
        ),
        pytest.param(
            "f", "F", marks=pytest.mark.dependency(name="case_insensitive_5")
        ),
    ],
)
def test_words_are_anagrams_case_insensitive(
    input_first_string, input_second_string
):
    check_usage_of_builtin_sorting()

    first_string = input_first_string
    second_string = input_second_string
    ordered_first_string = "".join(sorted(first_string.lower()))
    ordered_second_string = "".join(sorted(second_string.lower()))
    assert is_anagram(first_string, second_string) == (
        ordered_first_string,
        ordered_second_string,
        True,
    )


@pytest.mark.dependency(
    depends=[
        "not_anagram_1",
        "not_anagram_2",
        "not_anagram_3",
        "not_anagram_4",
        "not_anagram_5",
    ]
)
@pytest.mark.dependency(
    depends=["anagram_1", "anagram_2", "anagram_3", "anagram_4", "anagram_5"]
)
@pytest.mark.dependency(
    depends=["empty_1", "empty_2", "empty_3", "empty_4", "empty_5"]
)
@pytest.mark.dependency(
    depends=[
        "case_insensitive_1",
        "case_insensitive_2",
        "case_insensitive_3",
        "case_insensitive_4",
        "case_insensitive_5",
    ]
)
def test_evaluate_time_anagram():
    highest_acceptable_complexity = big_o.complexities.Linearithmic

    # ! Tenta fazer o teste passar 3 vezes antes de confirmar que deu ruim
    for _ in range(3):
        data = ComplexityInferenceData(
            analyzed_function=lambda tupla_de_str: is_anagram(*tupla_de_str),
            generation_function=generate_anagrams,
            # * Valores obtidos de forma empírica, por meio de testes robustos
            order_of_magnitude=6,
            initial_order=3,
            base_of_magnitude=2,
            execution_quantity=243,
            times_to_repeat=9,
        )

        results = measure_execution_times(data)
        observed_complexity = infer_complexity(
            results.registered_sizes, results.registered_times
        )

        if observed_complexity <= highest_acceptable_complexity:
            break
        sleep(3)
    else:
        assert False, (
            "Seu algoritmo parece ser "
            f"{NOTATIONS[observed_complexity.__class__]}"  # type:ignore
            ", mas deveria ser no máximo "
            f"{NOTATIONS[highest_acceptable_complexity]}"
        )
