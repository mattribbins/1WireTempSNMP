#!/usr/bin/python3
# 1-Wire Temperature Sensor poller
#
# Author: mribbins
# Description: Retrieves a temperature value from a 1-Wire device and returns
#              a temperature value in celsius*1000.
# Args: -h - Help
#       -i/--uid - 1-Wire sensor UID
#       -s       - Post Salvo ID

import os, sys, getopt, requests, smtplib, datetime
from email.mime.text import MIMEText

## Settings ##
threshold = 25.0
calibration = -1.0
get_url = "http://172.25.129.32:18513/VClock?Salvo="

send_from = "Bristol Studios <studios-bristol@bauermedia.co.uk>"
send_to = "radio.southengineers@bauermedia.co.uk"
smtp_server = "smtp.bauer-uk.bauermedia.group"

# Get the UID
uid = "28-000000000000"
salvo = "STUDIO_UNKNOWN"
try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:s:", ["uid="])
except getopt.GetoptError:
    print("0.01")
    exit(1)
for opt, arg in opts:
    if opt == '-h':
        exit(1)
    # UID
    elif opt in ("-i", "--uid"):
        uid = "28-" + arg
    elif opt in ("-s", "--salvo"):
        salvo = arg

# Open the probe data file
try:
    probe_file = open("/sys/bus/w1/devices/" + uid + "/w1_slave")
    probe_data = probe_file.read()
    probe_file.close()
except IOError:
    print("0.00")
    exit(2)
# Parse the data received
line = probe_data.split("\n")[1]
data = line.split(" ")[9]
temperature = float(data[2:])
temperature = temperature / 1000
temperature = temperature + calibration
print(str(temperature))

# Are we above the threshold?
if temperature > threshold:
    try:
        f = open("/tmp/" + salvo, "r")
        title = ''
    except FileNotFoundError:
        f = open("/tmp/" + salvo, "w")
        f.write(str(temperature))
        # New File
        title = 'Bristol Studio - Temperature Alarm ' + salvo
    finally:
        f.close()
else:
    try:
        f = open("/tmp/" + salvo, "r")
        f.close()
        os.remove("/tmp/" + salvo)
        title = 'Bristol Studio - Temperature Clear ' + salvo
    except IOError:
        title = ''
    except FileNotFoundError:
        title = ''
        # New File

if temperature > threshold:
    try:
        r = requests.get(get_url + salvo + '_TEMP_FAIL')
    except:
        print('Salvo Fail')
else:
    try:
        r = requests.get(get_url + salvo + '_TEMP_OK')
    except:
        print('Salvo Fail')

# Only send email if we have defined a title.
if title != '':
    print("Sending email...")
    # Compose
    body = "%s \r\n\r\n Since %s: \r\n %s" % (title, datetime.datetime.today().strftime("%d %B %Y %H:%M:%S"), str(temperature))
    print(body)
    msg = MIMEText(body)
    msg['Subject'] = title
    msg['From'] = send_from
    msg['To'] = send_to

    # Send the message via the SMTP server
    s = smtplib.SMTP(smtp_server)
    s.send_message(msg)
    s.quit()