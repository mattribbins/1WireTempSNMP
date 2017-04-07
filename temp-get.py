# 1-Wire Temperature Sensor parser
#
# Author: mribbins
# Description: Retrieves a temperature value from a 1-Wire device and returns
#              a temperature value in celsius*1000.
# Args: -h - Help
#       -i/--uid - 1-Wire sensor UID

import sys, getopt

# Get the UID
uid = "28-000000000000"
try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:", ["uid="])
except getopt.GetoptError:
    print "0.01"
    exit(1)
for opt, arg in opts:
    if opt == '-h':
        exit(1)
    # UID
    elif opt in ("-i", "--uid"):
        uid = "28-" + arg

# Open the probe data file
try:
    probe_file = open("/sys/bus/w1/devices/" + uid + "/w1_slave")
    probe_data = probe_file.read()
    probe_file.close()
except IOError:
    print "0.00"
    exit(2)
# Parse the data received
line = probe_data.split("\n")[1]
data = line.split(" ")[9]
temperature = float(data[2:])
#temperature = temperature / 1000

# Print temp in C*1000
print temperature
