# Filename : grossIdleWaitTime.py
# Repository : cookie-clicker
# INFO : Calculates gross idle wait time to next achievement.

# TODO: change CPS in prompt
# TODO: order keys in ouput
# TODO: fix rounding: precision; format large/specific numbers
# TODO: improve runtime speed
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
def timeReport(seconds, PRECISION):
    minutes = round(seconds / 60.0, PRECISION)
    hours = round(seconds / 3600.0, PRECISION)
    days = round(seconds / 86400.0, PRECISION)
    if minutes < 1:
        print "%d secs" % seconds,
    elif minutes < 5:
        print "%d mins\t(%d seconds)" % (minutes, seconds),
    elif days < 1.5:
        print "%d mins\t(%d hours)" % (minutes, hours),
    else:
        print "%d hours\t(%d DAYS)" % (hours, days),
    return "\n"

# Summarize status and wait time
def cookieReport(INFLATION, PRECISION, CPS, currentStock, targetStock, targetCookies):

    # Ouput cookies to goal (assume inBank = 0)
    i = 0 # buildings to quota
    cookiesToQuota = 0
    while i < (targetStock - currentStock):
        cookiesToQuota = cookiesToQuota + targetCookies * (INFLATION ** i)
        i = i + 1
    if targetStock - currentStock > 1:
        print "Next item cost: \t%d" % targetCookies
        print "Cumulative cost:\t%d (%d)" % (long(cookiesToQuota), int(cookiesToQuota))
    
    # Output corresponding idle wait time
    grossTime = targetCookies / CPS
    print "Minutes for next purchase:\t", timeReport(grossTime, PRECISION),
    if targetStock - currentStock > 1:
        grossTime = cookiesToQuota / CPS
        print "Minutes for target quota:\t", timeReport(grossTime, PRECISION)

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
PRECISION = 2 # rounding precision

CPS = 5705693990.7 # cookies per second

building = "" # BASE_COST key

"""
MAIN
"""

print "INFO: Calculates gross idle wait time to next achievement.\n"
print "Cookies per second:\t%d" % CPS

while building.upper() not in BASE_COST:
   try: # Case: cookie (numerical) input
      target = raw_input("Enter target:\t")
      targetCookies = long(target)
      building = None
      currentStock = 0
      targetStock = 1
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
   while True:
      try:
         currentStock = int(raw_input("Have: "))
         targetStock = int(raw_input("Need: "))
         if targetStock > currentStock: # inputs are valid
            break
         else:
            print "\"Need\" value must be greater than \"Have\" value. Please try again."
      except ValueError:
         print "Invalid input. Please try again."
      except KeyboardInterrupt:
         handleExit()
   print "(%d more)\n" % (targetStock - currentStock)
   targetCookies = long(BASE_COST[building] * INFLATION ** currentStock) # cost of next building upgrade

cookieReport(INFLATION, PRECISION, CPS, currentStock, targetStock, targetCookies) 
