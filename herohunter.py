#! python3

import requests
import json
import csv

# keywords to search urlscan.io (follows query syntax found here: https://urlscan.io/search/#* under 'Help & Examples)
kw_list = ["hash:7E50E406688BD898803F653058D14CA384734CB9B39BA900BC5E2734B59C073B"]

# domains to ignore from results
whitelist = ["onedrive.live.com"]

# IPs associated with hits from keywords which will then be searched for connected domains
ip_list = [""]

# list of IDs for records in existing CSV list
id_list = []


def search(query):
    '''
    searches urlscan.io with provided query and creates record of pertinent info of results
    '''
    new_records = 0

    # open CSV for updating later on in this function
    with open("hits.csv", 'a+', newline='') as updated_hits:
        fieldnames = ['submit_date', 'domain', 'url', 'ip', 'asn', 'ptr', 'city', 'country', 'server', 'source', 'id']
        writer = csv.DictWriter(updated_hits, fieldnames=fieldnames)

        for item in query:
            print("\n")
            print("Searching for {0}...".format(item))
            resp = requests.get('https://urlscan.io/api/v1/search/?q={0}'.format(item))
            data = json.loads(resp.text)

            # iterate through JSON for pertinent info
            for results in data["results"]:
                submit_date = results["task"]["time"]
                domain = results["page"]["domain"]
                url = results["page"]["url"]
                ip = results["page"]["ip"]
                asn = results["page"]["asn"]
                ptr = results["page"]["ptr"]
                city = results["page"]["city"]
                country = results["page"]["country"]
                server = results["page"]["server"]
                source = results["task"]["source"]
                id = results["_id"]

                # remove leading www. from domain
                if domain.startswith("www."):
                    domain = domain.replace("www.", "")

                # check domain against whitelist and prevent against duplicate records
                if domain not in whitelist and id not in id_list:

                    # write row of link details to CSV
                    writer.writerow(
                        {'submit_date': submit_date, 'domain': domain, 'url': url, 'ip': ip, 'asn': asn, 'ptr': ptr, 'city': city, 'country': country, 'server': server, 'source': source, 'id': id})

                    # keep count of new records added to existing hits
                    new_records += 1

                    # add associated IP to ip_list for searching/pivoting
                    if ip not in ip_list:
                        ip_list.append(ip)
    print("New records appended: {0}".format(new_records))


def get_history():
    '''
    read in the existing CSV and enumerate all IDs and add to a list.
    '''
    try:
        with open('hits.csv', 'r') as past_hits:
            reader = csv.DictReader(past_hits)

            for row in reader:
                id_list.append(row['id'])

    except FileNotFoundError:
        print("No existing CSV of hits")
        with open('hits.csv', 'w', newline='') as new_csv:
            fieldnames = ['submit_date', 'domain', 'url', 'ip', 'asn', 'ptr', 'city', 'country', 'server', 'source', 'id']
            writer = csv.DictWriter(new_csv, fieldnames=fieldnames)
            writer.writeheader()


def main():
    get_history()
    search(kw_list)
    search(ip_list)

    # print(ip_list)
    # print(len(ip_list))

if __name__ == '__main__':
    main()

