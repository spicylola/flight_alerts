import sys
import requests
import json
import json
from lxml import html


required_keys =['arrival_date','arrival_time']

# TODO: Dont forget to make ability to parse args for the script
source='Atlanta'
destination = 'Miami'
departure='05/20/2019'

# Example URL
# https://www.expedia.com/Flights-Search?trip=oneway&leg1=from:Atlanta,to:Miami,departure:04/12/2019TANYT&passengers=adults:1,children:0,seniors:0,infantinlap:Y&options=cabinclass%3Aeconomy&mode=search&origref=www.expedia.com
flight_url = "https://www.expedia.com/Flights-Search?trip=oneway&leg1=from:{0},to:{1},departure:{2}TANYT&passengers=adults:1,children:0,seniors:0,infantinlap:Y&options=cabinclass%3Aeconomy&mode=search&origref=www.expedia.com".format(source,destination,departure)
headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
resp = requests.get(flight_url, headers=headers, verify=False)

# This is just me looking at XMLs, thinking of storing them to cache data
parser = html.fromstring(resp.content)
#outfile = open('results.html', "w")
#outfile.write(str(resp.content))
#outfile.close()
json_data_xpath = parser.xpath("//script[@id='cachedResultsJson']//text()")
raw_json =json.loads(json_data_xpath[0] if json_data_xpath else '')
flight_data = json.loads(raw_json["content"])

test_data = flight_data['legs']['AA1177coach2019-05-20T06:53-04:00ATL2019-05-20T08:51-04:00MIA596']
for item in test_data:
    print("key: "+item)
    print("value: "+ str(test_data[item]))
#
for elt in flight_data:
   each_flight = flight_data['elt']
   for item in each_flight:
       flight_info = {}
       # Must be populated, validations

       # Arrival Info
       flight_info['arrival_date'] = item['arrival_date'].get('date',None)
       flight_info['arrival_time'] = item['arrival_date'].get('time', None)

       # Carrier Info
       flight_info['is_next_day_arrival'] = item['carrierSummary'].get('nextDayArrival', None)
       flight_info['airline_name'] = item['carrierSummary'].get('airlineName', None)
       flight_info['is_multistop'] = item['carrierSummary'].get('multiStop', None)
       flight_info['num_of_tickets_left'] = item['carrierSummary'].get('noOfTicketsLeft')

       # Duration Info
       flight_info['duration_hour'] = item['duration'].get('hours', None)
       flight_info['duration_mins'] = item['duration'].get('minutes', None)

       # Maybe Depature Location info
       flight_info['airport_city'] = item['depatureLocation'].get('airportCity')
       flight_info['airport_code'] = item['depatureLocation'].get('airportCode')

       # Timeline Info
       timeline_info = item['timeline']
       # Arrival Airport
       flight_info['city'] = timeline_info['arrivalAirport'].get('city', None)
       flight_info['full_airport_name'] = timeline_info['arrivalAirport'].get('longName', None)








   key: timeline
   value: [{'layover': False,
            'arrivalAirport': {'code': 'MIA', 'longName': 'Miami, FL (MIA-Miami Intl.)', 'city': 'Miami',
                               'name': 'Miami (Miami Intl.)', 'airportCityState': 'Miami, FL',
                               'localName': 'Miami Intl.'}, 'segment': True,
            'distance': {'total': 596, 'unit': 'mi', 'formattedTotal': '596'},
            'carrier': {'operatedBy': '', 'seatMapAvailable': True, 'airlineImageFileName': 'AA.gif',
                        'operatedByAirlineCode': '', 'airlineCode': 'AA', 'showCabinClass': True,
                        'flightNumber': '1177', 'airlineName': 'American Airlines', 'planeCode': '319',
                        'airlineImageFileNameWithoutExtension': 'AA', 'bookingCode': 'B', 'plane': 'Airbus A319',
                        'cabinClass': '3'}, 'brandedFareName': None,
            'departureTime': {'hour': None, 'time': '6:53am', 'isoStr': '2019-05-20T06:53:00-04:00',
                              'date': '5/20/2019', 'dateLongStr': 'Mon, May 20', 'travelDate': '05/20/19',
                              'dateTime': 1558349580000},
            'departureAirport': {'code': 'ATL', 'longName': 'Atlanta, GA (ATL-Hartsfield-Jackson Atlanta Intl.)',
                                 'city': 'Atlanta', 'name': 'Atlanta (Hartsfield-Jackson Atlanta Intl.)',
                                 'airportCityState': 'Atlanta, GA', 'localName': 'Hartsfield-Jackson Atlanta Intl.'},
            'meals': [],
            'duration': {'hours': 1, 'departureTimeOfDay': '', 'numOfDays': 0, 'arrivalTimeOfDay': '', 'minutes': 58},
            'type': 'Segment',
            'arrivalTime': {'hour': None, 'time': '8:51am', 'isoStr': '2019-05-20T08:51:00-04:00', 'date': '5/20/2019',
                            'dateLongStr': 'Mon, May 20', 'travelDate': '05/20/19', 'dateTime': 1558356660000}}]

key: price
value: {'hasFare': True, 'roundedBestPriceDelta': None, 'formattedPriceWithCreditCardFeesEstimate': '', 'flightFareTypeCode': 'P', 'formattedRoundedBestPriceDelta': None, 'currencyCode': 'USD', 'priceIllegal': False, 'flightFareTypeValue': 1, 'totalPriceAsDecimal': 222.6, 'formattedPrice': '$111.30', 'totalPriceAsDecimalString': '222.6', 'bestPriceDelta': 0.0, 'localizedCurrencyCode': 'USD', 'formattedTotalPrice': '$222.60', 'pricedFlight': False, 'formattedRoundedTotalPrice': '$223', 'exactPrice': 111.3, 'formattedBestPriceDelta': None, 'formattedRoundedPrice': '$112', 'earnGPSRewards': None, 'offerPrice': 112.0, 'hasFees': False, 'feesMessage': {'showHandBaggageOnlyMsg': False, 'bringFreeCheckedBags': False, 'showBaggageFeeNotIncludedMsg': False, 'isShowFreeCancellation': True, 'airlineBasedBaggageAllowance': 0, 'baggageAllowance': '', 'matchDataAirProvider': True, 'isShowBestPriceGuarantee': False, 'isFlightIneligibleForBPG': False, 'showOBFeeDetailLink': False, 'bringOneFreeCheckedBag': False, 'showBaggageFeeIncludedMsg': False, 'showLCCBaggageAllowanceMsg': False, 'showBaggageFeeOnPurchaseMsg': False, 'showOBFeeMessageForLeg': False, 'freeCancellationTimeLimit': 0, 'showFirstCheckedBagIncludedMsg': False, 'specialFareMessage': '', 'showCheckedBagIncludedMsg': False, 'payFeeForBagMsg': False, 'apacFreeCancellation': False, 'nextGenContentWithLink': False}}
key: naturalKey
value: AA1177coach2019-05-20T06:53-04:00ATL2019-05-20T08:51-04:00MIA596
key: departureTime
value: {'hour': None, 'time': '6:53am', 'isoStr': '2019-05-20T06:53:00-04:00', 'date': '5/20/2019', 'dateLongStr': 'Mon, May 20', 'travelDate': '05/20/19', 'dateTime': 1558349580000}
key: index
value: 0
key: hotelAdjustedDatesModel
value: None
key: partnerLoyaltyBrandedFare
value: None
key: basicEconomy
value: {'enabled': True, 'rules': [{'airlineName': 'American Airlines', 'ruleLocIds': ['onePersonalItemNoOverheadAccess', 'seatsAssignedAtCheckin', 'noUpgrades', 'changesNotPermitted', 'boardInLastGroup'], 'airlineCode': 'AA', 'ruleLocIdsFsr': ['onePersonalItemNoOverheadAccess', 'seatsAssignedAtCheckin', 'noUpgrades', 'changesNotPermitted', 'boardInLastGroup']}], 'areaOneTrip': True}
key: arrivalLocation
value: {'airportCity': 'Miami', 'airportCode': 'MIA'}
key: stops
value: 0
key: amenityInfo
value: None
key: restrictiveFare
value: None
key: formattedDistance
value: 596
key: unformattedDistance
value: 596
key: formattedStops
value: 0

# import json
# import requests
# from lxml import html
# from collections import OrderedDict
# import argparse
#
#
# def parse(source, destination, date):
#     for i in range(5):
#         try:
#             url = "https://www.expedia.com/Flights-Search?trip=oneway&leg1=from:{0},to:{1},departure:{2}TANYT&passengers=adults:1,children:0,seniors:0,infantinlap:Y&options=cabinclass%3Aeconomy&mode=search&origref=www.expedia.com".format(
#                 source, destination, date)
#             headers = {
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
#             response = requests.get(url, headers=headers, verify=False)
#             parser = html.fromstring(response.text)
#             json_data_xpath = parser.xpath("//script[@id='cachedResultsJson']//text()")
#             raw_json = json.loads(json_data_xpath[0] if json_data_xpath else '')
#             flight_data = json.loads(raw_json["content"])
#
#             flight_info = OrderedDict()
#             lists = []
#
#             for i in flight_data['legs'].keys():
#                 total_distance = flight_data['legs'][i].get("formattedDistance", '')
#                 exact_price = flight_data['legs'][i].get('price', {}).get('totalPriceAsDecimal', '')
#
#                 departure_location_airport = flight_data['legs'][i].get('departureLocation', {}).get('airportLongName',
#                                                                                                      '')
#                 departure_location_city = flight_data['legs'][i].get('departureLocation', {}).get('airportCity', '')
#                 departure_location_airport_code = flight_data['legs'][i].get('departureLocation', {}).get('airportCode',
#                                                                                                           '')
#
#                 arrival_location_airport = flight_data['legs'][i].get('arrivalLocation', {}).get('airportLongName', '')
#                 arrival_location_airport_code = flight_data['legs'][i].get('arrivalLocation', {}).get('airportCode', '')
#                 arrival_location_city = flight_data['legs'][i].get('arrivalLocation', {}).get('airportCity', '')
#                 airline_name = flight_data['legs'][i].get('carrierSummary', {}).get('airlineName', '')
#
#                 no_of_stops = flight_data['legs'][i].get("stops", "")
#                 flight_duration = flight_data['legs'][i].get('duration', {})
#                 flight_hour = flight_duration.get('hours', '')
#                 flight_minutes = flight_duration.get('minutes', '')
#                 flight_days = flight_duration.get('numOfDays', '')
#
#                 if no_of_stops == 0:
#                     stop = "Nonstop"
#                 else:
#                     stop = str(no_of_stops) + ' Stop'
#
#                 total_flight_duration = "{0} days {1} hours {2} minutes".format(flight_days, flight_hour,
#                                                                                 flight_minutes)
#                 departure = departure_location_airport + ", " + departure_location_city
#                 arrival = arrival_location_airport + ", " + arrival_location_city
#                 carrier = flight_data['legs'][i].get('timeline', [])[0].get('carrier', {})
#                 plane = carrier.get('plane', '')
#                 plane_code = carrier.get('planeCode', '')
#                 formatted_price = "{0:.2f}".format(exact_price)
#
#                 if not airline_name:
#                     airline_name = carrier.get('operatedBy', '')
#
#                 timings = []
#                 for timeline in flight_data['legs'][i].get('timeline', {}):
#                     if 'departureAirport' in timeline.keys():
#                         departure_airport = timeline['departureAirport'].get('longName', '')
#                         departure_time = timeline['departureTime'].get('time', '')
#                         arrival_airport = timeline.get('arrivalAirport', {}).get('longName', '')
#                         arrival_time = timeline.get('arrivalTime', {}).get('time', '')
#                         flight_timing = {
#                             'departure_airport': departure_airport,
#                             'departure_time': departure_time,
#                             'arrival_airport': arrival_airport,
#                             'arrival_time': arrival_time
#                         }
#                         timings.append(flight_timing)
#
#                 flight_info = {'stops': stop,
#                                'ticket price': formatted_price,
#                                'departure': departure,
#                                'arrival': arrival,
#                                'flight duration': total_flight_duration,
#                                'airline': airline_name,
#                                'plane': plane,
#                                'timings': timings,
#                                'plane code': plane_code
#                                }
#                 lists.append(flight_info)
#             sortedlist = sorted(lists, key=lambda k: k['ticket price'], reverse=False)
#             return sortedlist
#
#         except ValueError:
#             print ("Rerying...")
#
#         return {"error": "failed to process the page", }
#
#
# if __name__ == "__main__":
#     argparser = argparse.ArgumentParser()
#     argparser.add_argument('source', help='Source airport code')
#     argparser.add_argument('destination', help='Destination airport code')
#     argparser.add_argument('date', help='MM/DD/YYYY')
#
#     args = argparser.parse_args()
#     source = args.source
#     destination = args.destination
#     date = args.date
#     print ("Fetching flight details")
#     scraped_data = parse(source, destination, date)
#     print ("Writing data to output file")
#     with open('%s-%s-flight-results.json' % (source, destination), 'w') as fp:
#         json.dump(scraped_data, fp, indent=4)
