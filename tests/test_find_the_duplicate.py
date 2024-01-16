from time import sleep

import big_o
from challenges.challenge_find_the_duplicate import find_duplicate

from tests.complexities import (
    NOTATIONS,
    ComplexityInferenceData,
    infer_complexity,
    measure_execution_times,
)
from tests.generators import generate_integers


def test_find_duplicate_number_with_success():
    nums = [1, 3, 4, 2, 2]
    assert find_duplicate(nums) == 2
    nums = [3, 1, 3, 4, 2]
    assert find_duplicate(nums) == 3
    nums = [1, 1]
    assert find_duplicate(nums) == 1
    nums = [1, 1, 2]
    assert find_duplicate(nums) == 1
    nums = [3, 1, 2, 4, 6, 5, 7, 7, 7, 8]
    assert find_duplicate(nums) == 7


def test_not_duplicate_when_empty_input():
    nums = []
    assert find_duplicate(nums) is False


def test_not_duplicate_when_string_input():
    nums = ["a", "b"]
    assert find_duplicate(nums) is False


def test_not_duplicate_numbers():
    nums = [1, 2]
    assert find_duplicate(nums) is False


def test_not_duplicate_when_single_number():
    nums = [1]
    assert find_duplicate(nums) is False


def test_not_duplicate_when_negative_numbers():
    nums = [-1, -1]
    assert find_duplicate(nums) is False


def test_evaluate_time_find_the_duplicate():
    assert (
        _correct_algorithm()
    ), "O algoritmo precisa estar correto para passar na validação de tempo"

    highest_acceptable_complexity = big_o.complexities.Linearithmic

    # ! Tenta fazer o teste passar algumas vezes antes de confirmar que falhou
    # ! , bem como aumenta a quantidade de entradas a cada vez que falha
    for tries in range(5):
        data = ComplexityInferenceData(
            analyzed_function=find_duplicate,
            generation_function=generate_integers,
            # * Valores obtidos de forma empírica, por meio de testes robustos
            order_of_magnitude=5 + tries // 2,
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
            ", mas deveria ser no máximo "
            f"{NOTATIONS[highest_acceptable_complexity]}"
        )


def _correct_algorithm() -> bool:
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
        test_find_duplicate_number_with_success()
        test_not_duplicate_when_empty_input()
        test_not_duplicate_when_string_input()
        test_not_duplicate_numbers()
        test_not_duplicate_when_single_number()
        test_not_duplicate_when_negative_numbers()
    except AssertionError:
        return False
    return True
