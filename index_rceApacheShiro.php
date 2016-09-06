<?php
if(isset($_GET['flag'])){
$flag=$_GET['flag'];
}else{
$flag='';
}
$id=$_GET['id'];
if ($flag=="rceApacheShiro"){
	$myfile = fopen("log.txt", "w") or die("Unable to open file!");
	fwrite($myfile, $id."|".$flag."\n");
	fclose($myfile);
}else{
	$myfile = fopen("log.txt", "r") or die("Unable to open file!");
 	$filecontent = fgets($myfile,47);
	echo $filecontent;
	//if(strpos($filecontent, $id)==true){
	//	echo $filecontent;
	//	exit();
	//}
	fclose($myfile);
}
?>
