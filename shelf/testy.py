from datetime import datetime

import pytest


def analyze_pesel(pesel):
    weights = [1, 3, 7, 9,
               1, 3, 7, 9, 1, 3]
    weight_index = 0
    digits_sum = 0
    for digit in pesel[: -1]:
        digits_sum += int(digit) * weights[weight_index]
        weight_index += 1
    pesel_modulo = digits_sum % 10
    validate = 10 - pesel_modulo
    if validate == 10:
        validate = 0
    gender = "male" if int(pesel[-2]) % 2 == 1 else "female"
    month = int(pesel[2:4])
    m_module = month // 20
    month = month - m_module * 20
    data = {
        0: '19',
        1: '20',
        2: '21',
        3: '22',
        4: '18'
    }
    b_of_year = data[m_module]
    year = int(b_of_year + pesel[0: 2])
    birth_date = datetime(year, month, int(pesel[4:6]))

    result = {
        "pesel": pesel,
        "valid": validate == int(pesel[-1]),
        "gender": gender,
        "birth_date": birth_date
    }
    return result


def add(a, b):
    return a + b


def div(a, b):
    return a / b


def test_add_22():
    assert add(2, 2) == 4


def test_add_00():
    assert add(0, 0) == 0


def test_add_11():
    assert add(1, 1) == 2


def test_add_54():
    assert add(5, 4) == 9


def test_div():
    assert 0.333 == pytest.approx(div(1, 3), 0.001)


def test_anal_pesel():
    pesel = '84083000654'
    wynik = analyze_pesel(pesel)
    assert wynik['gender'] == 'male'


def test_anal_pesel_g_female():
    pesel = '84083000664'
    wynik = analyze_pesel(pesel)
    assert wynik['gender'] == 'female'


@pytest.mark.parametrize("pesel, gender", [
    ("28070531952", 'male'),
    ("23122441218", 'male'),
    ("86012892374", 'male'),
    ("19102269394", 'male'),
    ("27081834713", 'male'),
    ("59040999223", 'female'),
    ("58110181847", 'female'),
    ("90073188288", 'female'),
    ("11111453845", 'female'),
    ("84020548762", 'female'),
])
def test_analyze_pesel_gender(pesel, gender):
    result = analyze_pesel(pesel)
    assert result['gender'] == gender


@pytest.mark.parametrize("pesel, valid", [
    ("28070531952", True),
    ("23122441211", False),
    ("59040999223", True),
    ("58110181841", False),
])
def test_analize_pesel_is_valid(pesel, valid):
    result = analyze_pesel(pesel)
    assert result['valid'] == valid


@pytest.mark.parametrize("pesel, date", [
    ("28070531952", datetime(year=1928, month=7, day=5)),
    ("23122441211", datetime(year=1923, month=12, day=24)),
    ("59040999223", datetime(year=1959, month=4, day=9)),
    ("58110181841", datetime(year=1958, month=11, day=1)),
    ("27290441812", datetime(year=2027, month=9, day=4)),
    ("43252939892", datetime(year=2043, month=5, day=29)),
    ('00410924631', datetime(year=2100, month=1, day=9)),
])
def test_analize_pesel_date(pesel, date):
    result = analyze_pesel(pesel)
    assert result['birth_date'] == date
