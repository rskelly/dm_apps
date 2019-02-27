import xlsxwriter as xlsxwriter
from django.template.defaultfilters import yesno
from django.utils import timezone
from django.conf import settings

from lib.functions.nz import nz
from lib.templatetags.verbose_names import get_verbose_label
from . import models
import os


def generate_capacity_spreadsheet(fy=None, orgs=None):
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'ihub', 'temp')
    target_file = "temp_data_export_{}.xlsx".format(timezone.now().strftime("%Y-%m-%d"))
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'ihub', 'temp', target_file)

    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)

    # create formatting
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#D6D1C0', "align": 'normal', "text_wrap": True})
    total_format = workbook.add_format({'bold': True, "align": 'left', "text_wrap": True, 'num_format': '$#,##0'})
    normal_format = workbook.add_format({"align": 'left', "text_wrap": True, 'num_format': '$#,##0'})

    # get an entry list for the fiscal year (if any)
    if fy:
        entry_list = models.Entry.objects.filter(fiscal_year=fy)
    else:
        entry_list = models.Entry.objects.all()

    # define the header
    header = [
        get_verbose_label(entry_list.first(), 'fiscal_year'),
        get_verbose_label(entry_list.first(), 'title'),
        get_verbose_label(entry_list.first(), 'organizations'),
        get_verbose_label(entry_list.first(), 'status'),
        get_verbose_label(entry_list.first(), 'sectors'),
        get_verbose_label(entry_list.first(), 'entry_type'),
        get_verbose_label(entry_list.first(), 'initial_date'),
        get_verbose_label(entry_list.first(), 'regions'),
        get_verbose_label(entry_list.first(), 'funding_needed'),
        get_verbose_label(entry_list.first(), 'funding_purpose'),
        get_verbose_label(entry_list.first(), 'amount_requested'),
        get_verbose_label(entry_list.first(), 'amount_approved'),
        get_verbose_label(entry_list.first(), 'amount_transferred'),
        get_verbose_label(entry_list.first(), 'amount_lapsed'),
        "Amount outstanding",
    ]

    # worksheets #
    ##############

    # each org should be represented on a separate worksheet
    # therefore determine an appropriate org list
    if orgs:
        org_list = [models.Organization.objects.get(pk=int(o)) for o in orgs.split(",")]
    else:
        org_list = models.Organization.objects.all()

    for org in org_list:
        if org.entries.count() > 0:
            my_ws = workbook.add_worksheet(name=org.abbrev)

            # create the col_max column to store the length of each header
            # should be a maximum column width to 100
            col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]
            my_ws.write_row(0, 0, header, header_format)

            tot_requested = 0
            tot_approved = 0
            tot_transferred = 0
            tot_lapsed = 0
            tot_outstanding = 0
            i = 1
            for e in entry_list.filter(organizations=org):

                if e.organizations.count() > 0:
                    orgs = str([str(obj) for obj in e.organizations.all()]).replace("[", "").replace("]", "").replace("'", "").replace('"',
                                                                                                                                       "")
                else:
                    orgs = None

                if e.sectors.count() > 0:
                    sectors = str([str(obj) for obj in e.sectors.all()]).replace("[", "").replace("]", "").replace("'", "").replace('"', "")
                else:
                    sectors = None

                if e.regions.count() > 0:
                    regions = str([str(obj) for obj in e.regions.all()]).replace("[", "").replace("]", "").replace("'", "").replace('"', "")
                else:
                    regions = None

                data_row = [
                    e.fiscal_year,
                    e.title,
                    orgs,
                    str(e.status),
                    sectors,
                    str(e.entry_type),
                    e.initial_date.strftime("%Y-%m-%d"),
                    regions,
                    yesno(e.funding_needed),
                    nz(str(e.funding_purpose), ""),
                    nz(e.amount_requested, 0),
                    nz(e.amount_approved, 0),
                    nz(e.amount_transferred, 0),
                    nz(e.amount_lapsed, 0),
                    nz(e.amount_outstanding, 0),
                ]

                tot_requested += nz(e.amount_requested, 0)
                tot_approved += nz(e.amount_approved, 0)
                tot_transferred += nz(e.amount_transferred, 0)
                tot_lapsed += nz(e.amount_lapsed, 0)
                tot_outstanding += nz(e.amount_outstanding, 0)

                # adjust the width of the columns based on the max string length in each col
                ## replace col_max[j] if str length j is bigger than stored value

                j = 0
                for d in data_row:
                    # if new value > stored value... replace stored value
                    if len(str(d)) > col_max[j]:
                        if len(str(d)) < 100:
                            col_max[j] = len(str(d))
                        else:
                            col_max[j] = 100
                    j += 1

                my_ws.write_row(i, 0, data_row, normal_format)
                i += 1

            # set column widths
            for j in range(0, len(col_max)):
                my_ws.set_column(j, j, width=col_max[j] * 1.1)

            # set formatting on currency columns
            # my_ws.set_column(first_col=10, last_col=10, cell_format=money_format)
            # my_ws.set_column(header.index("Funding requested"), header.index("Funding requested"), cell_format=money_format)
            # my_ws.set_column(header.index("Funding approved"), header.index("Funding approved"), cell_format=money_format)
            # my_ws.set_column(header.index("Amount transferred"), header.index("Amount transferred"), cell_format=money_format)
            # my_ws.set_column(header.index("Amount lapsed"), header.index("Amount lapsed"), cell_format=money_format)
            # my_ws.set_column(header.index("Amount outstanding"), header.index("Amount outstanding"), cell_format=money_format)

            # sum all the currency columns
            total_row = [
                "GRAND TOTAL:",
                tot_requested,
                tot_approved,
                tot_transferred,
                tot_lapsed,
                tot_outstanding,
            ]
            my_ws.write_row(i + 2, header.index("Funding requested") - 1, total_row, total_format)

            # set formatting for status
            for status in models.Status.objects.all():
                my_ws.conditional_format(0, header.index("Status"), i, header.index("Status"),
                                         {
                                             'type': 'cell',
                                             'criteria': 'equal to',
                                             'value': '"{}"'.format(status.name),
                                             'format': workbook.add_format({'bg_color': status.color, }),
                                         })

            # set formatting for entry type
            for entry_type in models.EntryType.objects.all():
                my_ws.conditional_format(0, header.index("Entry type"), i, header.index("Entry type"),
                                         {
                                             'type': 'cell',
                                             'criteria': 'equal to',
                                             'value': '"{}"'.format(entry_type.name),
                                             'format': workbook.add_format({'bg_color': entry_type.color, }),
                                         })

    workbook.close()
    return target_url
