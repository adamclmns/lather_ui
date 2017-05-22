def parse(line):
    spaces = len(l) - len(line.lstrip(' '))
    return line.lstrip(' '), spaces


string_to_parse = """
    Suds ( https://github.com/cackharot/suds-py3 )  version: 1.3.3.0 IN  build: 20170311

    Service ( GlobalWeather ) tns="http://www.webserviceX.NET"
       Prefixes (0)
       Ports (2):
          (GlobalWeatherSoap)
             Methods (2):
                GetCitiesByCountry(xs:string CountryName, )
                GetWeather(xs:string CityName, xs:string CountryName, )
             Types (0):
          (GlobalWeatherSoap12)
             Methods (2):
                GetCitiesByCountry(xs:string CountryName, )
                GetWeather(xs:string CityName, xs:string CountryName, )
             Types (0):
    """

for line in string_to_parse.split('\n'):
    print(line)

result = {}
parents = {}
last_indentation = None
parents[0] = result
for l in string_to_parse.split('\n'):  # for l in f.xreadlines():
    (c, i) = parse(l)  # create parse to return character and indentation

    # Sometimes, the data is already indented by a certain amount... we need to
    # know that the first line we read is the root
    if last_indentation is None:
        last_indentation = i  # We also want to skip the first line, because it's the SUDS version and build string
    elif i == last_indentation:
        # What's our indentation step?
        dif = abs(i - last_indentation)
        # sibling to last

        new_el = {}
        parents[i - dif][c] = new_el
        parents[i] = new_el
        last_indentation = i
    elif i > last_indentation:
        # child of last element... last element must be parent
        dif = abs(i=last_indentation)
        new_el = c
        parents[i - c]
        pass
    else:
        # end of children, back to a higher level
        pass

print(parents)
print(result)
