# Filename:     grossIdleWaitTime.py
# Repository:   cookie-clicker
# Creator:      peronium
# Summary:      Calculates gross idle wait time to next achievement.

# TODO: order dict keys in ouput
# TODO: format/align numbers
# TODO: refactor for speed
# TODO: read directly from game stats?

import sys

"""
FUNCTION DEFINITIONS
"""

# Called upon KeyboardInterrupt or "Exit" input
def handleExit():
   print "\nExiting..."
   sys.exit(1)

# Comprehensive time conversion
def timeReport(seconds, PRECISION):
    days = round(seconds / 86400.0, PRECISION)
    hours = round(seconds / 3600.0, PRECISION)
    minutes = round(seconds / 60.0, PRECISION)
    seconds = round(seconds, PRECISION)
    if minutes < 1:
        print "%r secs" % seconds,
    elif minutes < 5:
        print "%r mins\t(%r seconds)" % (minutes, seconds),
    elif days < 1.5:
        print "%r mins\t(%r hours)" % (minutes, hours),
    else:
        print "%r hours\t(%r DAYS)" % (hours, days),
    return "\n"


"""
CONSTANTS
"""
 
BASE_COST = {
    'CURSOR':15,
    'GRANDMA':100,
    'FARM':500,
    'FACTORY':300,
    'MINE':10000,
    'SHIPMENT':40000,
    'ALCHEMY':200000,
    'PORTAL':1666666,
    'TIMEMACHINE':123456789,
    'ANTIMATTER':3999999999}
INFLATION = 1.15 # building price increase ratio
PRECISION = 2 # rounding precision

cps = 7461297260.1 # cookies per second
# Technically not constant - can be overwritten in runtime


"""
MAIN
"""

print "INFO: Calculates gross idle wait time to next achievement.\n"
print "Cookies per second:\t%r\t(Type \"Edit CpS\" to change.)" % cps

building = "" # BASE_COST dict key
while building.upper() not in BASE_COST:

    # Case: numerical (cookie) input
    try: 
        target = raw_input("Enter target:\t")
        targetCookies = long(target)
        building = None
        currentStock = 0
        targetStock = 1
        break

    # Case: word (building) input   
    except ValueError:

        # Exit prompt
        if target.lower() == "exit":
            handleExit()

        # Edit CpS prompt
        elif target.lower() == "edit cps":
            while True:
                try:
                    cps = float(raw_input("Enter new CpS: "))
                    break
                except ValueError:
                    print "Invalid input.",
                except KeyboardInterrupt:
                    print "Cancelling edit..."
                    break

        # Building input
        else:
            try: 
                building = target.upper()
                targetCookies = BASE_COST[building]
            except KeyError:
                print "Invalid building name. Try one of the following:\n", BASE_COST.keys(),
                print "OR type \"Edit CpS\" or \"Exit\"."

    except KeyboardInterrupt:
        handleExit()

# Determine target cookies wrt building upgrade(s)
if isinstance(building, str): # Building entered, not cookies
    while True:
        try:
            currentStock = int(raw_input("\tHave:\t"))
            targetStock = int(raw_input("\tNeed:\t"))
            if targetStock > currentStock: # inputs are valid
                break
            else:
                print ("\"Need\" value must be greater than \"Have\" value. "
                    "Please try again.")
        except ValueError:
            print "Invalid input. Please try again."
        except KeyboardInterrupt:
            handleExit()
    print "\t\t(%d more)" % (targetStock - currentStock)
    targetCookies = long(BASE_COST[building] * INFLATION ** currentStock)


# Calculate gross cost (assume inBank = 0)
i = 0 # buildings to quota
cookiesToQuota = 0
while i < (targetStock - currentStock):
    cookiesToQuota = cookiesToQuota + targetCookies * (INFLATION ** i)
    i = i + 1
print "Next item cost: \t%d" % targetCookies
if targetStock - currentStock > 1:
    print "Cumulative cost:\t%d" % long(cookiesToQuota)

# Calculate gross idle wait time
grossTime = targetCookies / cps
print "Minutes for next purchase:\t", timeReport(grossTime, PRECISION),
if targetStock - currentStock > 1:
    grossTime = cookiesToQuota / cps
    print "Minutes for target quota:\t", timeReport(grossTime, PRECISION)
