<?php
	$state = '';
	$days = -1;
	if (isset($_POST["submit"])){
		$state = $_POST['state'];
		$days = intval($_POST['days']);
		$cmd = 'python demo_baseline.py '.$state;
		$out = exec($cmd);
		$out = str_replace("donald_trump", "Donald Trump", $out);
		$out = str_replace("john_kasich", "John Kasich", $out);
		$out = str_replace("kasich", "John Kasich", $out);
		$out = str_replace("hillary_clinton", "Hillary Clinton", $out);
		$out = str_replace("bernie_sanders", "Bernie Sanders", $out);
		$out = str_replace("marco_rubio", "Marco Rubio", $out);
		$out = str_replace("ted_cruz", "Ted Cruz", $out);

		$baseline_pred = json_decode($out, true);
		$cmd = 'python demo_predict.py '.$state.' '.strval($days);
		$out = exec($cmd);
		$out = str_replace("donald_trump", "Donald Trump", $out);
		$out = str_replace("john_kasich", "John Kasich", $out);
		$out = str_replace("kasich", "John Kasich", $out);
		$out = str_replace("hillary_clinton", "Hillary Clinton", $out);
		$out = str_replace("bernie_sanders", "Bernie Sanders", $out);
		$out = str_replace("marco_rubio", "Marco Rubio", $out);
		$out = str_replace("ted_cruz", "Ted Cruz", $out);
		$improved_pred = json_decode($out, true);


	
	}
?>
<title>Predicting elections</title>
<link rel="stylesheet" href="bootstrap.min.css">

<div class='container'>
<div class="page-header">
	<h1>Predicting US Primaries 2016 <small> through Twitter </small></h1> 
</div>
<form action="demo_nlp.php" method="post">
	  <div class="form-group">
	    <label for="exampleInputEmail1">State Name</label>
		<select name="state" class="form-control" selected="alaska">
		<?php 
			$places = ['alabama', 'alaska', 'arizona', 'arkansas', 'colorado', 'connecticut', 'delaware', 'districtofcolumbia', 'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'iowa', 'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri', 'nebraska', 'nevada', 'newhampshire', 'newyork', 'northcarolina', 'northdakota', 'ohio', 'oklahoma', 'pennsylvania', 'rhodeisland', 'southcarolina', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington', 'wisconsin', 'wyoming'];
			$places_2 = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Nebraska', 'Nevada', 'New Hampshire', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'Wisconsin', 'Wyoming'];
			for ($x = 0; $x < sizeof($places); $x++) {
			    echo '<option value="'.$places[$x].'" ';
			    if($state == $places[$x])
			    	echo 'selected="selected"';
			    echo '>'.$places_2[$x].'</option>';
			} 
		?>	  
	</select>
	
</div>
<div class="form-group">
	<label for="exampleInputEmail2">Number of days to Primary</label>
		<select name="days" class="form-control">
			<?php
			for ($x = 0; $x <= 14; $x++) {
				    echo '<option value="'.$x.'" ';
			    if($days == $x)
			    	echo 'selected="selected"';
			    echo '>'.$x.'</option>';
			}
			?>
		
		
	</select><br>
</div>
	<button type="submit" class="btn btn-default" name="submit">Submit</button>
</form>

<?php
	if (isset($_POST["submit"])){
?>


<div class="row">
	<div class="col-md-6">
		<div class="panel panel-primary">
		<div class="panel-heading">
		    <h3 class="panel-title" style="font-variant: small-caps;">Counts (Baseline)</h3>
		  </div>
		  <div class="panel-body">
		  	<table class="table table-striped">
		  		<tr>
		  			<th>Party</th>
		  			<th>Actual</th>
		  			<th>Predicted</th>
		  		</tr>
		  		<tr class=<?php echo ($baseline_pred['rep']['actual'] == $baseline_pred['rep']['predicted'])?"success":"danger"; ?> >
		  			<td>Republicans</td>
		  			<td><?php echo $baseline_pred['rep']['actual'] ?></td>
		  			<td><?php echo $baseline_pred['rep']['predicted'] ?></td>
		  		</tr>
		  		<tr class=<?php echo ($baseline_pred['dem']['actual'] == $baseline_pred['dem']['predicted'])?"success":"danger"; ?> >
		  			<td>Democrats</td>
		  			<td><?php echo $baseline_pred['dem']['actual'] ?></td>
		  			<td><?php echo $baseline_pred['dem']['predicted'] ?></td>
		  		</tr>
			</table>
		  </div>
		  
		</div>
	</div>
	<div class="col-md-6">
		<div class="panel panel-primary">
		<div class="panel-heading">
		    <h3 class="panel-title" style="font-variant: small-caps;">TimeSentiments</h3>
		  </div>
		  <div class="panel-body">
		    <table class="table table-striped">
		  		<tr>
		  			<th>Party</th>
		  			<th>Actual</th>
		  			<th>Predicted</th>
		  		</tr>
		  		<tr class=<?php echo ($improved_pred['rep']['actual'] == $improved_pred['rep']['predicted'])?"success":"danger"; ?> >
		  			<td>Republicans</td>
		  			<td><?php echo $improved_pred['rep']['actual'] ?></td>
		  			<td><?php echo $improved_pred['rep']['predicted'] ?></td>
		  		</tr>
		  		<tr class=<?php echo ($improved_pred['dem']['actual'] == $improved_pred['dem']['predicted'])?"success":"danger"; ?> >
		  			<td>Democrats</td>
		  			<td><?php echo $improved_pred['dem']['actual'] ?></td>
		  			<td><?php echo $improved_pred['dem']['predicted'] ?></td>
		  		</tr>
			</table>
		  </div>
		  
		</div>
	</div>
</div>
</div>
<?php
	}
?>
