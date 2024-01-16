from time import sleep

import big_o
from challenges.challenge_palindromes_iterative import is_palindrome_iterative

from tests.complexities import (
    NOTATIONS,
    ComplexityInferenceData,
    infer_complexity,
    measure_execution_times,
)
from tests.generators import generate_palindromes


def test_iterative_palindrome_success():
    word = "I"
    assert is_palindrome_iterative(word) is True
    word = "GG"
    assert is_palindrome_iterative(word) is True
    word = "ANA"
    assert is_palindrome_iterative(word) is True
    word = "ESSE"
    assert is_palindrome_iterative(word) is True
    word = "SOCOS"
    assert is_palindrome_iterative(word) is True
    word = "REVIVER"
    assert is_palindrome_iterative(word) is True


def test_not_iterative_palindrome():
    word = "AGUA"
    assert is_palindrome_iterative(word) is False


def test_not_iterative_palindrome_when_empty_input():
    word = ""
    assert is_palindrome_iterative(word) is False


def test_evaluate_time_iterative_palindrome():
    assert (
        _correct_algorithm()
    ), "O algoritmo precisa estar correto para passar na validação de tempo"

    highest_acceptable_complexity = big_o.complexities.Linear

    # ! Tenta fazer o teste passar 3 vezes antes de confirmar que falhou
    for _ in range(3):
        data = ComplexityInferenceData(
            analyzed_function=is_palindrome_iterative,
            generation_function=generate_palindromes,
            # * Valores obtidos de forma empírica, por meio de testes robustos
            order_of_magnitude=6,
            initial_order=3,
            base_of_magnitude=3,
            execution_quantity=6561,
            times_to_repeat=3,
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
            f", mas deveria ser no máximo "
            f"{NOTATIONS[highest_acceptable_complexity]}"
        )


def _correct_algorithm():
    """Valida se o algoritmo está correto

    Roda as funções de teste que garantem que o algoritmo da função está
    correto

    Serve como uma função auxiliar para o cálculo de tempo, que necessita
    validar que o algoritmo está correto antes de validar o tempo de execução

    Returns
    -------
    bool
        True se todas as funções de teste passarem, False caso contrário
    """
    try:
        test_iterative_palindrome_success()
        test_not_iterative_palindrome()
        test_not_iterative_palindrome_when_empty_input()
    except AssertionError:
        return False
    return True
