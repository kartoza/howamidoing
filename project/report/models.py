# from django.contrib.gis.geos import fromstr
# from django.contrib.gis.db import models as gis
# from django.db import models
# from project.users.models import User
# from django.utils.translation import ugettext_lazy as _
# from .utils.scoring_grid import color_score_km_grid, status_score_km_grid
# import logging

# logger = logging.getLogger(__name__)


# class Status(models.Model):
#     """
#     Status used in report, e.g. 'All Well Here', 'We Need Medical Help', etc.
#     """
#     name = models.CharField(
#         help_text=_('Name of this status'),
#         max_length=50,
#         null=False,
#         blank=False,
#         default=''
#     )

#     description = models.TextField(
#         help_text=_('Brief description of this status'),
#         null=True,
#         blank=True,
#         default=None
#     )

#     def __str__(self):
#         return '{} | {}'.format(self.id, self.name)

#     class Meta:
#         ordering = ('name',)
#         verbose_name_plural = 'Statuses'


# class ReportQuerySet(models.QuerySet):
#     """Custom QuerySet for Report."""

#     def location_within(self, geojson_geometry_string):
#         geometry = fromstr(geojson_geometry_string, srid=4326)
#         return self.filter(
#             location__within=geometry
#         )

#     def status_contains(self, status_name):
#         return self.filter(
#             status__name__icontains=status_name
#         )

#     def green_report(self):
#         return self.status_contains('well')

#     def yellow_report(self):
#         return self.status_contains('food')

#     def red_report(self):
#         return self.status_contains('medic')


# class Report(models.Model):
#     """
#     Report about latest user status.
#     Everytime user renew their status, system will create a new Report instead of updating the old one.
#     """
#     location = gis.PointField(
#         help_text=_('Location of the report/user Location'),
#         null=True,
#         default=None,
#         blank=True
#     )

#     status = models.ForeignKey(
#         Status,
#         help_text=_('Status of this report'),
#         on_delete=models.CASCADE,
#         null=False,
#         blank=False
#     )

#     timestamp = models.DateTimeField(
#         help_text=_('Timestamp of report creation'),
#         auto_now_add=True
#     )

#     user = models.ForeignKey(
#         User,
#         help_text=_('Owner/user of this report'),
#         on_delete=models.CASCADE,
#         null=False,
#         blank=False
#     )

#     objects = ReportQuerySet.as_manager()

#     def __str__(self):
#         return '{} | {} | {} | {}'.format(self.id, self.location, self.timestamp, self.user.username)

#     class Meta:
#         ordering = ('-id',)


# class PopulatedKmGridManager(models.Manager):
#     """Custom version manager that shows only populated Grid."""

#     def get_query_set(self):
#         """Query set generator."""
#         return super(PopulatedKmGridManager, self).get_query_set().filter(
#             population__gt=0
#         )


# class KmGridQuerySet(models.QuerySet):
#     """Custom version manager for Grid."""

#     def geometry_contains(self, geojson_geometry_string):
#         geometry = fromstr(geojson_geometry_string, srid=4326)
#         return self.filter(
#             geometry__contains=geometry
#         )

#     def geometry_equals(self, geojson_geometry_string):
#         geometry = fromstr(geojson_geometry_string, srid=4326)
#         return self.filter(
#             geometry__equals=geometry
#         )


# class KmGrid(models.Model):
#     """
#     Model representing grid and its population number.
#     Data will be generated using Positgis and Worldpop.
#     """
#     geometry = gis.PolygonField(
#         help_text=_('Geometry of this grid'),
#         null=True,
#         blank=True,
#         default=None
#     )

#     population = models.IntegerField(
#         help_text=_('Number of people in this grid'),
#         null=False,
#         blank=False,
#         default=300
#     )

#     objects = KmGridQuerySet().as_manager()
#     populated_objects = PopulatedKmGridManager()

#     def __str__(self):
#         return '{} | {} | {}'.format(self.id, self.geometry, self.population)

#     class Meta:
#         # Temporarily set managed to False because we still don't know
#         # how to create the data
#         managed = True
#         ordering = ('-id',)


# class KmGridScoreQuerySet(KmGridQuerySet):
#     """Custom version manager for Grid."""

#     def geometry_contains(self, geojson_geometry_string):
#         geometry = fromstr(geojson_geometry_string, srid=4326)
#         return self.filter(
#             geometry__contains=geometry
#         )

#     def geometry_equals(self, geojson_geometry_string):
#         geometry = fromstr(geojson_geometry_string, srid=4326)
#         return self.filter(
#             geometry__equals=geometry
#         )

#     def green_grid(self):
#         return self.filter(total_score=0)

#     def yellow_grid(self):
#         return self.filter(total_score=1)

#     def red_grid(self):
#         return self.filter(total_score=2)

#     def grid_with_report(self):
#         return self.filter(total_report__gt=0)


# class KmGridScoreManager(models.Manager):
#     """Custom version manager for Grid Score."""

#     def get_queryset(self):
#         return KmGridQuerySet(self.model, using=self._db).filter(total_score__gt=0)

#     def geometry_contains(self, geojson_geometry_string):
#         geometry = fromstr(geojson_geometry_string, srid=4326)
#         return self.get_queryset().filter(
#             geometry__contains=geometry
#         )

#     def geometry_equals(self, geojson_geometry_string):
#         geometry = fromstr(geojson_geometry_string, srid=4326)
#         return self.get_queryset().filter(
#             geometry__equals=geometry
#         )

#     def green_grid(self):
#         return self.get_queryset().filter(total_score=0)

#     def yellow_grid(self):
#         return self.get_queryset().filter(total_score=1)

#     def red_grid(self):
#         return self.get_queryset().filter(total_score=2)

#     def grid_with_report(self):
#         return self.get_queryset().filter(total_report__gt=0)


# class KmGridScore(models.Model):
#     """
#     Materialized uiews for user status summary per grid
#     """
#     geometry = gis.PolygonField(
#         help_text=_('Geometry of this Grid'),
#         null=True,
#         blank=True,
#         default=None
#     )

#     score_green = models.DecimalField(
#         help_text=_('The score of user with latest "All is Well" status in this grid'),
#         max_digits=7,
#         decimal_places=2,
#         null=False,
#         blank=False,
#         default=0
#     )

#     count_green = models.SmallIntegerField(
#         help_text=_('The number of user with latest "All is Well" status in this grid'),
#         null=False,
#         blank=False,
#         default=0
#     )

#     score_yellow = models.DecimalField(
#         help_text=_('The score of user with latest "We need food or supplies" status in this grid'),
#         max_digits=7,
#         decimal_places=2,
#         null=False,
#         blank=False,
#         default=0
#     )

#     count_yellow = models.SmallIntegerField(
#         help_text=_('The number of user with latest "We need food or supplies" status'),
#         null=False,
#         blank=False,
#         default=0
#     )

#     score_red = models.DecimalField(
#         help_text=_('The score of user with latest "We need medical help" status in this grid'),
#         max_digits=7,
#         decimal_places=2,
#         null=False,
#         blank=False,
#         default=0
#     )

#     count_red = models.SmallIntegerField(
#         help_text=_('The number of user with latest "We need medical help" status in this grid'),
#         null=False,
#         blank=False,
#         default=0
#     )

#     population = models.IntegerField(
#         help_text=_('Number of people in this grid'),
#         null=False,
#         blank=False,
#         default=300
#     )

#     total_report = models.SmallIntegerField(
#         help_text=_('The number of all report in the grid'),
#         null=False,
#         blank=False,
#         default=0
#     )

#     total_score = models.DecimalField(
#         help_text=_('Total score of this grid'),
#         max_digits=7,
#         decimal_places=2,
#         null=False,
#         blank=False,
#         default=0
#     )

#     objects = KmGridScoreManager()

#     def __str__(self):
#         return '{} | {} | {} | {}'.format(self.id, self.geometry, self.population, self.total_score)

#     def set_color_score(self, color="green"):
#         score = color_score_km_grid(getattr(self, f'count_{color}'), self.population, color)
#         setattr(self, f'score_{color}', score)
#         self.save()

#     def set_total_score(self):
#         total_score = status_score_km_grid(
#             self.count_green,
#             self.count_yellow,
#             self.count_red,
#             self.population,
#         )

#         self.total_score = total_score
#         self.save()

#     class Meta:
#         # Set managed to False because this model will access existing Materialized Views
#         managed = True
#         ordering = ('-id',)
