# robotframeworkMBT - the oneliner

 Model-based testing in Robot framework with test case generation

## Introduction

This project is an extension to [Robot framework](https://robotframework.org/) for model-based testing. The term model-based testing, or MBT in short, has been used in many different ways. Within this context two modelling aspects are most important. The first is about domain modelling using a domain specific language, or DSL. [Robot framework](https://robotframework.org/) already has great support for this aspect, which is why it was used as a base. The second aspect is about test case generation.

Test case generation introduces a more dynamic approach to executing a test suite. A typical traditional test suite is executed front to back. For maintainability reasons, test cases are often kept independent of each other. The down side to this approach is that there is little variation and often a lot of duplication, mostly during the setup phases.

With this project we aim to get the best of both worlds. Allowing testers to write small, independent cases that are automatically combined. Finding more issues in less time, by focusing on effectively reaching the desired coverage.

## Installation

The recommended installation method is using [pip](http://pip-installer.org)

    pip install robotframework-mbt

After installation include `robotmbt` as library in your robot file to get access to the new functionality.

## Capabilities

To get a feel for what this library can do, have a look at our [Titanic themed demo](https://github.com/JFoederer/robotframeworkMBT/tree/main/demo/Titanic), that his executable as a [Robot framework](https://robotframework.org/) test suite. Current capabilities focus around complete scenarios. When all steps are properly annotated with modelling info, the library can resolve their dependencies to figure out the correct execution order. To be successful, the set of scenarios in the model must be composable into a single complete sequence, without repetitions or leftovers.

## How to model

Modelling can be done directy from [Robot framework](https://robotframework.org/), without the need for additional tooling. The popular _Given-When-Then_ style is used to capture behaviour in scenarios. Consider these two scenarios:

```
Buying a postcard
    When you buy a new postcard
    then you have a blank postcard

Preparing for a birthday party
    Given you have a blank postcard
    When you write 'Happy birthday!' on the postcard
    then you are ready to go to the birthday party
```

Mapping the dependencies between scenarios is done by annotating the steps with modelling info. Modelling info is added to the documentation of the step as shown below. Regular documentation can still be added, as long as `*model info*` starts on a new line and a whiteline is included after the last `:OUT:` expressions.

```
you buy a new postcard
    [Documentation]    *model info*
    ...    :IN: None
    ...    :OUT: new postcard | postcard.wish=None

you have a blank postcard
    [Documentation]    *model info*
    ...    :IN: postcard.wish==None
    ...    :OUT: postcard.wish==None
```

The first scenario can be executed directly. It has no dependencies that need to be resolved before going into its first step, as indicated by the `:IN:` expression which is `None`. After completing the step, a new domain term is available with a single property. The term `postcard` with property `wish` is introduced, as stated by the `:OUT:` expressions. This satisfies the condition for the then-step to complete this scenario.

The second scenario has a dependency to the first scenario, due to the condition stated in the given-step of the scenario. How this works is by evaluating the expressions according to this schema:

* given-steps evaluate only the `:IN:` expressions
* when-steps evaluate both the `:IN:` and `:OUT:` expressions
* then-steps evaluate only the `:OUT:` expressions

If evaluation of any expressions fails or is False, then the scenario is rejected. By properly annotating all steps to reflect their impact on the system or its environment, you can model the intended relations between scenarios. This forms the specification model. The step implementations use keywords to connect to the system under test to verify the specified behaviour.

There are three typical kinds of steps

* __Stative__  
  Stative steps express a truth value. Like _you have a blank postcard_ For these steps the `:IN:` and `:OUT:` expressions have identical conditions and the step implementation consists purely of checks.
* __Action__  
  Action steps perform an action on the system that alters its state. These steps can have dependencies in their `:IN:` conditions that are needed to complete the action. Statements in the `:OUT:` expressions indicate what changes are expected by executing this action.
* __Refinement__  
  Action refinement allows you to build hierarchy into your scenarios. The `:IN:` and `:OUT:` expressions are only conditions (checks), but the `:IN:` and `:OUT:` expressions are different. If for any step the `:OUT:` expression is reached for evaluation, but fails, this signals the need for refinement. A single full scenario can be inserted if all conditions match at the current position and the pending `:OUT:` conditions are satisfied after insertion.

Finally, to run your scenarios model-based, import `robotmbt` as a library and use the __Treat this test suite model-based__ keyword as suite setup. You are now ready to run your modelled test suite.
```
*** Settings ***
Suite Setup       Treat this test suite model-based
Library           robotmbt
```

Please note that this library is in a premature state and hasn't reached its first official release yet. Developments are ongoing within the context of the [TiCToC](https://tictoc.cs.ru.nl/) research project. Interface changes are still frequent and no deprecation warnings are being issued yet.
