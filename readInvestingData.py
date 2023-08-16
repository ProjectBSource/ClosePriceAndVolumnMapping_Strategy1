import csv

dates = []
close_prices = []
open_prices = []
highs = []
lows = []
volumes = []
percentage_changes = []

csv_file_path = '/Users/patrickfung/Downloads/DowJonesHistorialData.csv'
outputFile  = '/Users/patrickfung/Downloads/outputFile.csv'

def read_csv_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        
        for row in reader:
            date = row[0].strip('"')
            close_price = float(row[1].replace(',', '').strip('"'))
            open_price = float(row[2].replace(',', '').strip('"'))
            high = float(row[3].replace(',', '').strip('"'))
            low = float(row[4].replace(',', '').strip('"'))
            volume = row[5].strip('"')
            percentage_change = row[6].strip('"')

            dates.append(date)
            close_prices.append(close_price)
            open_prices.append(open_price)
            highs.append(high)
            lows.append(low)
            volumes.append(volume)
            percentage_changes.append(percentage_change)

    # Print the lists
    #print("Dates:", dates)
    #print("Close Prices:", close_prices)
    #print("Open Prices:", open_prices)
    #print("Highs:", highs)
    #print("Lows:", lows)
    #print("Volumes:", volumes)
    #print("Percentage Changes:", percentage_changes)
    
def calculateEachClosePriceSumupVolumn():
    min_close_price = int(min(close_prices))
    max_close_price = int(max(close_prices))
    close_price_list = list(range(min_close_price, max_close_price+1))
    for i in range(0, len(dates), 1):
        tempVolumns = volumes[i].replace("K", "")
        if(tempVolumns != None and tempVolumns != ""):
            close_price_list[ int(close_prices[i]) - min_close_price ] += float(volumes[i].replace("K", ""))*1000;
    with open(outputFile, 'w') as file:
        for i in range(len(close_price_list)-1, 0, -1):
            file.write("\"{a}\",\"{b}\"\n".format(a = str(min_close_price+i), b = str(close_price_list[i])))
        
    
    

# Example usage
read_csv_file(csv_file_path)
calculateEachClosePriceSumupVolumn();
