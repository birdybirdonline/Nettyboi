#!/usr/bin/python
from os  import system as term
from subprocess import run, DEVNULL
from re import sub, IGNORECASE
import pandas as pd

# run netstat and translate its output using awk to parse for csv
term("sudo netstat -Watuvep | awk '{print  $1\",\",$2\",\",$3\",\",$4\",\",$5\",\",$6\",\",$7\",\",$8\",\",$9}'> nettycache.csv")


# read log csv into dataframe and replace header names with more readable ones
df = pd.read_csv("nettycache.csv", header=1, names=['prot', 'recv', 'send', 'loc_add', 'remote_add', 'state', 'usr', 'inode', 'program'])
# remove rows related to local connections only
sort_df = df[~df['remote_add'].str.contains("local|0.0.0.0:\*|\[::\]:\*|_gateway:bootps")].sort_values(['recv','program','usr','remote_add', 'state', 'remote_add', 'loc_add', 'send'], ascending=False)

# get the list of remote addresses
remote_adds = sort_df.remote_add

# instantiate resolver list to feed into the  df later
# and an investigation list for checking unresolved manually at the end
resolved = []
investigate = []

# for each remote address, run dig to ensure we're working with an IP rather than a subdomain etc
for addr in remote_adds:
    # strip the port ref if https
    addr = addr.replace(":https", '')

    # run dig +short on the address
    dig = run(f'dig {addr} +short', shell=True, capture_output=True)

    # maybe has more than one line. we only need the first line
    digsplit = str(dig.stdout).split('\\')
    # stdout will have bullshit to remove
    dug = sub(r"[b']", '', digsplit[0])

    # run whois against the sanitized dig output
    who = run(f'whois {dug}', shell=True, capture_output=True)

    # grep the netname from the whois output (case insensitive)
    netn = run(f"grep -i netname", shell=True, input=who.stdout, capture_output=True)

    # sanitize the netname result to be more readable in our dataframe
    name = sub(r"[b': ]|\W*(\\n)\W*|\W*(NetName)\W*|", '', str(netn.stdout), flags=IGNORECASE)
    resolved.append(name)

    # check  to make sure there was meaningful output for the resolved name. If not,
    # add it to a list to print later for manual investigation
    if len(name) < 2:
        investigate.append(addr)

# insert all the resolved names into a new column in the df
sort_df.insert(5, "Remote_Add_Resolved", resolved, True)

# get all add
# print it out baby (set pd options so that it never truncates)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
print(sort_df)
print("Unresolved Remote Addresses to investigate manually:")
for i, addr in enumerate(investigate):
    print(f'{i+1}. {addr}')
    
    
