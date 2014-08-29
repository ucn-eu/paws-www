#!/usr/bin/perl -wT
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser); 
use DBI;
use strict;

my $consent1 = param('consent1');
my $consent2 = param('consent2');



if ($consent1 eq "yes" && $consent2 eq "yes") {
print "Location: https://vpn.publicaccesswifi.org/secure-cgi/signup_user.cgi/";
}
else
{
 print "Accept both terms and conditions and age";
}
print "Content-type: text/html\n\n";
print <<HTML;


<!DOCTYPE html

PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"

"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US" xml:lang="en-US">

<head>

<title>PAWS User Creation</title>

<link rel="stylesheet" type="text/css" href="/styles/style.css" />

<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />

</head>

<body>

<img align="CENTER" src="/images/Paws-Logo.jpg" />

<b> Welcome to PAWS (Public Access Wi-Fi Service). </b> <br>
<br<br><br>
<b> PAWS </b> is a research project conducted by the Universities of Nottingham and Cambridge. The aim is to improve access to the Internet by making better use of the existing resources in communities. This is done by sharing a small part of existing connections with those who aren’t online.
<br><br>On the next page you will be able to set up your PAWS account so that you can use the service. As this is a research project there are a few <b>Terms and Conditions </b> you must agree to first.<br><br>
1.	As part of the research, we will need to ask you a few questions about your experience of the PAWS service. We will contact you after you sign up to arrange to do this. You will be compensated for your time. <br>
<br>2.	During the trial we will be working on getting the best from the PAWS technology. This means that <b> we have to monitor what websites users access during the trial </b>. This data will be treated as confidential and only anonymised data will shared outside of the research team. Other PAWS users cannot see what you access.
<br><br>3.	You must be 16 or over. <br>
<br>If you have any problems with this service you can call 0115 8714190 or email paws&#64;horizon.ac.uk <br> <br>
</h1><form method="post" action="/secure-cgi/consent.cgi" enctype="multipart/form-data">

<table> <tr><td>I am over 16 </td> <td><label><input type="checkbox" name="consent1" value="yes" /></label></td></tr> 

<tr><td>I agree to the terms and conditions </td> <td><label><input type="checkbox" name="consent2" value="yes" /></label></td></tr> 

<td><input type="submit" name="submit_form" value="Continue" /></td></tr>
</table></form>

</body>

</html>




<!-- adding jquery to the page -->
<script type="text/javascript" src="/js/jquery-1.9.1.js"></script>
<script type="text/javascript">
\$(function() {
    var frm = \$('#userform');
    frm.submit(function () {
        console.log( 'the form values are', frm.serialize() );
	\$.ajax({
            type: 'GET',
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                console.log('ok',data);
		\$('#userstatus').html('<div style="background-color:red;margin:1em;padding:5px;"><h3>Registration Status</h3>'+ data+'</div>');
            }
        });
        return false;
    });
});
</script>

</body>
</html>

HTML
exit;
