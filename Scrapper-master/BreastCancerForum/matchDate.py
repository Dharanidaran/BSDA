# matchDate.py

import re


sentence = """

Mom recently diagnosed with breast cancer



6 Posts


95 Views



    Created by:
    rpreston133
    on
     Feb  5, 2018 01:12PM


      Latest post:
       Feb  7, 2018 02:04AM

        by
        Peregrinelady

"""
# pattern = re.compile(r'\b[a-z]{3}\s+\d+,\s\d+\s\d+:\d+[AP]M')
# pattern = re.compile(r'(?P<Created>\w{3}\s+\d+,\s\d+\s\d+:\d+[AP]M)')
pattern = re.compile(r"""
(?P<Created>\w{3}\s+\d+,\s\d+\s\d+:\d+[AP]M) # Created On

""",re.VERBOSE
)



matches =  pattern.finditer(sentence)


for match in matches:
    print(match.group())
    print("-----------")
