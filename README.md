# Cloudflare Keepalived


## Description
A script that will compare a list of IP's to the users cloudflare IP's. The script will ping each ip in the ip_list variable, if it cannot ping it will remove the IP from cloudflare and send an email to user. If the script can ping the IP and the IP doesn't exist in cloudflare then it will add the ip and email the user.

Can run on Linux or Windows as a cronjob or task.

## Requirements
Cloudflare account
Sendmail account (Optional)
Python >= 2.7.12
Python requests module (pip install requests)
Python os module (pip install os)

##Notes
If sendmail is not required, simply comment out the 2 send_mail calls towards the end of the script.