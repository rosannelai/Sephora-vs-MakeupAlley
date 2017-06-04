# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import json
import requests
from lxml import html
import signal

driver = webdriver.PhantomJS() # or add to your PATH

#category = ["Face-Makeup","Cheek-Makeup","Eye-Makeup","Lips-Makeup","Makeup-Applicators","Makeup-Accessories","Nails-Makeup"]
#category = ["Moisturizing-Cream-Oils-Mists","Cleanser","Facial-Treatments","Skin-Care-Tools","Face-Mask","Eye-Treatment-Dark-Circle-Treatment","Sunscreen-Sun-Protection","Self-Tanning-Products","Lip-Treatments"]
#category = ["Fragrances-for-Women","Fragrances-for-Men"]
#category = ["Shampoo-Conditioner","Hair-Products-Treatments","Hair-Styling-Tools"]
#category = ["Bath-and-Body-Soap","Body-Moisturizers","Sun-Lotion","Bronzer-Self-Tanner-Bath-Body","Body-Care","Body-Care-Tools","Home-Scents-Candles","Beauty-Supplements-Bath-Body","Mens-Bath-Body-Care"]

for cat in category:
    print cat
    base_url = 'http://www.sephora.com/'+str(cat)+'?pageSize=-1&currentPage='
    for x in xrange(0, 5):
        url = base_url+str(x)
        driver.get(url)
        if x > 0:
                parsed_json = json.loads(driver.find_element_by_id('searchResult').get_attribute("innerHTML"))
                products = parsed_json["products"]
                print len(products)
                makeupdatasaved = ""
                for product in products:
                    if product["rating"]==0:
                        product['num_reviews'] = "0"
                    else:
                        url_review = "http://reviews.sephora.com/8723abredes/"+ product['id'] + "/reviews.htm?format=noscript"
                        response = requests.get(url_review)
                        tree = html.fromstring(response.content)
                        reviews = tree.xpath('//span[@class="BVRRNumber"]/text()')
                        if len(reviews) == 0:
                             product['num_reviews'] = "0"               
                        else:
                            product['num_reviews'] = reviews[0]
                    makeupdata = product["brand_name"].encode("utf-8")+"|"+product["brand_name"].encode("utf-8")+" "+product["display_name"].encode("utf-8")+"|"+str(cat)+"|"+str(product["rating"])+"|"+product['num_reviews']
                    makeupdatasaved = makeupdatasaved + "\n" + makeupdata
                with open("./sephora/sephora"+"_"+str(cat)+".csv", 'a') as f:
                    f.write (makeupdatasaved)
                    """w = csv.writer(f, encoding='utf-8')
                    w.writerow(unicode(makeupdatasaved))"""
                time.sleep(5)



driver.service.process.send_signal(signal.SIGTERM) # kill the specific phantomjs child proc
driver.quit() 
