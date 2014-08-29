<?php
/**
 * This section ensures that Twilio gets a response.
 */
header('Content-type: text/xml');
echo '<?xml version="1.0" encoding="UTF-8"?>';
echo '<Response><Message>Thank you for your interest in the PAWS project, we will be in contact.</Message></Response>'; //Place the desired response (if any) here
 
/**
 * This section actually sends the email.
 */
$to      = "horizon-paws-ops@cs.nott.ac.uk"; // Your email address
$subject = "Message from {$_REQUEST['From']} at {$_REQUEST['To']}";
$message = "PAWS has received an SMS message from {$_REQUEST['From']}.
Body: {$_REQUEST['Body']}";
$headers = "From: DoNotReply@vpn.publicaccesswifi.org"; // Who should it come from?
 
mail($to, $subject, $message, $headers);