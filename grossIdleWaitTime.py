# Filename : grossIdleWaitTime.py
# Repository : cookie-clicker
# INFO : Calculates gross idle wait time to next achievement.

# TODO: single report, flexible input
# TODO: format large/specific numbers
# TODO: read directly from game stats?

"""
FUNCTION DEFINITIONS
"""

# Comprehensive time conversion
def timeReport(seconds):
    minutes = round(seconds / 60.0, 3)
    hours = round(seconds / 3600.0, 3)
    days = round(seconds / 86400.0, 3)
    if minutes < 1:
        print "%d secs" % seconds,
    elif minutes < 5:
        print "%d mins\t(%d seconds)" % (minutes, seconds),
    elif days < 1.5:
        print "%d mins\t(%d hours)" % (minutes, hours),
    else:
        print "%d hours\t(%d DAYS)" % (hours, days),
    return ""

# Summarize status and wait time
def cookieReport(INFLATION, CPS, CURRENT_STOCK, TARGET_QUOTA, targetCookies, BUILDING):

    # Current Status
    if TARGET_QUOTA != 1:
        print "Item:\t%s" % BUILDING
        print "Have:\t%d" % CURRENT_STOCK
        print "Need:\t%d (%d more)" % (TARGET_QUOTA, (TARGET_QUOTA - CURRENT_STOCK))
    
    # Ouput cookies to goal (assume inBank = 0)
    i = 0 # buildings to quota
    cookiesToQuota = 0
    while i < (TARGET_QUOTA - CURRENT_STOCK):
        cookiesToQuota = cookiesToQuota + targetCookies * (INFLATION ** i)
        i = i + 1
    if TARGET_QUOTA - CURRENT_STOCK > 1:
        print "Next item cost: \t%d" % targetCookies
        print "Cumulative cost:\t%d (%d)" % (long(cookiesToQuota), int(cookiesToQuota))
    
    # Output corresponding idle wait time
    grossTime = targetCookies / CPS
    print "Minutes for next purchase:\t", timeReport(grossTime)
    if TARGET_QUOTA - CURRENT_STOCK > 1:
        grossTime = cookiesToQuota / CPS
        print "Minutes for target quota:\t", timeReport(grossTime)

"""
INITIALIZATION
"""

# Constants
BASE_COST = {
    'CURSOR':15,
    'GRANDMA':100,
    'FARM':500,
    'FACTORY':300,
    'MINE':10000,
    'SHIPMENT':40000,
    'ALCHEMY':200000,
    'PORTAL':1666666,
    'TIME_MACHINE':123456789,
    'ANTIMATTER':3999999999}
INFLATION = 1.15 # building price increase ratio

# Input
CPS = 5705693990.7 # cookies per second
BUILDING = 'grandma'.upper() # BASE_COST key
CURRENT_STOCK = 150 # Minimum: 0
TARGET_QUOTA = 200 # Minimum: 1

"""
MAIN
"""

print "INFO: Calculates gross idle wait time to next achievement."
print "Cookies per second:\t", CPS, "\n"

# Long-term calculation - building accumulator
targetCookies = long(BASE_COST[BUILDING] * INFLATION ** CURRENT_STOCK) # cost of next building upgrade
cookieReport(INFLATION, CPS, CURRENT_STOCK, TARGET_QUOTA, targetCookies, BUILDING)
print ""

# Optional calculation - single target
try:
    targetCookies = int(raw_input("Enter target cookies: \t"))
    cookieReport(1, CPS, 0, 1, targetCookies, None)
except ValueError:
    print "Invalid input; exiting program."
except KeyboardInterrupt:
    print ""
