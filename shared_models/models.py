from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


# CONNECTED APPS: dm_tickets, travel, projects, sci_fi
class FiscalYear(models.Model):
    full = models.TextField(blank=True, null=True)
    short = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.full)

    class Meta:
        ordering = ['id', ]


# CONNECTED APPS: masterlist
# STILL NEED TO CONNECT: camp (needs remapping), grais (needs remapping)
class Province(models.Model):
    # Choices for surface_type
    CAN = 'Canada'
    US = 'United States'
    COUNTRY_CHOICES = (
        (CAN, _('Canada')),
        (US, _('United States')),
    )
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("name (French)"))
    abbrev_eng = models.CharField(max_length=25, blank=True, null=True, verbose_name=_("abbreviation (English)"))
    abbrev_fre = models.CharField(max_length=25, blank=True, null=True, verbose_name=_("abbreviation (French)"))
    country = models.CharField(max_length=25, choices=COUNTRY_CHOICES, verbose_name=_("country"))
    # meta
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


# CONNECTED APPS: masterlist
class Region(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Name (French)"))
    abbrev = models.CharField(max_length=10, verbose_name=_("abbreviation"))
    # meta
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class Branch(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Name (French)"))
    abbrev = models.CharField(max_length=10, verbose_name=_("abbreviation"))
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, verbose_name=_("region"))
    # meta
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{} ({})".format(getattr(self, str(_("name"))), self.region)
        # if there is no translated term, just pull from the english field
        else:
            return "{} ({})".format(self.name, self.region)

    class Meta:
        ordering = ['name', ]


class Division(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("name (French)"))
    abbrev = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("abbreviation"))
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING, verbose_name=_("branch"))
    # meta
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{} ({})".format(getattr(self, str(_("name"))), self.branch.region)
        # if there is no translated term, just pull from the english field
        else:
            return "{} ({})".format(self.name, self.branch.region)

    class Meta:
        ordering = ['name', ]


# CONNECTED APPS: dm_tickets, travel, projects
# STILL NEED TO CONNECT: inventory
class Section(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("name (French)"))
    division = models.ForeignKey(Division, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="sections")
    head = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("section head"),
                             related_name="shared_models_sections")
    abbrev = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("abbreviation"))
    # meta
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]

    @property
    def full_name(self):
        my_str = "{} - {} - {} - {}".format(self.division.branch.region.name, self.division.branch.name, self.division.name, self.name)
        return my_str



class AllotmentCategory(models.Model):
    name = models.CharField(max_length=25)
    color = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


# CONNECTED APPS: projects
# STILL NEED TO CONNECT: scifi
class AllotmentCode(models.Model):
    # choices for category
    SAL = "salary"
    CAP = "capital"
    OM = "om"
    GC = "gc"
    CBASE = "cbase"
    CATEGORY_CHOICES = (
        (SAL, "Salary"),
        (CAP, "Capital"),
        (OM, "O&M"),
        (CBASE, "Cbase"),
        (GC, "G&C"),
    )
    code = models.CharField(max_length=50, unique=True)
    name = models.TextField(blank=True, null=True)
    # category = models.CharField(max_length=25, choices=CATEGORY_CHOICES, default="other")
    allotment_category = models.ForeignKey(AllotmentCategory, on_delete=models.DO_NOTHING, related_name="allotment_codes", blank=True,
                                           null=True)

    def __str__(self):
        return "{} ({})".format(self.code, self.name)

    class Meta:
        ordering = ['code', ]


# CONNECTED APPS:
# STILL NEED TO CONNECT: scifi
class BusinessLine(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.code, self.name)

    class Meta:
        ordering = ['code', ]


# CONNECTED APPS:
# STILL NEED TO CONNECT: scifi
class LineObject(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name_eng = models.CharField(max_length=1000)
    description_eng = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.code, self.name_eng)

    class Meta:
        ordering = ['code', ]


# CONNECTED APPS: projects
# STILL NEED TO CONNECT: scifi
class ResponsibilityCenter(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.TextField(blank=True, null=True)
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True,)

    def __str__(self):
        return "{} ({})".format(self.code, self.name)

    class Meta:
        ordering = ['code', ]


# CONNECTED APPS: projects
# STILL NEED TO CONNECT: scifi
class Project(models.Model):
    name = models.CharField(max_length=1000)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    project_lead = models.CharField(max_length=500, blank=True, null=True)
    default_responsibility_center = models.ForeignKey(ResponsibilityCenter, on_delete=models.DO_NOTHING, blank=True,
                                                      null=True, related_name='projects')
    default_allotment_code = models.ForeignKey(AllotmentCode, on_delete=models.DO_NOTHING, blank=True, null=True)
    default_business_line = models.ForeignKey(BusinessLine, on_delete=models.DO_NOTHING, blank=True, null=True)
    default_line_object = models.ForeignKey(LineObject, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.code, self.name)

    class Meta:
        ordering = ['code', ]


########################


class Probe(models.Model):
    name = models.CharField(max_length=255)
    nom = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class Institute(models.Model):
    name = models.CharField(max_length=255)
    nom = models.CharField(max_length=255, blank=True, null=True)
    abbrev = models.CharField(max_length=255, verbose_name=_("abbreviation"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class Vessel(models.Model):
    name = models.CharField(max_length=255)
    call_sign = models.CharField(max_length=56, null=True, blank=True)

    def __str__(self):
        if self.call_sign:
            return "{} {}".format(self.name, self.call_sign)
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


# oceanography
# diets
# snowcrab
class Cruise(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.DO_NOTHING, blank=True, null=True)
    mission_name = models.CharField(max_length=255)
    mission_number = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    chief_scientist = models.CharField(max_length=255)
    samplers = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    probe = models.ForeignKey(Probe, null=True, blank=True, on_delete=models.DO_NOTHING)
    area_of_operation = models.CharField(max_length=255, null=True, blank=True)
    number_of_profiles = models.IntegerField()
    meds_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="MEDS ID")
    notes = models.CharField(max_length=255, null=True, blank=True)
    season = models.IntegerField(null=True, blank=True)
    vessel = models.ForeignKey(Vessel, on_delete=models.DO_NOTHING, related_name="missions", blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.start_date:
            self.season = self.start_date.year
        return super().save(*args, **kwargs)

#########################################

# species model
# person
