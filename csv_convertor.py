from bs4 import BeautifulSoup
import os
import pandas as pd
dict={"Name":[],"Make":[],"Model":[],"Build_Date":[],"Odometer":[],"Body_type":[],"Fuel":[],"Transmission":[],"Seats":[],"Provider":[],"Location":[],"Vin":[],"Price":[]}    
for file in os.listdir('html_data'):
    try:
        with open(f"html_data/{file}") as f:
            html_doc=f.read()
        soup=BeautifulSoup(html_doc,'html.parser')
        print(soup.prettify())

        # Extract the title
        title_tag=soup.find('tr', {'data-value': 'Title'})
        td_elements_t = title_tag.find_all('td')
        title=td_elements_t[1].text
        # print(title)
        dict["Name"].append(title)

        if title:
            year = title[:4]
            split_title = title.split(' ')
            make = split_title[1] if len(split_title) > 1 else None
            model = split_title[2] if len(split_title) > 1 else None
        else:
            year, make, model = None, None, None

        dict["Build_Date"].append(year)
        dict["Make"].append(make)
        dict["Model"].append(model)
        
        #Extracting the price
        price_tag=soup.find('tr', {'data-value': 'Price'})
        price=None
        if price_tag:
            span_elements_p = price_tag.find('span', 'details-vehicle-info-price-special')
            if span_elements_p:
                price= span_elements_p.text[1:]  # Remove the currency symbol
        dict["Price"].append(price)

        #Extracting the odometer
        odo_tag= soup.find('tr', {'data-value': 'Odometer'})
        odometer= None
        if odo_tag:
            td_elements_odo = odo_tag.find_all('td')
            if len(td_elements_odo) > 1:
                odometer = td_elements_odo[1].text.strip()
        dict["Odometer"].append(odometer)

        #Extracting transmission
        Transmission= soup.find('tr', {'data-value': 'Transmission'})
        transmission= None
        if Transmission:
            td_elements_trans= Transmission.find_all('td')
            if len(td_elements_trans) > 1:
                transmission= td_elements_trans[1].text.strip()
        dict["Transmission"].append(transmission)

        #Extracting fuel typoe
        Fuel= soup.find('tr', {'data-value': 'Fuel'})
        fuel= None
        if Fuel:
            td_elements_fuel= Fuel.find_all('td')
            if len(td_elements_fuel) > 1:
                fuel= td_elements_fuel[1].text.strip()
        dict["Fuel"].append(fuel)

        #Extracting body type
        Body_t= soup.find('tr', {'data-value': 'Body'})
        body_type = None
        if Body_t:
            td_elements_body = Body_t.find_all('td')
            if len(td_elements_body) > 1:
                body_type = td_elements_body[1].text.strip()
        dict["Body_type"].append(body_type)

        #Extracting number of seats
        Seat= soup.find('tr', {'data-value': 'SeatCapacity'})
        seats= None
        if Seat:
            td_elements_seat = Seat.find_all('td')
            if len(td_elements_seat) > 1:
                seats = td_elements_seat[1].text.strip()
        dict["Seats"].append(seats)

        #Extracting provider
        provider= soup.find('div', {'class': 'body'})
        provider_name =None
        if provider:
            bold_text=provider.find('b')
            if bold_text:
                provider_name= bold_text.text.strip()
        dict["Provider"].append(provider_name)

        #Extracting location
        location=None
        if provider:
            loc= provider.find('p')
            if loc:
                p_text= loc.get_text(separator="\n")
                split_tex = p_text.split('\n')
                if len(split_tex) > 3:
                    thd_line = split_tex[3].strip()
                    first_word = thd_line.split()[0]
                    location = first_word[:-1] 
        dict["Location"].append(location)

        #Extracting VIN
        Vin = soup.find('tr', {'data-value': 'VIN'})
        vin = None
        if Vin:
            td_elements_vin = Vin.find_all('td')
            if len(td_elements_vin) > 1:
                vin = td_elements_vin[1].text.strip()
        dict["Vin"].append(vin)

        # Print the dictionary for the current file (optional)
        # print(dict)
        #break

    except Exception as e:
        for key in dict.keys():
            dict[key].append(None)
df=pd.DataFrame(dict)
print(df)
csv=pd.read_csv("Scrapped_data_copy.csv")
dfc=pd.DataFrame(csv)
print(dfc)
com_df = pd.concat([df,dfc],axis=1)
print (com_df)

com_df.to_csv("Scrapped_data.csv", index=False)
    
    