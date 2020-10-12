import gps
import time
from ISStreamer.Streamer import Streamer
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import sys, traceback
from sys import exit


geolocator = Nominatim()
session = gps.gps("127.0.0.1", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
publish_data = Streamer(bucket_name="GPS KSA", bucket_key="4GAXRFTVSCRX", access_key="ist_-fO177NPqe3zGv2KprvMZ7N-hb-zFkK4") 


time_1=None
i =0; j =0
lat = []
lon = []


while True:
	try:

    		raw_data = session.next()
		if i<3 and j<3:
			if raw_data['class'] == 'TPV':
				if hasattr(raw_data,'lat') and hasattr(raw_data,'lon'):
					lat.append(raw_data.lat)
					lon.append(raw_data.lon)
					i += 1
					j += 1

		else:
			if raw_data['class'] == 'TPV':
				if hasattr(raw_data,'time'):
					if raw_data.time != time:
						time_1 = raw_data.time
						publish_data.log("Time",raw_data.time)
						print "The curent date and time is = "+str(raw_data.time)


						if raw_data['class'] =='TPV':
							if hasattr(raw_data,'lat') and hasattr(raw_data,'lon'):
								lat[0] = lat[1];  lon[0] = lon[1]
								lat[1] = lat[2];  lon[1] = lon[2]
								lat[2] = raw_data.lat; lon[2] = raw_data.lon
								ave_lat = (lat[0] + lat[1] + lat[2])/3
								ave_lon = (lon[0] + lon[1] + lon[2])/3
								publish_data.log("Location", "{lat},{lon}".format(lat=ave_lat,lon=ave_lon))
								print "Latitude  =  ", ave_lat,",    Longitude   =  ",ave_lon
								coordinates = str(ave_lat)+ "," + str(ave_lon)
								location = geolocator.reverse(coordinates,timeout=10)
								publish_data.log("Object is located at",location.address)
								print "Location: ", (location.address)


						if raw_data['class'] =='TPV':
							if hasattr(raw_data,'speed'):
								speed_mps= format((raw_data.speed/3.6), ".2f")
								speed_kmh= format((raw_data.speed), ".2f")
								publish_data.log("Speed of the object", speed_mps)
								publish_data.log("Speed of the object", speed_kmh)
								print "Object speed  =", speed_mps," mps or ", speed_kmh,"kmh"


						if raw_data['class'] =='TPV':
							if hasattr(raw_data,'alt'):
								publish_data.log("Altitude",raw_data.alt)
								print "The altitude is = "+str(raw_data.alt)+" m/n/n"
								raw_data = session.next()


	except GeocoderTimedOut as e:
		pass
	except KeyError:
		pass
	except (KeyboardInterrupt, SystemExit):
		publish_data.close()
		print "\nEnding the current process"
		gps.running = False
		exit()
		quit()
	except StopIteration:
		session = None
		print "No incoming data from the GPS module"

