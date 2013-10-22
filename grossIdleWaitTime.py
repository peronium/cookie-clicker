# Filename : cookieclicker.py
# INFO : Calculates gross idle wait time to next achievement.

""" 
TODO: 
- %s formatted output
- single report, flexible input
- format large/specific numbers
- read directly from game stats?
"""

########################
# FUNCTION DEFINITIONS #
########################

# Comprehensive time conversion
def timeReport(seconds):
	minutes = int(seconds) / 60
	hours = float(seconds) / 3600
	days = float(seconds) / 86400
	if minutes < 1:
		print seconds, "secs",
	elif minutes < 5:
		print minutes, "mins\t(", seconds, "seconds )",
	elif days < 1.5:
		print minutes, "mins\t(", hours, "hours )",
	else:
		print int(hours), "hours\t(", days, "DAYS )",
	return ""

# Summarize status and wait time
def cookieReport(INFLATION, CPS, CURRENT_STOCK, TARGET_QUOTA, targetFunds, BUILDING):

	# Current Status
	if TARGET_QUOTA != 1:
		print "Item:\t", BUILDING
		print "Have:\t", CURRENT_STOCK
		print "Need:\t", TARGET_QUOTA, "(", TARGET_QUOTA - CURRENT_STOCK, "more )"
	
	# Ouput cookies to goal (assume inBank = 0)
	i = 0 # buildings to quota
	cookiesToQuota = 0
	while i < (TARGET_QUOTA - CURRENT_STOCK):
		cookiesToQuota = cookiesToQuota + targetFunds * (INFLATION ** i)
		i = i + 1
	if TARGET_QUOTA - CURRENT_STOCK > 1:
		print "Next item cost: \t", targetFunds
		print "Cumulative cost:\t", long(cookiesToQuota), "(", cookiesToQuota, ")"
	
	# Output corresponding idle wait time
	grossTime = targetFunds / CPS
	print "Minutes for next purchase:\t", timeReport(grossTime)
	if TARGET_QUOTA - CURRENT_STOCK > 1:
		grossTime = cookiesToQuota / CPS
		print "Minutes for target quota:\t", timeReport(grossTime)

##################
# INITIALIZATION #
##################

# Constants
BASE_COST = {'CURSOR':15, 'GRANDMA':100, 'FARM':500, 'FACTORY':300, 'MINE':10000, 'SHIPMENT':40000, 'ALCHEMY':200000, 'PORTAL':1666666, 'TIME_MACHINE':123456789, 'ANTIMATTER':3999999999}
INFLATION = 1.15 # building price increase ratio 

# Input 
CPS = 5705693990.7 # cookies per second
BUILDING = 'grandma'.upper() # BASE_COST key
CURRENT_STOCK = 150 # Minimum: 0
TARGET_QUOTA = 200 # Minimum: 1

########
# MAIN #
########

print "INFO: Calculates gross idle wait time to next achievement."
print "Cookies per second:\t", CPS, "\n"

# Long-term calculation - building accumulator
targetFunds = long(BASE_COST[BUILDING] * INFLATION ** CURRENT_STOCK) # cost of next building upgrade
cookieReport(INFLATION, CPS, CURRENT_STOCK, TARGET_QUOTA, targetFunds, BUILDING)
print ""

# Optional calculation - single target
try:
	targetFunds = int(raw_input("Enter target cookies: \t"))
	cookieReport(1, CPS, 0, 1, targetFunds, None)
except ValueError:
	print "Invalid input; exiting program."
except KeyboardInterrupt:
	print None
