from bs4 import BeautifulSoup
html_govno = """
<!DOCTYPE html>
<html>

<head>
   <title>Web Development Page</title>
   <style type="text/css">
      h1 {
         color: white;
         background: red;
      }

      li {
         color: red;
      }

      #css-li {
         color: blue;
      }

      .green {
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

# allLinks = pars_my_html.find_all(class_="green")[1]
# print(allLinks)
# print(allLinks.get_text())

all_select = pars_my_html.select(".green")
# print(pars_my_html.find_all(class_="green"))
print(len(all_select))

count = 0

# for link in allLinks:
#     count += 1
#     print(f'#{count} + {link}')
# for link in all_select:
#     count += 1
#     print(f'#{count} + {link.get_text()}')

# for link in all_select:
#     count += 1
#     print(f'#{count} + {link.name}')
# for link in all_select:
#     count += 1
#     print(f'#{count} + {link.attrs}')
# for link in all_select:
#     print(link.attrs['class'])

# print(pars_my_html.body.contents[7])

data = pars_my_html.find(id='css-li').parent
print(data)
