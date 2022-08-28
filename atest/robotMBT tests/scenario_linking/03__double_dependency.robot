*** Settings ***
Documentation     There are three test cases, one must go first. The other two are both
...               valid as a second scenario. However, if you pick the wrong one, the
...               third scenario cannot be added anymore, because its precondition will
...               fail. The scenarios are included in the suite in reverse order to
...               force the model to reorganise the scenarios.
Suite Setup       Suite setup
Suite Teardown    Should be equal    ${test_count}    ${3}
Test Setup        Set Global Variable    ${test_count}    ${test_count+1}
Resource          birthday_cards.resource
Library           robotmbt

*** Test Cases ***
trailing scenario
    Given the birthday card has 'Johan' written on it
    when 'Tannaz' writes their name on the birthday card
    then the birthday card has 'Johan' written on it
    and the birthday card has 'Tannaz' written on it
    [Teardown]    Should be equal    ${test_count}    ${3}

middle scenario
    Given the birthday card has 1 name written on it
    when 'Nicolas' writes their name on the birthday card
    then the birthday card has 'Nicolas' written on it
    and the birthday card has 2 names written on it
    [Teardown]    Should be equal    ${test_count}    ${2}

leading scenario
    Given a blank birthday card
    when 'Johan' writes their name on the birthday card
    then the birthday card has 'Johan' written on it
    [Teardown]    Should be equal    ${test_count}    ${1}

*** Keywords ***
Suite setup
    Set Global Variable    ${test_count}    ${0}
    Treat this test suite Model-based