from fractions import Fraction as F
import pytest
from consent_lottery import Menu
from consent_lottery.broker import OneShotBroker


def test_exact_outcome_counts_all_profiles():
    menu=Menu(3,(3,5,6))
    for profile in range(8):
        outcomes=[]
        for draw in range(20):
            broker=OneShotBroker(menu,['1/20']*3,['1/10']*3)
            outcomes.append(broker.select(profile,randbelow=lambda _,d=draw:d))
        for j,contract in enumerate(menu.contracts):
            assert outcomes.count(j)==int(contract&profile==contract)


def test_veto_consumes_one_draw_and_one_session():
    broker=OneShotBroker(Menu(2,(3,)),['1/10'],['1/10']*2)
    assert broker.select(0,randbelow=lambda _:0) is None
    with pytest.raises(RuntimeError):broker.select(3,randbelow=lambda _:0)


def test_rational_privacy_validation_is_exact():
    with pytest.raises(ValueError):
        OneShotBroker(Menu(2,(1,3)),['1/10','1/100000000000000000000'],['1/10']*2)


def test_abstention_remainder_and_contract_index():
    menu=Menu(3,(3,5,6))
    assert OneShotBroker(menu,['1/20']*3,['1/10']*3).select(7,randbelow=lambda _:19) is None
    assert OneShotBroker(menu,['1/20']*3,['1/10']*3).select(7,randbelow=lambda _:1)==1
