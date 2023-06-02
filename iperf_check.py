# ======================================================
# Name: iperf_check.py
# Date: 2023-05-28_2200
# Description: iperf3 to csv script
# Tested on: Ubuntu Server 22.04.2 LTS
# ======================================================
# Install Prereqs - 'apt install python3 iperf3 pip'
# Install iPerf3 Python Wrapper - 'pip install iperf3'
# ======================================================

# import modules
import datetime
import iperf3
import csv
import os
import sys

# set variables
# remote iperf3 server
remote_site = sys.argv[1]
# iperf3 port to use
test_port = sys.argv[2]
# length of iperf3 test in seconds
test_duration = 20

# set iperf3 client options
# run 10 parallel streams for duration w/ reverse
client = iperf3.Client()
client.server_hostname = remote_site
client.zerocopy = True
client.verbose = False
client.reverse = True
client.port = test_port
client.num_streams = 10
client.duration = int(test_duration)
client.bandwidth = 1000000000

# run iperf3 test
result = client.run()

# prepare data for error log
result_date = datetime.datetime.now().strftime('%Y-%m-%d')
result_time = datetime.datetime.now().strftime('%H:%M:%S')
result_error = result.error
result_log = f'{result_date},{result_time},{result_error}'

# write data to error log
with open('/home/ubuntu/logs/iperf_error.log', 'a') as f:
    print(result_log, file=f)

# extract data from results
sent_mbps = int(result.sent_Mbps)
received_mbps = int(result.received_Mbps)

# prepare data for CSV
data = [
    [result_date, result_time, remote_site, test_port, sent_mbps, received_mbps]
]

# define CSV file path
csv_file = '/home/ubuntu/logs/iperf_results.csv'

# check if the CSV file exists
file_exists = os.path.isfile(csv_file)

# write data to CSV
with open(csv_file, 'a', newline='') as file:
    writer = csv.writer(file)

    # write header row if the file is being created for the first time
    if not file_exists:
        writer.writerow(['result_date','result_time','remote_site','test_port','sent_mbps','received_mbps'])

    # write data rows
    writer.writerows(data)