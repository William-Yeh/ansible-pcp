#!/usr/bin/env python
#
# Check if specified PMDAs have been installed already.
#
# USAGE:
#     progname  <pmcd.conf path>  [list of PMDAs...]
#
#
# @see http://www.pcp.io/books/PCP_UAG/html/LE63226-PARENT.html
#

import sys
import re


pmcd_conf_path = ""

pmda_to_be_checked = []
pmda_already_installed = []
pmda_need_to_be_installed = []


# argv[] sent from Ansible
#
REGEX_PMDA_LIST = re.compile('^\s*\[([^\]]+)\]\s*$')

# Performance Metrics Domain Specifications
# Format:
#     label_name   domain_number   type   path
# @see http://www.pcp.io/books/PCP_UAG/html/LE63226-PARENT.html
REGEX_PMDS_ENTRY = re.compile('^\s*([^\s]+)\s+\d+.*$')


def report_error_cmdline():
    print '{ "ok": false }'
    sys.exit(1)


def report_error_file_reading():
    print '{ "ok": false, "msg": "error reading pmcd.conf file" }'
    sys.exit(1)


def report_not_changed():
    print '{ "ok": true, "changed": false }'
    sys.exit(0)


def report_changed():
    pmda_data = ','.join(pmda_need_to_be_installed)
    print '{ "ok": true, "changed": true, "add": [ %s ] }' % pmda_data
    sys.exit(0)


def process_cmdline():
    if len(sys.argv) < 2:
        report_error_cmdline()
    if len(sys.argv) < 3:
        report_not_changed()

    global pmcd_conf_path
    pmcd_conf_path = sys.argv[1]

    m = REGEX_PMDA_LIST.match(''.join(sys.argv[2:]))
    if m is None:
        report_not_changed()
    pmda_args = m.group(1).split(',')
    if len(pmda_args) < 1:
        report_not_changed()

    global pmda_to_be_checked
    for item in pmda_args:
        pmda_to_be_checked.append(item.strip())


def read_pmcd_conf():
    global pmda_already_installed

    try:
        f = open(pmcd_conf_path, "r")
        for line in f.readlines():
            m = REGEX_PMDS_ENTRY.match(line)
            if m is not None:
                pmda_already_installed.append(m.group(1))
        f.close()
    except IOError:
        report_error_file_reading()
    # pmda_already_installed.sort()
    # print pmda_already_installed


def check_all_pmda():
    diff = set(pmda_to_be_checked) - set(pmda_already_installed)
    #print pmda_to_be_checked
    #print pmda_already_installed
    #print diff

    global pmda_need_to_be_installed
    for item in diff:
        item_string = '"{0}"'.format(item)  # surround with double quote
        pmda_need_to_be_installed.append(item_string)


process_cmdline()
read_pmcd_conf()
check_all_pmda()
if len(pmda_need_to_be_installed) > 0:
    report_changed()
else:
    report_not_changed()
