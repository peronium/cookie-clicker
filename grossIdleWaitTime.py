# Filename : grossIdleWaitTime.py
# Repository : cookie-clicker
# INFO : Calculates gross idle wait time to next achievement.

# TODO: improve runtime speed
# TODO: format large/specific numbers; rounding
# TODO: read directly from game stats?

import sys

"""
FUNCTION DEFINITIONS
"""

# Called upon KeyboardInterrupt or "Exit" input
def handleExit():
   print "Exiting."
   sys.exit(1)

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
def cookieReport(INFLATION, CPS, currentStock, targetQuota, targetCookies, building):

    # Ouput cookies to goal (assume inBank = 0)
    i = 0 # buildings to quota
    cookiesToQuota = 0
    while i < (targetQuota - currentStock):
        cookiesToQuota = cookiesToQuota + targetCookies * (INFLATION ** i)
        i = i + 1
    if targetQuota - currentStock > 1:
        print "Next item cost: \t%d" % targetCookies
        print "Cumulative cost:\t%d (%d)" % (long(cookiesToQuota), int(cookiesToQuota))
    
    # Output corresponding idle wait time
    grossTime = targetCookies / CPS
    print "Minutes for next purchase:\t", timeReport(grossTime)
    if targetQuota - currentStock > 1:
        grossTime = cookiesToQuota / CPS
        print "Minutes for target quota:\t", timeReport(grossTime)
    return ""

"""
INITIALIZATION
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

CPS = 5705693990.7 # cookies per second

building = "" # BASE_COST key

"""
MAIN
"""

print "INFO: Calculates gross idle wait time to next achievement."
print "Cookies per second:\t%d\n" % CPS

while building.upper() not in BASE_COST:
   try: # Case: cookie (numerical) input
      target = raw_input("Enter target:\t")
      targetCookies = long(target)
      building = None
      currentStock = 0
      targetQuota = 1
      break
   except ValueError: # Case: building (string) input
      if target.lower() == "exit":
         handleExit()
      else:
         try: 
            building = target.upper()
            targetCookies = BASE_COST[building]
         except KeyError:
            print "Invalid building name. Try one of the following:\n", BASE_COST.keys()
   except KeyboardInterrupt:
      handleExit()
if isinstance(building, str): # Building entered, not cookies
   currentStock = int(raw_input("Have:\t",))
   targetQuota = int(raw_input("Need:\t",))
   print "(%d more)\n" % (targetQuota - currentStock)
   targetCookies = long(BASE_COST[building] * INFLATION ** currentStock) # cost of next building upgrade

cookieReport(INFLATION, CPS, currentStock, targetQuota, targetCookies, building) 
