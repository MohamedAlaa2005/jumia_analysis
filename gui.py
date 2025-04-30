import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
from datetime import date
import pandas as pd
import streamlit as st
from docx import Document
import streamlit as st
from streamlit_option_menu import option_menu
from vega_datasets import data
import os
from pdf2image import convert_from_bytes
from streamlit_pdf_viewer import pdf_viewer
import requests
from bs4 import BeautifulSoup
import re
import streamlit.components.v1 as components
import seaborn as sns
with st.sidebar:
    selected = option_menu("Menu", 
    ["webscraping code", "DataFrame file", "Data Analysis", "Visual representations", "Team Member"], 
    icons=["code-slash","file-earmark-spreadsheet", "bar-chart", "image", "people-fill"], 
    menu_icon="cast", 
    default_index=0
)

# Handle different options based on the selected menu item
if selected == "webscraping code":
    st.markdown("<h1 style='text-align: center;'>Web Scraping Code</h1>", unsafe_allow_html=True)
    code = '''
    import requests
    import streamlit as st

    jumia_url = "https://www.jumia.com.eg/"
    page = requests.get(jumia_url)  # send a request to the page.
    st.write(page)  # to get the response of the page.
    '''
    st.code(code, language='python')
    st.write("Response [200]")
    code = '''
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
def scrape_category(url):
    products = []
    for page in range(1, 16):  # Loop through the first 15 pages.
        page_url = f"{url}?page={page}"  # Construct the page URL.
        res = requests.get(page_url, headers=headers)
        soupp = BeautifulSoup(res.content, 'html.parser')
        if(soupp.get_text()[:10]=='No results'):
            break
        for link in soupp.find_all('a', class_='core'):
            href = link.get('href')
            if href and href.startswith('/'):
                #product page
                full_link = 'https://www.jumia.com.eg' + href
                response = requests.get(full_link, headers=headers)
                soup = BeautifulSoup(response.content, "html.parser")
                target_divs = soup.find_all("div", class_="-phs")
                product=str(target_divs[2].get_text(strip=True))
                if re.search(r"Brand:([^|]+)", product) is  None and product[0:3]!='EGP':
                    continue
                #extract seller
                seller = soup.find_all("div", class_="-hr -pas")
                for div in seller:
                    text = div.get_text(strip=True)
                    match = re.match(r'^(.*?)\d+%', text)
                    if match:
                        seller_name = match.group(1)
                        # 1. Product Name
                product_name = soup.find('h1', {'class': '-fs20'}).text.strip() if soup.find('h1', {'class': '-fs20'}) else "N/A"
                        # 2. Discount
                discount = soup.find('span', {'class': 'bdg _dsct _dyn -mls'}).text.strip() if soup.find('span', {'class': 'bdg _dsct _dyn -mls'}) else "0%" 
                        # 3. Current & Original Price
                current_price = soup.find('span', {'class': '-b'}).text.strip() if soup.find('span', {'class': '-b'}) else "N/A"
                if discount=="0%":
                    original_price = current_price
                else:
                    original_price = soup.select_one('span.-tal.-gy5.-lthr, span[aria-label="Original price"]').get_text(strip=True)

                        # 4. Brand
                if re.search(r"Brand:([^|]+)", product):
                    brand=str(re.findall(r"Brand:([^|]+)", product)[0])
                else:
                    brand="Unknown Brand"
                        #5. rating   
                rating = str(re.findall(r"(\d+\.?\d*)\s*out of 5", product)[0]) 
                        # 5. Reviews

                reviews = soup.find('a', {'class': '-plxs'}).text.strip() if soup.find('a', {'class': '-plxs'}) else "0 reviews"

                        # 6. Availability
                stock = soup.find('span', {'class': 'bdg _invert _xs'}).text.strip() if soup.find('span', {'class': 'bdg _invert _xs'}) else "Available"
                         # 8. SKU
                SKU = soup.find_all("li", class_="-pvxs")
                if SKU ==[]:
                    continue
                for item in SKU:
                    Product_id = re.search(r'SKU</span>:\s*([A-Z0-9]+)',str(item))
                    if Product_id:
                        break
                        #9
                breadcrumb_links = soup.select('div.brcbs a')
                if len(breadcrumb_links) > 1:
                    category = breadcrumb_links[1].text.strip()
                else:
                    continue
                        # Output Results
                products.append( {
                            "Product Name": product_name,
                            "Brand": brand,
                            "Current Price": current_price,
                            "Original Price": original_price,
                            "Discount": discount,
                            "Rating": rating,
                            "Reviews": reviews,
                            "Stock Status": stock,
                            "SellerInfo" : seller_name,
                            "CATEGORY" : category
                        })
    return products  
    '''
    st.code(code, language='python')
    code='''
categories = {
    "Fashion": "https://www.jumia.com.eg/category-fashion-by-jumia/",
    "Phones & Tablets": "https://www.jumia.com.eg/phones-tablets/",
    "Health & Beauty": "https://www.jumia.com.eg/health-beauty/",
    "Home & Furniture": "https://www.jumia.com.eg/home-office/",
    "Appliances" : "https://www.jumia.com.eg/mlp-category-appliances/",
    "Televisions & Audio" : "https://www.jumia.com.eg/electronic-television-video/",
    "Baby Products" : "https://www.jumia.com.eg/baby-products//",
    "Supermarket" : "https://www.jumia.com.eg/groceries/",
    "Computing" : "https://www.jumia.com.eg/computing/",
    "Sporting Goods" : "https://www.jumia.com.eg/sporting-goods/",
    "Gaming " : "https://www.jumia.com.eg/video-games/",
    "Electronics" : "https://www.jumia.com.eg/electronics/",
    "Automobile" : "https://www.jumia.com.eg/automobile/",
    "Industrial & Scientific": "https://www.jumia.com.eg/industrial-scientific/",
    "Hand Crafted" : "https://www.jumia.com.eg/mlp-ebda3-men-masr-store/",
    " Books,Movies, and Music" : "https://www.jumia.com.eg/books-movies-music/"
}
all_products = []
for name, link in categories.items():
    print(f"Scraping {name}...")
    all_products.extend(scrape_category(link))  # limit to 2 pages
print("Scraping Complete ✅ ")
# Save the data to a CSV file
df=pd.DataFrame(all_products)
        ''' 
    output = '''
Scraping Fashion...\n
Scraping Phones & Tablets...\n
Scraping Health & Beauty...\n
Scraping Home & Furniture...\n
Scraping Televisions & Audio...\n
Scraping Baby Products...\n
Scraping Supermarket...\n
Scraping Computing...\n
Scraping Sporting Goods...\n
Scraping Gaming ...\n
Scraping Electronics...\n
Scraping Automobile...\n
Scraping Industrial & Scientific...\n
Scraping Hand Crafted...\n
Scraping  Books,Movies, and Music...\n
Scraping Complete ✅ 
    '''
    st.code(code, language='python')
    st.write(output)

elif selected == "DataFrame file":
# Displaying a header
    st.markdown("<h1 style='text-align: center;'>DataFrame File</h1>", unsafe_allow_html=True)
    # Load the dataset
    df = pd.read_csv(r"https://raw.githubusercontent.com/MohamedAlaa2005/jumia_analysis/refs/heads/main/scraping.csv")
    # Display the dataframe with custom column configuration
    st.dataframe(
        df
    )
elif selected == "Data Analysis":
    st.markdown("<h1 style='text-align: center;'>Data Analysis</h1>", unsafe_allow_html=True)
    tabs = st.tabs(["Report","Code"])
    with tabs[0]:
        url = "https://raw.githubusercontent.com/MohamedAlaa2005/jumia_analysis/refs/heads/main/Jumia%20Data%20Analysis%20Report.html"
        response = requests.get(url)
        source_code = response.text
        st.components.v1.html(source_code, height=11100)

    with tabs[1]:
        df = pd.read_csv(r"https://raw.githubusercontent.com/MohamedAlaa2005/jumia_analysis/6119e95058fa67441c817c965686c32705cdc1f8/Cleaned_Data.csv")
        df['Current Price Average'] = pd.to_numeric(df['Current Price Average'], errors='coerce')
        df['Original Price Average'] = pd.to_numeric(df['Original Price Average'], errors='coerce')
        df['Discount Percentage'] = df['Discount'].str.replace('%', '').astype(float)
        with st.echo():
            basic_stats = df[['Current Price Average', 'Original Price Average', 'Discount Percentage', 'Rating', 'Reviews']].describe()
            st.subheader("Basic Statistical Summary:")
            st.dataframe(basic_stats)
        with st.echo():
            correlations = df[['Current Price Average', 'Original Price Average', 'Discount Percentage', 'Rating', 'Reviews']].corr()
            st.subheader("Correlation Matrix:")
            st.dataframe(correlations)
        with st.echo():
            rating_groups = df.groupby('Rating').agg({
                'Current Price Average': 'mean',
                'Reviews': 'mean',
                'Discount Percentage': 'mean'
            }).sort_index()
            
            st.subheader("Grouped Statistics by Rating:")
            st.dataframe(rating_groups)
        with st.echo():
            category_discounts = df.groupby('General_Category')['Discount Percentage'].mean().sort_values(ascending=False)
            st.subheader("Average Discount Percentage by Category:")
            st.dataframe(category_discounts)
        with st.echo():
            avg_prices = df.groupby('General_Category')['Current Price Average'].mean().sort_values()
            highest_avg_category = avg_prices.idxmax()
            lowest_avg_category = avg_prices.idxmin()
            highest_avg_price = avg_prices.max()
            lowest_avg_price = avg_prices.min()
            st.subheader("1. Average Prices by Category:")
            st.dataframe(avg_prices)
            st.write(f"**Highest Avg Price Category:** {highest_avg_category} (${highest_avg_price:.2f})")
            st.write(f"**Lowest Avg Price Category:** {lowest_avg_category} (${lowest_avg_price:.2f})")
        with st.echo():
            df['Price Drop'] = df['Original Price Average'] - df['Current Price Average']
            avg_discount = df['Discount Percentage'].mean()
            avg_price_drop = df['Price Drop'].mean()
            st.subheader("2. Discount Analysis:")
            st.write(f"**Average Discount Percentage:** {avg_discount:.2f}%")
            st.write(f"**Average Price Drop:** ${avg_price_drop:.2f}")
        with st.echo():
            rating_counts = df['Rating'].value_counts().sort_index()
            st.subheader("3. Rating Distribution:")
            st.dataframe(rating_counts)
        with st.echo():
            rated_df = df[df['Rating'] > 0]
            correlation = rated_df[['Rating', 'Current Price Average']].corr().iloc[0, 1]
            
            st.subheader("4. Rating vs. Price Correlation:")
            st.write(f"**Correlation between Rating and Current Price:** {correlation:.2f}")

elif selected == "Visual representations":
    st.markdown("<h1 style='text-align: center;'>Visual Representations</h1>", unsafe_allow_html=True)
    tabs = st.tabs(["pie", "bar Chart","heatmap", "Scatter Plot","box plot"])
    df = pd.read_csv(r"https://raw.githubusercontent.com/MohamedAlaa2005/jumia_analysis/6119e95058fa67441c817c965686c32705cdc1f8/Cleaned_Data.csv")
    with tabs[0]:
        is_discounted = len(df[df['Discount']!="0%"])
        not_discounted = len(df[df['Discount']=="0%"])
        st.subheader("Discounted Vs Non-Discounted Products",divider="blue")
        fig, ax = plt.subplots()
        fig.set_size_inches(3, 3)
        fig.patch.set_alpha(0)
        ax.pie([is_discounted,not_discounted],labels = ['Discounted', 'Non-Discounted'],autopct='%1.1f%%', colors=["#B68973","#FAF3E0"]) 
        ax.set_facecolor('none') 
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        st.write(fig)
    with tabs[1]:
        st.subheader("Top 10 Categories by Product Count",divider="blue")
        top_categories = df['CATEGORY'].value_counts().nlargest(10)
        fig, ax = plt.subplots()
        fig.set_size_inches(8, 5)
        fig.patch.set_alpha(0)
        ax.bar(top_categories.index, top_categories.values, color="#983d3d")  # primary color for bars
        ax.set_facecolor('none') 
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        ax.set_xlabel('Category') 
        ax.set_xticklabels(top_categories.index, rotation=45, ha='right')
        ax.set_ylabel('Number of Products') 
        st.write(fig)
        st.subheader("Top 10 Brands by Total Reviews",divider="blue")
        top_brands_reviews = df.groupby('Brand')['Reviews'].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots()
        fig.set_size_inches(8, 5)
        fig.patch.set_alpha(0)
        ax.bar(top_brands_reviews.index, top_brands_reviews.values, color="#983d3d")  # primary color for bars
        ax.set_facecolor('none') 
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        ax.set_xlabel('Brand') 
        ax.set_xticklabels(top_brands_reviews.index, rotation=45, ha='right')
        ax.set_ylabel('Total Reviews') 
        st.write(fig)
        st.subheader("Stock Status per Category",divider="blue")
        stock_counts = df.groupby(['CATEGORY', 'Stock Status']).size().reset_index(name='Counts')
        fig, ax = plt.subplots()
        fig.set_size_inches(8, 5)
        fig.patch.set_alpha(0)
        ax.bar(stock_counts['CATEGORY'], stock_counts['Counts'], color="#983d3d")
        ax.set_facecolor('none') 
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        ax.set_xlabel('Category') 
        ax.set_xticklabels( stock_counts['CATEGORY'],rotation=45, ha='right')
        ax.set_ylabel('Number of Products') 
        st.write(fig)
    with tabs[2]:
        primaryColor = "#983d3d"
        backgroundColor = "#393939"
        secondaryBackgroundColor = "#2d2d2d"
        textColor = "#92a1ff"
        sns.set(style="darkgrid", palette="muted")
        top10 = df.groupby('CATEGORY')['Current Price Average'].mean().nlargest(10)
        heat = pd.DataFrame(top10).reset_index() 
        st.title('Heatmap of Mean Price Trends')
        st.markdown('This heatmap shows the top 10 categories based on mean price trends.')
        fig, ax = plt.subplots(figsize=(10, 3), facecolor=backgroundColor)
        sns.heatmap(heat.set_index('CATEGORY').T, annot=True, cmap='Oranges', cbar_kws={'label': 'Price'},
                    linewidths=0.5, linecolor=primaryColor, annot_kws={'color': textColor})
        ax.set_title("Mean Price Trends across Categories", fontsize=16, color=textColor)
        ax.set_xlabel('Category', fontsize=12, color=textColor)
        ax.set_ylabel('Mean Price', fontsize=12, color=textColor)
        plt.gcf().set_facecolor(backgroundColor)
        plt.xticks(color=textColor)
        plt.yticks(color=textColor)
        plt.tight_layout()
        st.pyplot(fig)
    with tabs[3]:
        st.subheader("the relationship between Average price and rating correlation",divider="blue")
        fig, ax = plt.subplots()
        fig.set_size_inches(8, 5)
        fig.patch.set_alpha(0)
        ax.scatter(df["Current Price Average"],df["Rating"], color="#983d3d")  # primary color for bars
        ax.set_facecolor('none') 
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        ax.set_xlabel("Price") 
        ax.set_ylabel("Rating") 
        st.write(fig)
    with tabs[4]:
        st.subheader("Box Plot for Current Price Average",divider="blue")
        fig, ax = plt.subplots()
        fig.set_size_inches(8, 5)
        fig.patch.set_alpha(0)
        ax.boxplot(df['Current Price Average']) # primary color for bars
        ax.set_facecolor('none') 
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        ax.set_ylabel('Current Price Average') 
        st.write(fig)
elif selected == "Team Member":
    st.markdown("<h1 style='text-align: center;'>Team Member👥</h1>", unsafe_allow_html=True)
    # Define team data
    team = [
        {
            "first_name": "Mohamed",
            "last_name": "Alaa",
            "role": "Gui and Data Storage",
            "bio": "Storage Data in mongodb and make Gui use Streamlit",
        },
        {
            "first_name": "Mostafa",
            "last_name": "El-Hosseny",
            "role": "Data Analysis",
            "bio": "Find pattern and relationship in data",
        },
        {
            "first_name": "Mariam",
            "last_name": "Mohamed",
            "role": "Data Visualization",
            "bio": "Make graphical representation to information and data",
        },
        {

            "first_name": "Maryam",
            "last_name": "Mahmoud",
            "role": "Data Extraction and Data preprocessing",
            "bio": "Extract Data by use Web Scraping and Make Data preprocessing ",
        },

    ]

    # Layout: 3 columns
    cols = st.columns(3)

    # Render team cards
    for idx, member in enumerate(team):
        with cols[idx % 3]:
            st.markdown(f"""
                <div style="padding: 15px; background-color: #2d2d2d; border-radius: 12px; margin-bottom: 20px; border-left: 4px solid #983d3d;">
                    <h4 style="margin-bottom: 5px; color: #92a1ff;">{member['first_name']}<br>{member['last_name']}</h4>
                    <p style="color: #bbbbbb; margin-top: 0; font-weight: bold;">{member['role']}</p>
                    <p style="font-size: 14px; color: #cccccc;">{member['bio']}</p>
                </div>
            """, unsafe_allow_html=True)