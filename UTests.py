# -*- coding: utf-8 -*-
from server import ParrentHandler
import pytest
import time


@pytest.mark.parametrize("znach", [u"Вованчик",	u"Вованчик Красный", u"Вованчик1",	u"Вован-чик", u"Вован.чик", u"Vovancik",	u"Во", u"йцукенйцукенйцукенйцукенйцукен"])
def test_1_CheckName_P(znach):
    print(znach)
    assert ParrentHandler.check_name(znach) is True


@pytest.mark.parametrize("znach", ["", u"В", u"Вован,к",	u"Вовка!",	u"Вов_ан", u"йцукенйцукенйцукенйцукенйцукенй"])
def test_2_CheckName_N(znach):
    print(znach)
    assert ParrentHandler.check_name(znach) is False


@pytest.mark.parametrize("znach", [u"Белов",	u"Белов Красный", u"Красный1",	u"Белов-Красный",	u"Бел.ов", u"Belov",	u"B"*2,	u"q"*50])
def test_3_CheckSurName_P(znach):
    print(znach)
    assert ParrentHandler.check_surname(znach) is True


@pytest.mark.parametrize("znach", ["",	u"к",	u"Бел,ов",	u"Belov!!!!",	u"Бе_лов", u"йцукевйцукейцукейцукейцукейцукейцукейцукейцукейцукейцуке"])
def test_4_CheckSurName_N(znach):
    print(znach)
    assert ParrentHandler.check_surname(znach) is False


@pytest.mark.parametrize("znach", [u"F", u"M"])
def test_5_CheckSex_P(znach):
    assert ParrentHandler.check_sex(znach) is True


@pytest.mark.parametrize("znach", [u"Мужик",	u"Пацан",	u"/v\\",	"1", ""])
def test_6_CheckSex_N(znach):
    assert ParrentHandler.check_sex(znach) is False


@pytest.mark.parametrize("znach", ["1999-12-12",	"1899-12-12",	time.strftime("%Y-%m-%d")])
def test_7_Birthday_P(znach):
    assert ParrentHandler.check_bitrhday(znach) is True


@pytest.mark.parametrize("znach", ["2099-12-12",	u"12.апр",	"02.04.2001", ""])
def test_8_Birthday_N(znach):
    assert ParrentHandler.check_bitrhday(znach) is False


@pytest.mark.parametrize("znach", [u"Русский",	u"Чумек чучмек", u"чуч32мек",	u"чуч-мек",	u"чуч.мек",	u"chuchmek",	u"ч"*2,	u"q"*20])
def test_9_Nationality_P(znach):
        assert ParrentHandler.check_nationality(znach) is True


@pytest.mark.parametrize("znach", [u"в", "", u"чу_ч", u"q"*21])
def test_10_Nationality_N(znach):
    assert ParrentHandler.check_nationality(znach) is False


@pytest.mark.parametrize("znach", [u"Москва",	u"Москва ул",	u"мосул.",	u"мос,ул",	u"мос-ул",	u"мосул;", u"M0sc0w",	u"м",	u"r"*50])
def test_11_Address_P(znach):
    assert ParrentHandler.check_address(znach) is True


@pytest.mark.parametrize("znach", ["", u"??вв",	u"мосул!",	u"q"*51,	u"[ул, центральная, Д, 5]",	u"SELECT * FROM STUDENT"])
def test_12_Address_N(znach):
    assert ParrentHandler.check_address(znach) is False


@pytest.mark.parametrize("znach", ["3",	"4.44",	"5.00", "2.00"])
def test_13_Mark_P(znach):
    assert ParrentHandler.check_mark(znach) is True


@pytest.mark.parametrize("znach", ["1.99", "", "4,44",	"5.01", "2.123", u"Пять", "010101"])
def test_14_Mark_N(znach):
    assert ParrentHandler.check_mark(znach) is False