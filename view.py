from mod_python import apache
from mod_python import util
import utils

html1 = """
<!DOCTYPE HTML>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<title>
"""
html2 = """</title>

		<script type="text/javascript" src="../libs/jquery-1.8.3.min.js"></script>
		<script type="text/javascript">
$(function () {
    var chart;
    $(document).ready(function() {
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'container',
                type: 'line'
            },
            title: {
                text: 'Salespoint checker'
            },
            subtitle: {
                text: 'by dspshin'
            },
            yAxis: {
                title: {
                    text: 'Salespoint'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled:false 
                    },
                    enableMouseTracking: false
                },
		series: {
			marker: {
				radius:2
			}
		}
            },
            series: [{
"""
                #name: 'Tokyo',
                #data: [7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
html3="""
            }],
"""
html4="""   
        });
    });
    
});
		</script>
	</head>
	<body>
<script src="../libs/highcharts/highcharts.js"></script>
<script src="../libs/highcharts/modules/exporting.js"></script>

<div id="container" style="min-width: 400px; height: 400px; margin: 0 auto"></div>

	</body>
</html>
"""

def handler(req):
	db = utils.DB()
	req.content_type="Text/html"
	req.send_http_header()

	fs = util.FieldStorage(req)
	title = fs.getfirst('title', None)

	dates, raw_scores = db.getResult(title)
	dates.reverse()
	raw_scores.reverse()
	chart_data = ""

	data_length = len(raw_scores)

	for r in raw_scores:
		if r<1: r=1
		try:
			chart_data += "%d,"%r
		except:
			pass

	date_data = ""
	i=0
	for d in dates:
		if i==0 or i==len(dates)-1:
			date_data += "'%s',"%d
		else:
			date_data += "'',"
		i+=1
	date_data = date_data[:-1]
	chart_data = chart_data[:-1]
	data = "name: '"+title+"',"
	data+= "data: ["+chart_data+"]"
	
	xaxis = "xAxis: { categories : [%s]}"%date_data

	req.write(html1+title+html2+data+html3+xaxis+html4)
	return apache.OK

