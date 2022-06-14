from bs4 import BeautifulSoup
html_govno = """
	<!DOCTYPE html>
	<html>
	<head>
		<title>Web Development Page</title>
		<style type="text/css">
			
			h1{
				color: white;
				background: red;
			}

			li{
				color: red;
			}

			#css-li{
				color: blue;
			}

			.green{
				color: green;
			}

		</style>
	</head>
	<body>
		<h1>Web Development</h1>
		<h1 class="green">Web</h1>
		<h3>Programming Languages</h3>

		<ol>
			<li>HTML</li>
			<li id="css-li">CSS</li>
			<li class="green">JavaScript</li>
			<li class="green">Python</li>
		</ol>

	</body>
	</html>



"""

pars_my_html = BeautifulSoup(html_govno, 'html.parser')


# print(pars_my_html.body.ol.li)
# print(pars_my_html.find('li'))
print(type(pars_my_html.find('li')))
# print(pars_my_html.find_all('li'))
print(type(pars_my_html.find_all('li')))
print(type(pars_my_html.select('li')))
# print(pars_my_html.find(id="css-li"))  
# print(pars_my_html.select('#css-li')[0])
# print(pars_my_html.find_all(class_="green"))
# print(pars_my_html.select(".green")[1])
# print(pars_my_html.select("li")[3].string)

# for link in pars_my_html('li'):
#     link += 1
#     print(link.get().name)
