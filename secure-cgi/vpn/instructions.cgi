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
android_message();
intro_text();
print "<br>\n";
print "<B>Step 1.</B> Please click <a href=\"https://play.google.com/store/apps/details?id=net.openvpn.openvpn\">here</a> to get the app you will need to connect.";
print "<br>\n";
print "Now, once your app is installed...";
print "<br>\n";
print "<B>Step 2.</B> Click <a href=\"http://vpn.publicaccesswifi.org/opvpn_client_conf/paws.ovpn\">here</a> download a special PAWS setup file to get you connected";
print "<p>\n";
print "<B>Step 3.</B>
<ul>
<li>Run the OpenVPN Connect app that you installed at Step 1.
</li><li>Press the list/menu button on the case of your phone.
</li><li>Touch 'Import' and then touch 'Import Profile from SD Card'. 
</li><li>Browse to the location of 'paws.ovpn', which was downloaded at Step 2 (this should be in your browser's 'Downloads' folder, exact location dependent on browser). 
</li><li>Select 'paws.ovpn'
</li><li>Enter your PAWS username and password
</li><li>Tick the 'save' box and touch 'Connect'.
</li>
</ul>";
}

#########################
sub print_iOS {
ios_message();
intro_text();
print "<br>\n";
print "<B>Step 1.</B> Please click <a href=\"https://itunes.apple.com/gb/app/openvpn-connect/id590379981?mt=8\">here</a> to get the app you will need to connect.";
print "<br>\n";
print "Now, once your app is installed...";
print "<br>\n";
print "<B>Step 2.</B> Click <a href=\"http://vpn.publicaccesswifi.org/opvpn_client_conf/paws.mobileconfig\">here</a> download a special PAWS setup file to get you connected";
print "<p>\n";
print "<B>Step 3.</B> 
<ul>
<li>When you see the 'Install Profile' screen, touch 'Install'.
</li><li>When you see the 'Unsigned Profile' warning, touch 'Install Now' and then Touch 'Done'.
</li><li>Go to the OpenVPN Connect app and enter your PAWS username into the 'User ID' box.
</li><li>Enter your PAWS password into the 'Password' box.
</li><li>Slide the button next to 'Save' to green.
</li><li>Slide the button next to 'Disconnected' to green.
</li>
</ul>";	
}
#########################
sub print_windows {
pc_message();
intro_text();
print "<br>\n";
print "<B>Step 1.</B> Please click <a href=\"http://vpn.publicaccesswifi.org/opvpn_client_apps/tunXten-1.0.8.6-setup.exe\">here</a> to get the app you will need to connect.";
print "<p>\n";
print "<B>Step 2.</B> Click <a href=\"http://vpn.publicaccesswifi.org/opvpn_client_conf/paws.ovpn\">here</a> download a special PAWS setup file to get you connected";
print "<p>\n";
print "<B>Step 3.</B>
<ul>
<li>Install the Tunxten app.
</li><li>Go to the Windows Notification Area (screen bottom right, next to clock) and click on the Tunxten icon.
</li><li>Click the blue '+' for 'Import OpenVPN Configuration'.
</li><li>Click the '...files on my computer' button.
</li><li>Browse to the location of 'paws.ovpn' (downloaded in Step 2). This is likely to be the Windows Download folder at: C:\\Users\**your Windows username**\\Downloads.
</li><li>Select 'paws.ovpn' and then click 'Open'.
</li><li>Click 'Close' in the configuration list window.
</li><li>Go to the Windows Notification Area and click on the Tunxten icon. 
</li><li>In the 'Paws' configuration, click the 'Connect' icon (small circle, to the right of the green shield icon).
</li><li>When asked to provide login credentials, enter your PAWS username and password. Click OK.
</li>
</ul>";
}
#########################
sub print_apple {
mac_message();
intro_text();
print "<br>\n";
print "<B>Step 1.</B> Please click <a href=\"http://vpn.publicaccesswifi.org/opvpn_client_apps/Tunnelblick_3.3.2.dmg\">here</a> to get the app you will need to connect.";
print "<br>\n";
print "<B>Step 2.</B> Click <a href=\"http://vpn.publicaccesswifi.org/opvpn_client_conf/paws.ovpn\">here</a> download a special PAWS setup file to get you connected";
print "<p>\n";
print "<B>Step 3.</B>
<ul>
<li>Install the Tunnelblick app downloaded at Step 1. 
</li><li>Run Tunnelblick and click [icon]>VPN details. 
</li><li>Click '+' in bottom left corner to add a configuration. 
</li><li>Click 'I have configurations'. 
</li><li>Click 'openvpn configurations'. 
</li><li>Move the paws.ovpn file you downloaded in Step 2 into the 'Empty Tunnelblick VPN Configuration' folder created on your desktop.
</li><li>Rename the 'Empty Tunnelblick VPN Configuration' directory to 'PAWS-VPN.tblk'. 
</li><li>Double click PAWS-VPN.tblk and follow on screen prompts for tunnelblick to install config. 
</li><li>Connect to PAWS-VPN, entering your PAWS username and password, when requested.
</li>
</ul>";
}

#########################
sub print_unknown {
	print "<br>\n";
	print "Instructions for this device coming soon...\n";
	print "<br>\n";
}

#########################
sub pc_message {
	print "<p><h3>If you already have a PAWS set up on your device then please start the Tunxten VPN app first before you can access the Internet.
	Otherwise, you will keep on being directed to this page.</h3></p>";
}

#########################
sub mac_message {
	print "<p><h3>If you already have a PAWS set up on your device then please start the Tunnelblick VPN app first before you can access the Internet.
	Otherwise, you will keep on being directed to this page.</h3></p>";
}

#########################
sub ios_message {
	print "<p><h3>If you already have a PAWS set up on your device then please start the OpenVPN Connect app first before you can access the Internet.
	Otherwise, you will keep on being directed to this page.</h3></p>";
}

#########################
sub android_message {
	print "<p><h3>If you already have a PAWS set up on your device then please start the OpenVPN app first before you can access the Internet.
	Otherwise, you will keep on being directed to this page.</h3></p>";
}
