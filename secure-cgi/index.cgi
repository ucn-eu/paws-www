#!/usr/bin/perl -wT

use strict;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser); 

print header;

=begin comment
PAWS2 splash page by Javid Yousaf 1.8.2014
=end comment
=cut

my $agent;
$agent=$ENV{'HTTP_USER_AGENT'};

print '<html xmlns="http://www.w3.org/1999/xhtml">';
print '<head>';
print '<title>Public Access WiFi Service</title>';
print '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">';
print '<link rel="stylesheet" type="text/css" href="/Public%20Access%20WiFi%20Service_files/index.css" />';

print'</head>';

print '<body>';
print '<div id="container">';
print '<div class="header">';
print '<img id="logo" src="/Public%20Access%20WiFi%20Service_files/paws.jpg" alt="PAWS logo">';
print '<div id="h1_container"><h1>Welcome to the PAWS VPN Server</h1></div>';		
print '</div>';

print '<p><h2>Would you like free access to the Internet?</h2></p>';
print '<p><i>PAWS (Public Access Wi-Fi Service) is a University of Nottingham led research project which aims to help everyone access the internet.</i></p>';

#######################################
# Device dependant conditional output #	
#######################################
if ( $agent =~ /Android\s(\d)\.(\d)\.(\d)/ ) {
	my $android_v1 = $1;
	my $android_v2 = $2;
	my $android_v3 = $3;
	
	if($android_v1 > 3)
	{
	print '<p><b>Please text PAWS to +441158241502 and our team will get you started*.</b></p>';
	}
	else
	{
	print 'Unfortunately PAWS requires Android 4 or higher.';
	}
}
elsif ( $agent =~ /\((iP\w+);/ ) {
	print '<p><b>Please text PAWS to +441158241502 and our team will get you started*.</b></p>';
}
elsif (( $agent =~ /Macintosh;.*Mac (OS\s+X\s+\d+_\d+_\d+)/ ) || ($agent =~ /Windows\sNT/ ) ) {
	print '<p><b>For desktop or laptop please click <a href="https://vpn.publicaccesswifi.org/secure-cgi/consent.cgi">here</a> to get started.</b></p>';
}

else {
	print '<h3>Sorry your device is currently unsupported for PAWS</h3>';  
}
#######################################

print '<p>This internet access service is shared to you through your neighbours who have taken part in the University of Nottingham PAWS project.</p>';
	 
print '<p><h4>Already have a PAWS account? Please click <a href="https://vpn.publicaccesswifi.org/secure-cgi/vpn/instructions.cgi"> here</a>.'; 
print 'You can also change your details including password<a href="https://vpn.publicaccesswifi.org/secure-cgi/edit_details_login.cgi"> here</a>.</h4></p>';
		
print '<p>For further information on the PAWS project visit our website  <a href="http://www.publicaccesswifi.org/">www.publicaccesswifi.org</a>.</p>';
print '<p><h5><i>*SMS at your standard network rate.</i></h5></p>';

print '<p><h6><a href="https://vpn.publicaccesswifi.org/admin.html">admin</a></h6></p>';
print '</div>';

print '<img src="/Public%20Access%20WiFi%20Service_files/bismark.gif" alt="Project BISmark" height="60">';
print '<img src="/Public%20Access%20WiFi%20Service_files/nch.jpg" alt="Nottingham City Homes" height="60">';
print '<img src="/Public%20Access%20WiFi%20Service_files/epsrc.jpg" alt="EPSRC " height="60">';
print '<img src="/Public%20Access%20WiFi%20Service_files/horizon.jpg" alt="Horizion" height="60">';
print '<img src="/Public%20Access%20WiFi%20Service_files/dot_rural.png" alt="dot.rural" height="60">';
print '<img src="/Public%20Access%20WiFi%20Service_files/samknows.jpg" alt="Sam Knows" height="60">';
print '<img src="/Public%20Access%20WiFi%20Service_files/ncc.jpg" alt="NCC" height="60">';
print '<img src="/Public%20Access%20WiFi%20Service_files/mlab.png" alt="M LAB" height="60">';

print '</body>';
print '</html>';

print end_html;