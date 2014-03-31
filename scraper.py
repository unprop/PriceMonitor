import scraperwiki
import gviz_api

#Example of:
## how to use the Google gviz Python library to cast Scraperwiki data into the Gviz format
## how to render the gviz data format using the Google Visualization library

#Based on the code example at:
#http://code.google.com/apis/chart/interactive/docs/dev/gviz_api_lib.html


page_template = """
<html>
  <head>
      <title>Fietsenwinkel Prijsmonitor - Fietsvoordeelshop</title>
      <script src="https://www.google.com/jsapi" type="text/javascript"></script>
      <script>
        google.load('visualization', '1', {packages:['table']});

        google.setOnLoadCallback(drawTable);
        function drawTable() {

          var json_table = new google.visualization.Table(document.getElementById('table_div_json'));
          var json_data = new google.visualization.DataTable(%(json)s, 0.6);
      
          var color_formatter = new google.visualization.ColorFormat();
          color_formatter.addRange(-10000, -998, 'white', 'white');
          color_formatter.addRange(-5000, -10, 'white', '#CD0000');
          color_formatter.addRange(-10, -0.005, 'white', '#FF3030');
          color_formatter.addRange(-0.005, 0.005, 'black', null);
          color_formatter.addRange(0.005, 10, 'white', '#32CD32');
          color_formatter.addRange(10, 20000, 'white', '#008B00');
          color_formatter.format(json_data, 4);
          color_formatter.format(json_data, 5);
          color_formatter.format(json_data, 6);
          color_formatter.format(json_data, 7);
          
/*  
          var number_formatter = new google.visualization.NumberFormat({
            prefix: '€', decimalSymbol: ',', groupingSymbol: '.', negativeParens: false});
          number_formatter.format(json_data, 3);
          number_formatter.format(json_data, 4);
          number_formatter.format(json_data, 5);
          number_formatter.format(json_data, 6);
          number_formatter.format(json_data, 7);
*/

          json_table.draw(json_data,{
            showRowNumber: false,
            page: 'enable',
            pageSize: 20,
            allowHtml: true,
            width: "1000px",
          });
        }
      </script>
      <style>
          h1 { font-family: 'Calibri', 'Myriad', arial, sans-serif; }
          div#scraperwikipane { display:none !important; }  
      </style>
  </head>
  <body>
    <h1>Fietsenwinkel Prijsmonitor</h1>
    <div id="table_div_json"></div>
  </body>
</html>
"""


scraperwiki.sqlite.attach( 'pricescraper' )
q = 'title, category, sku, our_price, gf_price, fvs_price, cb_price, izi_price FROM swdata'
data = scraperwiki.sqlite.select(q)

description = {
    "title": ("string", "Fietsnaam"),
    "category": ("string", "Categorie"),
    "sku": ("string", "SKU"),
    "our_price": ("number", "FW prijs"),
    "gf_price": ("number", "GF prijs"),
    "fvs_price": ("number", "FVS prijs"),
    "cb_price": ("number", "CB prijs"),
    "izi_price": ("number", "IZI prijs")
}

data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

json = data_table.ToJSon(columns_order=("title", "category", "sku", "our_price", "gf_price", "fvs_price", "cb_price", "izi_price"),order_by="title")



# Putting the JS code and JSon string into the template
#print "Content-type: text/html"
#print
print page_template % vars()