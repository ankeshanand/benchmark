<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
	<head>
		<style type="text/css">
			div.c1 {width: 900px; height: 500px;}
			#msg{text-color:red;}
			h1{text-aligh:center;}
		</style>
  		<title>Benchmark Performance Database Frontend</title>
	</head>
	
	<body>
		<h1> <u>Benchmark Performance Database</u> </h1>
		<div id="container">
			{{content}}
			
			
			<br/>
			
			<h2> Available plots </h2>
			<table border=1>
				<tr>
					<td>1</td>
					<td><a href='/absperformance'>Absolute Performance vs Reference images</a></td>
					<td> Plot of absolute performance(rays/sec) of various architectures w.r.t to each of the reference images. The horizontal axis has the reference images and the vertical axis is the average of all the measured absolute performances over a particular architecture. One could compare various architectures w.r.t to these images.</td>
				</tr>
				<tr>
					<td>2</td>
					<td><a href='/avgperfvsarch'>Average Absolute Performance vs Architecture</a></td>
					<td>Check the variation of average of the absolute performance(rays/sec) on various architectures. The horizontal axis has the architectures and the vertical axis measures the average of absolute performance. Atleast two architectures have to be selected for this plot.</td>
				</tr>
				<tr>
					<td>3</td>
					<td><a href='/perfvscpus'>Performance vs Number of CPUs</a></td>
					<td>Performance variation with the number of CPUs over various architecture with the variation could be checked using this plot. The horizontal axis has the number of CPUs and the vertical axis measures the average of absolute performance. </td>
				</tr>
				<tr>
					<td>4</td>
					<td><a href='/imgperfvscpus'>Image Performance vs Number of CPUs</a></td>
					<td>Performance variation with the number of cores over various reference images over a particular architecture. The horizontal axis has the number of CPUs and the vertical axis measures the average of absolute performance.</td>
				</tr>
			</table>
			
		</div>
	</body>
</html>