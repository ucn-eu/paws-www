#!/usr/bin/perl -wT
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser); 
use DBI;
use strict;




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
Enter your username and password to change your details.
<br><br>
</h1><form method="post" action="/secure-cgi/edit_details.cgi" enctype="multipart/form-data">

<table> 
Username <input type="text" name="un"><br>
Password <input type="password" name="password"><br>
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
