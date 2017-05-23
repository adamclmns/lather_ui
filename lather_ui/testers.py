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
<<<<<<< 2bbf46305a1c7a8df37b0b8e9620aa98c9237938
    (line, level) = parse(l)  # create parse to return character and indentation
    print("____________________________________")
    print(line)
    print(level)
    if level == last_level:
        # New parent, or we're at the first line
        parents[level]


print("DONE")
=======
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
>>>>>>> Minor style cleanup

print(result)
