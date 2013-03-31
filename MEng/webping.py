import urllib2

req = urllib2.Request('http://devtest.appinions.com/infapi/people/personas?influencerid=b97f7b3e-66ea-4322-a3ac-2fbf7afe2e40&appkey=cjvgsbragwdyncddda3ujmw8')
response = urllib2.urlopen(req)
the_page = response.read()
print the_page