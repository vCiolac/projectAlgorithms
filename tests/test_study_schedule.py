import pytest
import big_o
from time import sleep
from challenges.challenge_study_schedule import study_schedule

from tests.complexities import (
    NOTATIONS,
    ComplexityInferenceData,
    infer_complexity,
    measure_execution_times,
)
from tests.generators import generate_schedules


@pytest.mark.parametrize(
    "permanence_periods, target_time, expected",
    [
        ([(2, 2), (1, 2), (2, 3), (1, 5), (4, 5), (4, 5), (6, 7)], 5, 3),
        ([(2, 2), (1, 2), (2, 3), (1, 5), (4, 5), (4, 5)], 1, 2),
        ([(2, 2), (1, 2), (2, 3), (1, 5), (4, 5)], 3, 2),
        ([(1, 1), (2, 2), (3, 3), (4, 4)], 1, 1),
        ([(1, 2), (1, 3), (2, 3)], 2, 3),
    ],
)
def test_study_schedule_success(permanence_periods, target_time, expected):
    assert study_schedule(permanence_periods, target_time) == expected


@pytest.mark.parametrize(
    "permanence_periods, target_time",
    [
        ([(2, None), (1, 2), (2, 3), (1, 5), (4, 5), (4, 5), (6, 7)], 5),
        ([("2", 2), (1, 2), (2, 3), (1, 5), (4, 5), (4, 5)], 1),
        ([(2, "A"), (1, 2), (2, 3), (1, 5), (4, 5)], 3),
        ([(1, 1), (2, 2), (None, None), (4, 4)], 1),
        ([("1", 2), (None, 3), ("B", 3)], 2),
    ],
)
def test_study_schedule_invalid_permanence_periods(
    permanence_periods, target_time
):
    assert study_schedule(permanence_periods, target_time) is None


@pytest.mark.parametrize(
    "permanence_periods",
    [
        ([(2, 2), (1, 2), (2, 3), (1, 5), (4, 5), (4, 5), (6, 7)]),
        ([(2, 2), (1, 2), (2, 3), (1, 5), (4, 5), (4, 5)]),
        ([(2, 2), (1, 2), (2, 3), (1, 5), (4, 5)]),
        ([(1, 1), (2, 2), (3, 3), (4, 4)]),
        ([(1, 2), (1, 3), (2, 3)]),
    ],
)
def test_study_schedule_empty_target_time(permanence_periods):
    target_time = None
    assert study_schedule(permanence_periods, target_time) is None


def test_evaluate_time_study_schedule():
    assert (
        _correct_algorithm()
    ), "O algoritmo precisa estar correto para passar na validação de tempo"

    highest_acceptable_complexity = big_o.complexities.Linear

    # ! Tenta fazer o teste passar 3 vezes antes de confirmar que deu ruim
    for _ in range(3):
        data = ComplexityInferenceData(
            analyzed_function=lambda valores: study_schedule(*valores),
            generation_function=generate_schedules,
            # * Valores obtidos de forma empírica, por meio de testes robustos
            order_of_magnitude=5,
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
        test_study_schedule_success(
            [(2, 2), (1, 2), (2, 3), (1, 5), (4, 5), (4, 5), (6, 7)], 5, 3
        )
        test_study_schedule_invalid_permanence_periods(
            [(2, None), (1, 2), (2, 3), (1, 5), (4, 5), (4, 5), (6, 7)], 5
        )
        test_study_schedule_empty_target_time(
            [(2, 2), (1, 2), (2, 3), (1, 5), (4, 5), (4, 5), (6, 7)]
        )
        permanence_periods = [(2, 2), (1, 2), (2, 3), (1, 5), (4, 5), (4, 5)]
        algorithms_correct = study_schedule(permanence_periods, 5) == 3

        assert algorithms_correct
    except AssertionError:
        return False
    return True
