# PAWS Deployment Web Server

This repository contains the CGI code and other content for the VPN webserver for the [PAWS project](http://publicaccesswifi.org).

The PAWS Web Server delivers client sign­up pages, client app configuration information and client administration.

Scripting is mainly in Perl (.cgi files), with HTML and some usage of PHP i.e. a handler script for Twilio SMS responses and also the Stats.php page to display live PAWS router information. 
 
Web content can be found in three directories: 
/var/www/html/ 
/var/www/secure­html/ 
/var/www/secure­cgi/
 
/var/www/html/ contains SSL secured content. Both of the other two locations are SSL secured.
  
In addition, there are three ways in which FreeRadius/the mySQL user database is used to authenticate access to web content: 
 
1. Access to some files in /var/www/secure­-cgi/ is permitted without authentication 
(consent.cgi and signup_user.cgi), but in order to access edit_details.cgi, a user must sign­in 
to the form at edit_details_login.cgi, using their PAWS credentials. The credentials are 
passed to edit_details.cgi, which then manually checks for a username and password match 
in the mySQL ‘radcheck’ table. So, this is a direct check of the database, rather than 
requesting authentication from FreeRadius. The reasons for this are historical and long 
forgotten...  

2. Access to the entire directory ‘vpn’ requires FreeRadius authentication. This is where the 
script ‘instructions.cgi’ provides users with client configuration information. The requirement 
for FreeRadius authentication is in: /var/www/secure-cgi/vpn/.htaccess. 
 
3. Access to the entire directory ‘adm’ and is limited to the PAWS users listed in: 
/var/www/secure­cgi/adm/.htaccess. 
 
A use­case flow for the web content is: 
 
Unregistered first­-time user goes to: http://vpn.publicaccesswifi.org/ or https://vpn.publicaccesswifi.org (secure).
Both of these URL's redirect the browser to the main splash page at https://vpn.publicaccesswifi.org/secure-cgi/index.cgi. The index.cgi page has logic in to detect the device that is being used and it will display an appropriate message.

Currently the following devices are supported:
Android 4.x phones and tablets. Apple IOS 6+ devices (iPhone and iPad) and Mac OSX. Windows XP/Vista/7/8 (32 or 64­bit) desktop PCs & laptops.

Windows Phone 7.x & 8.x and Blackberry devices are NOT supported. 

User clicks ‘If you are not a registered PAWS user, then click here to sign up‘. 
User is sent to: https://vpn.publicaccesswifi.org/secure­cgi/consent.cgi  
Users completes consent, clicks ‘Continue’ and is forwarded to self­signup page: 
https://vpn.publicaccesswifi.org/secure­cgi/signup_user.cgi 

After user is verified, they are sent back to: https://vpn.publicaccesswifi.org. From 
now on, all returns to home page are to HTTPS secure version.  
User goes to: https://vpn.publicaccesswifi.org/secure­cgi/vpn/instructions.cgi to set 
up device. Will be prompted for PAWS credentials, which are authenticated by 
FreeRadius.

After the user’s device is configured, they should now be able to access OpenVPN via 
a PAWS box. Note: in theory, users can also access the PAWS VPN from anywhere 
with Internet access (home ADSL etc), but other than hiding IP address, it is unlikely 
they would be motivated to do this.  
 
On subsequent visits to the website, users can modify their user details, password etc via 
the https://vpn.publicaccesswifi.org/secure­cgi/edit_details_login.cgi (which is manually 
authenticated against the user database, rather than via FreeRadius).  
How the sign-up process works
 
In: https://vpn.publicaccesswifi.org/secure­cgi/signup_user.cgi 
 
1. Collect user info. 
2. Create a random code to use for verification (invisible to user).  
3. Add entry to 'radpawsusers' containing all user info. 
4. Add entry to 'radcheck' with username, and attribute = 'Auth­Type', op =":=" and value = "Reject". This is what stops user connecting, until removed.  
 
5. Add entry to 'radcheck' with attribute ='Password', op ='==' and value = $password. 
This is all ready to go, once the other 'Auth­Type:=Reject" above entry is removed from this 
table.  
 
6. Add entry to 'temp_user', with $username, $lastname, $postcode, $code. 
Note: $username field is called 'fname', but contains username! 
 
7. Send 'User Self­Sign­Up: New account added' email to admins. 
 
8. Send verification text to user with link (which includes $username and $code as URL arguments). This happens via Twilio. 
 
9. User clicks link in text and is sent back to:
https://vpn.publicaccesswifi.org/secure­cgi/signup_user.cgi?username=$username&code=$
code 
 
10. signup_user.cgi uses $code to look for a match in 'temp_user', 
If match found, $username is retrieved from 'temp_user'. 
Note: not sure why this is necessary...$username has already been received in URL! 
Maybe it was decided safer to just use $code to make sure $username is correct? 
In which case, sending $username in URL argument is redundant.  
 
11. Look for entry in 'radcheck' WHERE username = $username AND attribute = 'Auth­Type'". If found, delete this entry. 
 
User is now verified and should be able to connect to the VPN. 

The remote web interface for client administration:

Admin gateway: 
https://vpn.publicaccesswifi.org/admin.html 
 
Create User ­ cu.cgi 
https://vpn.publicaccesswifi.org/secure­cgi/adm/cu.cgi 
 
List users ­ lu.cgi 
https://vpn.publicaccesswifi.org/secure­cgi/adm/lu.cgi 
 
Other helper admin scripts: 
 
eu.cgi 
Edit user ­ called by lu.cgi or with URL argument 
https://vpn.publicaccesswifi.org/secure­cgi/adm/eu.cgi?un=<username> 
 
du.cgi 
Delete user ­ called by lu.cgi or with URL argument 
https://vpn.publicaccesswifi.org/secure­cgi/adm/du.cgi?username=ElizabethMiller&delete=yes 

Client apps for connecting to OpenVPN are downloaded by the user. The device setup instructions point them to the appropriate client: 

Android: OpenVPN Connect App (link to Google Play store provided)
iOS: OpenVPN Connect app (Lonk to Apple app store provided) 
Windows: TunXten (Hosted on server at /var/www/html/opvpn_client_apps/)
Mac: Tunnelblick (Hoste on server at /var/www/html/opvpn_client_apps/)

The OpenVPN Client Configuration File is downloaded during device configuration at: /var/www/html/opvpn_client_conf:
paws.ovpn 
paws.mobileconfig (for iOS devices)
 
There is an .htaccess file in this directory that forces a browser to download files, rather than display. 


 



