import os
import matplotlib

matplotlib.use('Agg')

from django.conf import settings
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num
from locations.models import Location, Measurement

FILE_FORMAT = '{location}-{proxy_name}-{type}.{ext}'


class LocationsGraph(object):
    def __init__(self, **kwargs):
        self.from_date = kwargs.get('from_date')
        self.to_date = kwargs.get('to_date')
        self.from_date_p = date2num(kwargs.get('from_date'))
        self.to_date_p = date2num(kwargs.get('to_date'))

    def get_graphs(self):
        # Get all locations
        for location in Location.objects.all():
            city = location.city.replace(' ', '_')
            # Get all proxies in location
            for proxy in Measurement.objects.filter(
                    location=location).values_list('proxy',
                                                   flat=True).distinct():
                img_meta = {
                    'location': city,
                    'proxy_name': proxy,
                    'ext': 'png'
                }

                y1 = []
                y2 = []
                x = []
                for data in Measurement.objects.filter(
                        location=location,
                        proxy=proxy,
                        date__gte=self.from_date,
                        date__lte=self.to_date):
                    y1.append(float(data.avg_resp_proxy))
                    y2.append(float(data.avg_resp_direct))
                    x.append(date2num(data.date))

                # If none data is available - just skip creating data
                if y1:
                    img_meta['type'] = 'proxy'
                    filename_proxy = os.path.join(settings.DATA_DIR,
                                                  FILE_FORMAT.format(
                                                      **img_meta))
                    print('Create file {}'.format(filename_proxy))
                    plt.gcf().clear()
                    plt.gca().xaxis.set_major_formatter(
                        mdates.DateFormatter('%m/%d/%y'))
                    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
                    # If data consists of one measurement - we draw only one dot
                    if len(y1) == 1:
                        plt.plot(x, y1, 'bo')
                    else:
                        plt.plot(x, y1, 'b-')
                    plt.title('avg_resp_proxy')
                    plt.xlabel('dates')
                    plt.ylabel('milliseconds')
                    plt.gcf().autofmt_xdate()
                    plt.savefig(filename_proxy)

                # If none data is available - just skip creating data
                if y2:
                    img_meta['type'] = 'direct'
                    filename_direct = os.path.join(settings.DATA_DIR,
                                                   FILE_FORMAT.format(
                                                       **img_meta))
                    print('Create file {}'.format(filename_direct))
                    plt.gcf().clear()
                    plt.gca().xaxis.set_major_formatter(
                        mdates.DateFormatter('%m/%d/%y'))
                    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
                    # If data consists of one measurement - we draw only one dot
                    if len(y1) == 1:
                        plt.plot(x, y2, 'bo')
                    else:
                        plt.plot(x, y2, 'b-')
                    plt.title('avg_resp_direct')
                    plt.xlabel('dates')
                    plt.ylabel('milliseconds')
                    plt.gcf().autofmt_xdate()
                    plt.savefig(filename_direct)
