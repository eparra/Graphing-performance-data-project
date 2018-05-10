# Data Graphing Project

## Task description

I needs to create .jpg/.png graphs images from data in postges, using Django’s management command.  The Django models and sample data are below (the actual data is truncated; just a subset is shown).  Please review the data before reading any further.  

We will build two graphs per location.  The first graph will use avg_resp_proxy data and the second will use avg_resp_direct data.  Based on the date specified, the code should query measurements for the amount of days requested, for each proxy.  If there are less days in the database than requested, the graph should only use the dates available.  To explain the X and Y columns, the Y column is milliseconds and the X columns are dates (although the graph below shows time, we will only use dates).  Although the timestamps in the database have more than 2 decimal points, these can be rounded, as shown in the example graph below:

# Some minor changes

1. In Measurement location field changed to ForeignKey field to allow store more than one measure per location

```
class Measurement(models.Model):
    location = models.ForeignKey('locations.Location', on_delete=models.CASCADE)
    proxy            = models.CharField(('proxy'), max_length=10)
    avg_resp_proxy   = models.CharField(('avg_resp_proxy'), max_length=20)
    avg_avail_proxy  = models.CharField(('Average available proxy'), max_length=20)
    avg_resp_direct  = models.CharField(('avg_resp_direct'), max_length=20)
    avg_avail_direct = models.CharField(('Average available direct'), max_length=20)
    date             = models.DateField(auto_now=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return '{} - {}'.format(self.date, self.location.city)
```

2. Using matplotlib instead https://plot.ly/python/. In this task only need to create static files with management
commands, so using plot.ly in this case will be overhead.

3. If only one measure available - drawing only one dot, if none data available - image didnt create, if more one data created - drawing simple graph.

# Installation

We use project in docker container for fast installation. So you need docker and doccker-compose packages installed.
Please refer https://docs.docker.com/install/linux/docker-ce/ubuntu/ and https://docs.docker.com/compose/install/ for installation procedures.

Copy env_default file to .env and edit parameters.
```
cp env_defaul .env
nano .env
```

Build image
```
docker-compose build
```

Start project with
```
docker-compose up -d
```

Docker starts two containers - graphic-web and graphic-db

# Load initial data
Initial test data can be loaded with:

```
cat graphic.sql | docker exec --user=postgres -i graphic-db  psql -U postgres
```

# Change password for admin

```
$ docker exec -ti graphic-web python manage.py changepassword admin
Changing password for user 'admin'
Password:
Password (again):
Password changed successfully for user 'admin'
```


# CLI syntax

Example of creating needed images:
Data in format dd/mm/yyyy
```
docker exec -ti graphic-web python manage.py build-images --date=02/03/2018 --days=4
```
By default graphic images created in ../data/ directory. You can change location in .env in DATA_DIR variable.
