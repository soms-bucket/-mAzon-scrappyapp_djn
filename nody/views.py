from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import sqlite3

# Create your views here.

#data_dict=dict()
#data_dict=None

def home(request):
	data_dict=None
	top_dict=None
	data_dict_1=None
	if 'product' in request.GET:

		Pro=request.GET.get('product')

		#Create and extract data
		#data_dict=boom(Pro)
		#print(boom(Pro))
		#data_dict=None


		try:

			conn = sqlite3.connect('nody/amazon_scrap.db')
			c = conn.cursor()
			#delete table
			#c.execute('''DROP TABLE ultimate''')

			#create a table
			c.execute('''CREATE TABLE ultimate(Website_ text,Product_Link text,Product_Name text,Product_Brand text,Rating_ int,Save_Price text,Price_ int,MRP_ int,Primary_Image_Link text)''')

			Website_=[]
			Product_Link=[]
			Product_Name=[]
			Product_Brand=[]
			Price_=[]
			MRP_=[]
			Rating_=[]
			Save_Price=[]
			Primary_Image_Link=[]


			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
			# the company page you're about to scrape
			#url = "https://www.myntra.com/men-clothings?p=2000&plaEnabled=false"
			###########for men_cl in range(1000):
			url="https://www.amazon.in/s?bbn=976419031&rh=n%3A976419031%2Cp_89%3Arealme&dc&qid=1624216249&rnid=3837712031&ref=lp_976420031_nr_p_89_3"
			#print(men_cl+1)
			#open the page
			page_request = requests.get(url, headers=headers)

			#page_request = requests.get(url, headers=headers)


			soup = bs(page_request.text,"lxml")
			#print(soup)
			#########################

			#Product name
			pr_name_lst=soup.findAll('span',{'class':"a-size-base-plus a-color-base a-text-normal"})

			#print(len(pri))
			for pr_n in range(len(pr_name_lst)):
				nm_org=pr_name_lst[pr_n].text

				#Product name Update #*#*#*#*#*#*
				nm_org1=nm_org.split(" ")[:3]
				nm_org2=""

				for org in nm_org1:
					nm_org2 +=""+org+" "

				#print(nm_org2+"\n")
				
				Product_Name.append(nm_org2.strip().lower())

			#print(Product_Name)

			###################

			#Product Website
			for web_s in range(len(pr_name_lst)):
				Website_.append("https://www.amazon.in/")
			#print(Website_)


			######################################

			#Product Link

			pr_lnk_lst=soup.findAll('a',{'class':"a-link-normal a-text-normal"})
			#print(pr_lnk_lst)
			#print("https://www.amazon.in"+pr_lnk_lst[0].get("href"))

			for pr_ln in range(len(pr_lnk_lst)):
				pr_v="https://www.amazon.in"+pr_lnk_lst[pr_ln].get("href")
				Product_Link.append(pr_v)

			#print(Product_Link)

			###################################
			#Product Brand

			for prc_br in range(len(pr_name_lst)):
				Product_Brand.append("Realme")



			###############################################

			#Product Price
			for pr_ic in Product_Link:
				#print(type(pr_ic))
				#url=Product_Link[pr_ic]
				url=pr_ic
				#print(url)

				page_request = requests.get(url, headers=headers)

				soup_1 = bs(page_request.text,"lxml")

				#print(soup_1)

				#product Price
				try:
					try:

						prc_1=soup_1.find('span',{'class':"a-size-medium a-color-price priceBlockDealPriceString"})
						
						Price_.append(prc_1.text[1:-3])  #product Price
						#print(prc_1.text[1:-3])
						#print("11111")

						

					except:
						
						prc_2=soup_1.find('span',{'class':"a-size-medium a-color-price priceBlockBuyingPriceString"})

						Price_.append(prc_2.text[1:-3])
						#print(prc_2.text[1:-3])
						#print("2222")

				except:
					#print("gooo,,,")
					Price_.append("Curently Unavailable")

				#PRODUCT MRP

				#priceBlockStrikePriceString a-text-strike
				try:

					prc_mrp=soup_1.find('span',{'class':"priceBlockStrikePriceString a-text-strike"})

					MRP_.append(prc_mrp.text[2:-3])
					#print(prc_mrp.text[2:-3]+"\n")
				except:
					MRP_.append("Curently Unavailable")
					#print("Curently Unavailable\n")



				###############################################

				#Save Price
				try:

					prc_svprc=soup_1.find('td',{'class':"a-span12 a-color-price a-size-base priceBlockSavingsString"})
					
					Save_Price.append(prc_svprc.text.strip()[1:])
					#print(prc_svprc.text.strip()[1:]+"\n")
				except:
					Save_Price.append("Curently Unavailable")
					#print("Curently Unavailable\n")






			######################################
			#Rating
				
			prc_rat_lst=soup.findAll('a',{'class':"a-popover-trigger a-declarative"})

			#MRP_.append(prc_mrp.text[2:-3])
			#print(len(prc_rat))
			for pr_rate in range(len(prc_rat_lst)):
				
				p_rte1=float(prc_rat_lst[pr_rate].text[:3])
				Rating_.append(p_rte1)
				#print(p_rte1)

			###############################################
			#Primary Image Link

			#a-section aok-relative s-image-square-aspect
			prc_img_lst=soup.findAll('img',{'class':"s-image"})

			#print(len(prc_img_lst))
			for pro_img in range(len(prc_img_lst)):
				#print(prc_img_lst[pro_img].get("src"))

				pro_img_1=prc_img_lst[pro_img].get("src")
				Primary_Image_Link.append(pro_img_1)




			#print(Primary_Image_Link)

			for ddd in range(len(Website_)):

				c.execute('''INSERT INTO ultimate VALUES(?,?,?,?,?,?,?,?,?)''', (Website_[ddd],Product_Link[ddd],Product_Name[ddd],Product_Brand[ddd],Rating_[ddd],Save_Price[ddd],Price_[ddd],MRP_[ddd],Primary_Image_Link[ddd]))
				conn.commit()

			#select all data from table and #print
			conn = sqlite3.connect('nody/amazon_scrap.db')
			c = conn.cursor()

			#####################################"RealMe 360 deg"
			a=Pro
			a=a.lower().replace(" ","")
			a_lst=[a[k] for k in range(len(a))]
			#print("soommm")
			#print(len(a_lst))
			p=0
			data_dict=dict()



			#select all data from table and #print
			c.execute('''SELECT * FROM ultimate''')
			results = c.fetchall()
			#print(results[0])

			for i in range(len(results)):

				#print(results[i][2])
				res_each=results[i][2].replace(" ","")
				#print("boom boom")	
				#print(len(res_each))

				try:
					#print("try")
					for j in range(len(res_each)):
							#print(j)
							
						if res_each[j]==a_lst[j]:
							p+=1


				except:
					p=0
					#print("ecee")

					#print("none")

					
					for j in range(len(a_lst)):
							#print(j)
							
						if res_each[j]==a_lst[j]:
							p+=1

				#print("value of p:"+str(p))
				
				if p>=9:

					#print(results[i])
					
					data_dict={'Website':results[i][0],
						'Product_Link':results[i][1],
						'Product_Name':results[i][2],
						'Product_Brand':results[i][3],
						'Product_Rating':results[i][4],
						'Price':results[i][6],
						'MRP':results[i][7],
						'Product_Save_Price':results[i][5],
						'Primary_Image_Link':results[i][8]}

					#print(data_dict["Website"])

				p=0
			#return data_dict

			conn.close()
			

		except:

			conn = sqlite3.connect('nody/amazon_scrap.db')
			c = conn.cursor()

			#"RealMe 360 deg"
			a=Pro
			a=a.lower().replace(" ","")
			a_lst=[a[k] for k in range(len(a))]
			#print("soommm")
			#print(len(a_lst))
			p=0
			data_dict=dict()



			#select all data from table and #print
			c.execute('''SELECT * FROM ultimate''')
			results = c.fetchall()
			#print(results[0])

			for i in range(len(results)):

				#print(results[i][2])
				res_each=results[i][2].replace(" ","")
				#print("boom boom")	
				#print(len(res_each))

				try:
					#print("try")
					for j in range(len(res_each)):
							#print(j)
							
						if res_each[j]==a_lst[j]:
							p+=1


				except:
					p=0
					#print("ecee")

					#print("none")

					
					for j in range(len(a_lst)):
							#print(j)
							
						if res_each[j]==a_lst[j]:
							p+=1

				#print("value of p:"+str(p))
				
				if p>=8 or a == "realme":
					#print(results[i])
					
					data_dict={'Website':results[i][0],
						'Product_Link':results[i][1],
						'Product_Name':results[i][2],
						'Product_Brand':results[i][3],
						'Product_Rating':results[i][4],
						'Price':results[i][6],
						'MRP':results[i][7],
						'Product_Save_Price':results[i][5],
						'Primary_Image_Link':results[i][8]}
					break

					#print(data_dict["Website"])
				
					#data_dict_1=dict()
				else:
					data_dict=""


				p=0

			data_dict_1={'not_f' : "Product you find Not stored in Our Database"}

			#return data_dict
			conn.close()
			
			
			############################################
			#top product 
			rt_rate=[]
			rt_name=[]
			top_dict=dict()

			#print(results[0][4])
			#print(results[0][2])
			for jgh in range(len(results)):
				rt_rate.append(results[jgh][4])
				rt_name.append(results[jgh][2])

			#rt_rate.sort(reverse = True)
			#print(rt_rate)
			#print(rt_name)

			bk_rating=[]
			basic=5
			mn=0.0
			count=0

			while(count<8):


				for loki in range(len(rt_rate)):
					if rt_rate[loki] == basic - mn:
							bk_rating.append(str(rt_rate[loki])+" rating on "+rt_name[loki])
							count += 1

					if 5==len(bk_rating):break

				mn +=0.1



			#print("\n\n\n\n\n")
			#print(tuple(bk_rating)[5])
			bk_rating=sorted(set(bk_rating))[::-1]
			#print(bk_rating[4])
			top_dict={'top_1':bk_rating[0],
						'top_2':bk_rating[1],
						'top_3':bk_rating[2],
						'top_4':bk_rating[3],
						'top_5':bk_rating[4]}

			#print(top_dict)


	#data_dict=dict()
	if data_dict != "" :
		return render(request, 'nody/home.html', {'result': data_dict ,'res' : top_dict} )

	else:
		return render(request, 'nody/home.html', {'result_1': data_dict_1 ,'res' : top_dict} )
