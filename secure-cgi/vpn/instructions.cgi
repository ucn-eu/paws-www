#!/usr/bin/perl -wT


use strict;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser); 

print header;

=begin comment
PAWS2 rewrite by Steve North
2014
=end comment
=cut

print start_html(
        -title  =>      'PAWS VPN Instructions',
        -style  =>      {'src'  =>      '/styles/style.css'},
);
print img { src => "/images/pawshdrmid.png", align => "CENTER" };


my $agent;

$agent=$ENV{'HTTP_USER_AGENT'};

#########################

if ( $agent =~ /Android\s(\d)\.(\d)\.(\d)/ ) {
	my $android_v1 = $1;
	my $android_v2 = $2;
	my $android_v3 = $3;

	print("<H2>You appear to be using Android $android_v1.$android_v2.$android_v3</H2>");
	
	if($android_v1 > 3)
	{
	print_android_4();
	}
	else
	{
	print_android_2();
	}
}
elsif ( $agent =~ /\((iP\w+);/ ) {
	print("<H2>You appear to be using $1</H2>");
	print_iOS();
}
elsif ( $agent =~ /Macintosh;.*Mac (OS\s+X\s+\d+_\d+_\d+)/ ) {
	print("<H2>You appear to be using $1</H2>");
	print_apple();
}
elsif ( $agent =~ /Windows\sNT/ ) {
	print("<H2>You appear to be using Microsoft Windows</H2>");
	print_windows();
}
else {
	print_unknown();
}

#print_android_4();
#print_iOS();
#print_windows();
#print_apple();

#########################

print end_html;


#########################
sub intro_text {
print("There are 3 simple steps to get your device ready for connection to PAWS:");
print "<br>\n";
print("1. Get the app. 2. Get the PAWS file. 3. Show the app where the PAWS file is on your device.");
print "<br>\n";
}

#########################
sub print_android_2 {
	print "<br>\n";
	print "Sorry, this device is not supported for PAWS. Android 4.0+ required.\n";
	print "<br>\n";
}

#########################
sub print_android_4 {
intro_text();
print "<br>\n";
print "<B>Step 1.</B> Please click <a href=\"https://play.google.com/store/apps/details?id=net.openvpn.openvpn\">here</a> to get the app you will need to connect.";
print "<br>\n";
print "Now, once your app is installed...";
print "<br>\n";
print "<B>Step 2.</B> Click <a href=\"http://vpn.publicaccesswifi.org/opvpn_client_conf/paws.ovpn\">here</a> download a special PAWS setup file to get you connected";
print "<p>\n";
print "<B>Step 3.</B>Run the OpenVPN Connect app that you installed at Step 1. 
Press the list/menu button on the case of your phone. Touch 'Import'. Touch 'Import Profile from SD Card'. 
Browse to the location of 'paws.ovpn', which was downloaded at Step 2 (this should be in your browser's 'Downloads' folder, exact location dependent on browser). 
Select 'paws.ovpn'. Enter your PAWS username and password. Tick the 'save' box. Touch 'Connect'. <br>\n";
}

#########################
sub print_iOS {
intro_text();
print "<br>\n";
print "<B>Step 1.</B> Please click <a href=\"https://itunes.apple.com/gb/app/openvpn-connect/id590379981?mt=8\">here</a> to get the app you will need to connect.";
print "<br>\n";
print "Now, once your app is installed...";
print "<br>\n";
print "<B>Step 2.</B> Click <a href=\"http://vpn.publicaccesswifi.org/opvpn_client_conf/paws.mobileconfig\">here</a> download a special PAWS setup file to get you connected";
print "<p>\n";
print "<B>Step 3.</B> When you see the 'Install Profile' screen, touch 'Install'. When you see the 'Unsigned Profile' warning, touch 'Install Now'. Touch 'Done'. Go to the OpenVPN Connect app. Enter your PAWS username into the 'User ID' box.
Enter your PAWS password into the 'Password' box. Slide the button next to 'Save' to green. Slide the button next to 'Disconnected' to green.<br>\n";	
}
#########################
sub print_windows {
intro_text();
print "<br>\n";
print "<B>Step 1.</B> Please click <a href=\"http://www.tunxten.com/download\">here</a> to get the app you will need to connect.";
print "<p>\n";
print "<B>Step 2.</B> Click <a href=\"http://vpn.publicaccesswifi.org/opvpn_client_conf/paws.ovpn\">here</a> download a special PAWS setup file to get you connected";
print "<p>\n";
print "<B>Step 3.</B> Install the Tunxten app. Go to the Windows Notification Area (screen bottom right, next to clock) and click on the Tunxten icon.
Click the blue '+' for 'Import OpenVPN Configuration'. Click the '...files on my computer' button.
Browse to the location of 'paws.ovpn' (downloaded in Step 2). This is likely to be the Windows Download folder at: C:\\Users\**your Windows username**\\Downloads.
Select 'paws.ovpn' and then click 'Open'. Click 'Close' in the configuration list window.
Go to the Windows Notification Area and click on the Tunxten icon. 
In the 'Paws' configuration, click the 'Connect' icon (small circle, to the right of the green shield icon).
When asked to provide login credentials, enter your PAWS username and password. Click OK.<br>\n";
}
#########################
sub print_apple {
intro_text();
print "<br>\n";
print "<B>Step 1.</B> Please click <a href=\"https://sourceforge.net/projects/tunnelblick/files/All%20files/Tunnelblick_3.3.2.dmg/download\">here</a> to get the app you will need to connect.";
print "<br>\n";
print "<B>Step 2.</B> Click <a href=\"http://vpn.publicaccesswifi.org/opvpn_client_conf/paws.ovpn\">here</a> download a special PAWS setup file to get you connected";
print "<p>\n";
print "<B>Step 3.</B>Install the Tunnelblick app downloaded at Step 1. Run Tunnelblick. Click [icon]>VPN details. Click '+' in bottom left corner to add a configuration. Click 'I have configurations'. 
Click 'openvpn configurations'. Move the paws.ovpn file you downloaded in Step 2 into the 'Empty Tunnelblick VPN Configuration' folder created on your desktop.
Rename the 'Empty Tunnelblick VPN Configuration' directory to 'PAWS-VPN.tblk'. Double click PAWS-VPN.tblk and follow on screen prompts for tunnelblick to install config. 
Connect to PAWS-VPN, entering your PAWS username and password, when requested.<br>\n";
}

#########################
sub print_unknown {
	print "<br>\n";
	print "Instructions for this device coming soon...\n";
	print "<br>\n";
}





