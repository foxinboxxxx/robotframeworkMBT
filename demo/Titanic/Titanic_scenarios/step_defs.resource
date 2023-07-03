*** Settings ***
Library           robotnl
Resource          ../domain_lib/Titanic.resource

*** Keywords ***
Titanic is scheduled for the voyage to New York
    Spawn titanic at location Southampton
    Log    Dear crew, your ship has been assigned to the trip to New York. You are due for departure from the port of Southampton at noon on 1912-04-10.
    Start Journey on 1912-04-10
    #Titanic is docked in the port of ${port}
    # \ \ \ Check that \ \ \ Map area where 'Titanic's position' is located \ \ \ Equals \ \ \ ${port}
    # \ \ \ Check that \ \ \ Titanic's speed \ \ \ equals \ \ \ 0

Titanic is docked in the port of Southampton
    Check that    Map area where 'Titanic's position' is located    Equals    Southampton
    Check that    Titanic's speed    equals    0

Titanic is docked in the port of Cherbourg
    Check that    Map area where 'Titanic's position' is located    Equals    Cherbourg
    Check that    Titanic's speed    equals    0

Titanic is docked in the port of Queenstown
    Check that Map area where 'Titanic's position' is located Equals Queenstown
    Check that Titanic's speed equals 0
    #Titanic sails from ${port A} to ${port B}
    # \ \ \ Check that \ \ \ Map area where 'Titanic's position' is located \ \ \ Equals \ \ \ ${port B}
    # \ \ \ log \ \ \ Completed the leg from ${port A} to ${port B}

Titanic sails from Southampton to New York
    Titanic sails from Southampton to Cherbourg
    Titanic sails from Cherbourg to Queenstown
    Titanic sails from Queenstown to New York

Titanic sails from Southampton to Cherbourg
    Titanic departs for the port of Cherbourg
    Check that    Map area where 'Titanic's position' is located    Equals    Cherbourg
    log    Completed the leg from Southampton to Cherbourg

Titanic sails from Cherbourg to Queenstown
    Check that    Map area where 'Titanic's position' is located    Equals    Queenstown
    log    Completed the leg from Cherbourg to Queenstown

Titanic sails from Queenstown to New York
    Check that    Map area where 'Titanic's position' is located    Equals    New York
    log    Completed the leg from Queenstown to New York
    #Titanic departs for the port of ${port}
    #Point titanic towards location ${port}
    #Titanic moves full speed ahead
    #Move Titanic out of current area

Titanic departs for the port of Cherbourg
    Point titanic towards location Cherbourg
    Titanic moves full speed ahead
    Move Titanic out of current area

Titanic departs for the port of Queenstown
    Point titanic towards location Queenstown
    Titanic moves full speed ahead
    Move Titanic out of current area

Titanic departs for the port of New York
    Point titanic towards location New York
    Titanic moves full speed ahead
    Move Titanic out of current area
    #Titanic arrives in the port of ${port}
    #Check that    Map area where 'Titanic's position' is located    Equals    ${port}
    #Titanic stops

Titanic arrives in the port of Cherbourg
    Check that    Map area where 'Titanic's position' is located    Equals    Cherbourg
    Titanic stops

Titanic arrives in the port of Queenstown
    Check that    Map area where 'Titanic's position' is located    Equals    Queenstown
    Titanic stops

Titanic arrives in the port of New York
    Check that    Map area where 'Titanic's position' is located    Equals    New York
    Titanic stops

Titanic crosses area ${area}
    Check that    Map area where 'Titanic's position' is located    Equals    ${area}
    Check that    Titanic's speed    Is Greater Than    0
    Move Titanic out of current area

Titanic crosses area ${area}
    Check that    Map area where 'Titanic's position' is located    Equals    ${area}
    Check that    Titanic's speed    Is Greater Than    0
    Move Titanic out of current area

Titanic sails the Atlantic
    log    Aahh, the fresh air of the open sea!
    Move Titanic out of current area

Titanic crosses Iceberg alley
    Check that    Map area where 'Titanic's position' is located    Equals    Atlantic ocean

Titanic is sailing Iceberg alley
    Check that    Map area where 'Titanic's position' is located    Equals    Iceberg alley
    Log    Brrr, that's a bit chilly

Titanic barely misses a huge iceberg
    Spawn iceberg at coordinate longitude 45.7500 latitude -44.0700
    Move Titanic out of current area
    Log    Pfew! That was close!

Titanic hits a huge iceberg
    Spawn iceberg at coordinate longitude 45.6119 latitude -45.0011
    log    Iceberg, right ahead!
    Move Titanic out of current area

Titanic continues on its voyage
    Check that    Titanic's speed    Is Greater Than    0

Titanic starts to sink
    Check that    Map area where 'Titanic's position' is located    Equals    Iceberg alley
    Check that    Titanic's speed    equals    0

Titanic's voyage is complete
    log    Dear passengers, this is the final destination of this journey. Please remember to collect all your personal belongings when disembarking.

the date is ${date}
    Check that    Current date of Journey    equals    ${date}
