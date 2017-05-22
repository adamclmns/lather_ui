string_to_parse = """
    <h1>Suds <small>(  version: 1.3.3.0 IN  build: 20170311)</small></h1>

    <hr/>Service ( GlobalWeather ) tns="http://www.webserviceX.NET"
    <p>   Prefixes (0)
    <p>   Ports (2):
    <p>      (GlobalWeatherSoap)
    <p>         Methods (2):
    <p>            GetCitiesByCountry(xs:string CountryName, )
    <p>            GetWeather(xs:string CityName, xs:string CountryName, )
    <p>         Types (0):
    <p>      (GlobalWeatherSoap12)
    <p>         Methods (2):
    <p>            GetCitiesByCountry(xs:string CountryName, )
    <p>            GetWeather(xs:string CityName, xs:string CountryName, )
    <p>         Types (0):
    <hr/>
    """

def dict_insert_or_append(adict,key,val):
    """Insert a value in dict at key if one does not exist
    Otherwise, convert value to list and append
    """
    if key in adict:
        if type(adict[key]) != list:
            adict[key] = [adict[key]]
        adict[key].append(val)
    else:
        adict[key] = val

def ttree_to_json(ttree,level=0):
    result = {}
    for i in range(0,len(ttree)):
        cn = ttree[i]
        try:
            nn  = ttree[i+1]
        except:
            nn = {'level':-1}

        # Edge cases
        if cn['level']>level:
            continue
        if cn['level']<level:
            return result

        # Recursion
        if nn['level']==level:
            dict_insert_or_append(result,cn['name'],cn['value'])
        elif nn['level']>level:
            rr = ttree_to_json(ttree[i+1:], level=nn['level'])
            dict_insert_or_append(result,cn['name'],rr)
        else:
            dict_insert_or_append(result,cn['name'],cn['value'])
            return result
    return result


def parse(line):
    spaces = len(l) - len(line.lstrip(' '))
    return line.lstrip(' '), spaces

result = {}
parents = {}
last_level = 0 # This is the root for SUDS Client
parents[0] = result
last_parent = None

for l in string_to_parse.split('\n'):  # for l in f.xreadlines():
    (line, level) = parse(l)  # create parse to return character and indentation
    print("____________________________________")
    print(line)
    print(level)
    if level == last_level:
        # New parent, or we're at the first line
        parents[level]


print("DONE")

print(result)
