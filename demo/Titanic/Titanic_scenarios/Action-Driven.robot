*** Settings ***
Resource          ../domain_lib/Titanic.resource
Library           robotnl

*** Test Cases ***
Start journey
    Spawn titanic at location Southampton
    Log    Dear crew, your ship has been assigned to the trip to New York. You are due for departure from the port of Southampton at noon on 1912-04-10.

Southampton to Cherbourg
    Check that    Map area where 'Titanic's position' is located    Equals    Southampton
    Point titanic towards location Cherbourg
    Titanic moves full speed ahead
    Move Titanic out of current area
    Check that    Map area where 'Titanic's position' is located    Equals    the English Channel
    Check that    Titanic's speed    Is Greater Than    0
    Move Titanic out of current area
    Check that    Map area where 'Titanic's position' is located    Equals    Cherbourg
    Titanic stops

Cherbourg to Queenstown
    Check that    Map area where 'Titanic's position' is located    Equals    Cherbourg
    Point titanic towards location Queenstown
    Titanic moves full speed ahead
    Move Titanic out of current area
    Check that    Map area where 'Titanic's position' is located    Equals    the English Channel
    Check that    Titanic's speed    Is Greater Than    0
    Move Titanic out of current area
    Check that    Map area where 'Titanic's position' is located    Equals    Queenstown
    Titanic stops

Queenstown to New York miss Iceberg
    Check that    Map area where 'Titanic's position' is located    Equals    Queenstown
    Point titanic towards location New York
    Titanic moves full speed ahead
    Move Titanic out of current area
    Check that    Map area where 'Titanic's position' is located    Equals    Atlantic ocean
    Move Titanic out of current area
    Check that    Map area where 'Titanic's position' is located    Equals    Iceberg alley
    Move Titanic out of current area
    Check that    Map area where 'Titanic's position' is located    Equals    Atlantic ocean
    Spawn iceberg at coordinate longitude 45.7500 latitude -44.0700
    Move Titanic out of current area
    Log    Pfew! That was close!
    Check that    Titanic's speed    Is Greater Than    0
    Titanic stops

Queenstown to New York hits Iceberg
    Check that    Map area where 'Titanic's position' is located    Equals    Queenstown
    Point titanic towards location New York
    Titanic moves full speed ahead
    Move Titanic out of current area
    Check that    Map area where 'Titanic's position' is located    Equals    Atlantic ocean
    Move Titanic out of current area
    Spawn iceberg at coordinate longitude 45.6119 latitude -45.0011
    log    Iceberg, right ahead!
    Check that    Map area where 'Titanic's position' is located    Equals    Iceberg alley
    Check that    Titanic's speed    equals    0
