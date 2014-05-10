<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
	<head>
		<style type="text/css">
			div.c1 {width: 900px; height: 500px;}
			#container{text-align: center;}
			#msg{text-color:red;}
		</style>
  		<title>{{title or 'No title'}}</title>
  		{{!js_code or '</br>'}}
	</head>
	
	<body>
		<div id="container">
			
			<div id="msg" class="span-24">
				{{!msg}}
			</div>
			
			<div id="text_result" class="span-24">
				{{!text_result}}
			</div>
			
			<div id="form" class="span-24">
				{{!form}}
			</div>
			<div id="charts_div" class="c1"></div>
		</div>
	</body>
</html>