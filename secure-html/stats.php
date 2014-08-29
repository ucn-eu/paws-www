<html>
<head>
	<title>PAWS Router Statistics</title>
	<link rel="stylesheet" type="text/css" href="stats.css">
</head>
<body>
<?php

/* Error reporting
ini_set('display_errors',1);
ini_set('display_startup_errors',1);
error_reporting(-1);
*/
echo "<div class='StatStyle'>";
echo "<h1>Router Device Activity</h1>";
echo "</div>";

$host = "127.0.0.1"; 
$user = "paws"; 
$port = "5432";
$pass = "g5juikR12MskPJF"; 
$db = "paws_mgmt"; 

$con = pg_connect("host=$host port=$port dbname=$db user=$user password=$pass") 
	or die("Unable to connect to db");
	
$query = "SELECT * FROM devices";
$rs = pg_query($con, $query) or die("Cannot execute query: $query\n"); 

echo "<div class='StatStyle'>";
echo "<table>
    <tr>
        <td>ID</td>
        <td>Version</td>
		<td>IP Address</td>
		<td>Last Active</td>
		<td>User</td>
		<td>Network</td>
		<td>Status</td>		
    </tr>";

while ($row = pg_fetch_row($rs)) {
	$now = time();
	$last = strtotime($row[3]);
	$interval = $now-$last;
	echo "<tr>";
		echo "<td>".$row[0]."</td>";
		echo "<td>".$row[1]."</td>";
		echo "<td>".$row[2]."</td>";
		echo "<td>".$row[3]."</td>";
		echo "<td>".$row[4]."</td>";
		echo "<td>".$row[5]."</td>";
		
		if($interval > 600){
			echo "<td><img src='images/offline.png' title='Router has been off-line for more than 10 minutes' width='20' height='20'></td>";
		} elseif ($interval > 300){
			echo "<td><img src='images/justoffline.png' title='Router has been off-line for more than 5 minutes' width='20' height='20'></td>";
		} else {
			echo "<td><img src='images/online.png' title='Router is on-line' width='20' height='20'></td>";
		}		
	echo "</tr>";
}
echo "</table>";
echo "</div>";

?>
</body>
</html>
