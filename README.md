# Cloudflare Keepalived

## Description
A script that will compare a list of IP's to the users cloudflare IP's. The script will ping each ip in the ip_list variable, if it cannot ping it will remove the IP from cloudflare and send an email to user. If the script can ping the IP and the IP doesn't exist in cloudflare then it will add the ip and email the user.

## Requirements
* Cloudflare account
* Sendmail account (Optional)
* Python >= 2.7.12
* Python requests module (pip install requests)
* Python os module (pip install os)

## Example
Fill in the variables at the top of the script (See notes about sendmail):

```
cloudflare_api_key = ''
cloudflare_email = ''
cloudflare_domain = ''
cloudflare_zone_id = ''

sendmail_api_key = ''
sendmail_mail_to = ''
sendmail_mail_from = ''

ip_list = ['1.1.1.1','2.2.2.2','3.3.3.3']
```

* To get the cloudflare zone id, simply login to cloudflare and copy the Zone ID from the Domain Summary.
* The ip list is the pool of server IP's

If on Linux:
```
crontab -e
```

Then add something like this to the crontab:
```
* * * * * python cloudflare_keepalive.py
```

## Notes
* If sendmail is not required, simply comment out the 2 send_mail calls towards the end of the script.
* This script should work on Linux or Windows as a cronjob or task.