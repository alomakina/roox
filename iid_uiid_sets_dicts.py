__author__ = 's-lomakina'
import sys
import json
import codecs
from os import listdir
from os.path import isfile
from os.path import join as joinpath
import time
import getopt


def get_dict(files, mypath, uiid_set, iid_set, verbose=True):
    """
    return:
    uiid_d - all uiid's records from the whole log (if such uiid in uiid samara set)
    iid_d -  all iid's records from the whole log (if such iid in iid samara set)
    """
    count_reports_all = 0
    uiid_d = {}
    iid_d = {}
    error_names = set()
    ts_in = 0
    ts_in_iid = 0

    for f in files[:]:
        if isfile(joinpath(mypath, f)):
            count_reports = 0
            with codecs.open(joinpath(mypath, f), 'r') as infile:
                for line in infile:
                    if 'YA_REPORT_RECEIVE_TIME' in line.rstrip('\n\r'):
                        count_reports += 1
                        count_reports_all += 1

                    elif '{"data"' in line.rstrip('\n\r'):
                        try:
                            js = json.loads(line.rstrip('\r\n'))
                            for x in xrange(len(js["data"])):
                                if js["data"][x]["name"] not in error_names:
                                    # if js["data"][x]["name"] == 'event.click':

                                    try:
                                        uiid = js["data"][x]["data"].get("uiid")
                                        iid = js["data"][x]["data"].get("iid")

                                        if uiid:
                                            if uiid in uiid_set:
                                                    uiid_d.setdefault(uiid, {})
                                                    timeStart = js["data"][x].get("timeStart")
                                                    timeEnd = js["data"][x].get("timeEnd")

                                                    if timeStart and timeEnd:
                                                        timeStart_d = {}
                                                        uiid_d[uiid].setdefault((int(timeStart),int(timeEnd)), [])
                                                        timeStart_d["name"] = js["data"][x]["name"]

                                                        for k in js["data"][x]["data"].keys():
                                                            if k != "uiid":
                                                                timeStart_d[k] = js["data"][x]["data"][k]
                                                        if timeStart_d in uiid_d[uiid][(int(timeStart),int(timeEnd))]:
                                                            ts_in += 1
                                                        else:
                                                            uiid_d[uiid][(int(timeStart),int(timeEnd))].append(timeStart_d)
                                        if iid:
                                            if iid in iid_set:
                                                iid_d.setdefault(iid, {})
                                                timeStart = js["data"][x].get("timeStart")
                                                timeEnd = js["data"][x].get("timeEnd")

                                                if timeStart and timeEnd:
                                                    timeStart_d = {}
                                                    iid_d[iid].setdefault((int(timeStart), int(timeEnd)), [])
                                                    timeStart_d["name"] = js["data"][x]["name"]

                                                    for k in js["data"][x]["data"].keys():
                                                        if k != "iid":
                                                            timeStart_d[k] = js["data"][x]["data"][k]
                                                    if timeStart_d in iid_d[iid][(int(timeStart), int(timeEnd))]:
                                                        ts_in += 1
                                                    else:
                                                        iid_d[iid][(int(timeStart), int(timeEnd))].append(timeStart_d)
                                    except:
                                        error_names.add(js["data"][x]["name"])
                        except ValueError:
                            continue
            if verbose:
                print 'count_reports file, ', count_reports, f
            infile.close()
    if verbose:
        print 'count_reports all, ', count_reports_all
        print 'error_names:\n', error_names
        print 'ts_in:\n', ts_in
        print 'ts_in_iid:\n', ts_in_iid

    return uiid_d, iid_d


def get_set(files, mypath):
    """
    uiid_set - 'mts-my-options' in history
    iid_set - 'mts-my-options' in history
    uiid_set_only_samara - 'samara.mts' in history
    iid_set_only_samara - 'samara.mts' in history

    error_names - error in parsing json to dict
    """
    count_reports_all = 0
    uiid_set = set()
    uiid_set_only_samara = set()
    iid_set = set()
    iid_set_only_samara = set()

    error_names = set()
    count_reports_all = 0
    for f in files[:]:
        if isfile(joinpath(mypath, f)):
            count_reports = 0
            with codecs.open(joinpath(mypath, f), 'r') as infile:
                for line in infile:
                    if 'YA_REPORT_RECEIVE_TIME' in line.rstrip('\n\r'):
                        count_reports += 1
                        count_reports_all += 1

                    elif '{"data"' in line.rstrip('\n\r'):

                        try:
                            js = json.loads(line.rstrip('\r\n'))
                            for x in xrange(len(js["data"])):
                                if js["data"][x]["name"] not in error_names:
                                    try:
                                        uiid = js["data"][x]["data"].get("uiid")
                                        iid = js["data"][x]["data"].get("iid")

                                        if uiid:
                                            for k, v in js["data"][x]["data"].items():
                                                    if k == 'w' and v == 'mts-my-options':
                                                        uiid_set.add(uiid)
                                                    if 'samara.mts' in str(v):
                                                        uiid_set_only_samara.add(uiid)
                                        if iid:
                                            for k, v in js["data"][x]["data"].items():
                                                if k == 'w' and v == 'mts-my-options':
                                                    iid_set.add(iid)
                                                if 'samara.mts' in str(v):
                                                    iid_set_only_samara.add(iid)
                                    except:
                                        error_names.add(js["data"][x]["name"])
                        except ValueError:
                            continue
            print 'count_reports file, ', count_reports, f
            infile.close()

    return uiid_set, iid_set, uiid_set_only_samara, iid_set_only_samara


def main(argv=None):
    if argv == None:
        argv = sys.argv

    mypath = "/home/s-lomakina/tests/unzip_dir"
    files = listdir("/home/s-lomakina/tests/unzip_dir")
    verbose = True

    try:
        opts, args = getopt.getopt(argv[1:], 'p:v:')
    except getopt.GetoptError, err:
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-p':
            mypath = arg
        if opt == '-v':
            verbose = arg

    if verbose:
        print time.asctime(), 'start getting Sets'

    uiid_set, iid_set, uiid_set_only_samara, iid_set_only_samara = get_set(files, mypath)

    if verbose:
        print 'len(uiid_set), ', len(uiid_set)
        print 'len(iid_set), ', len(iid_set)
        print 'len(uiid_set_only_samara), ', len(uiid_set_only_samara)
        print 'len(iid_set_only_samara), ', len(iid_set_only_samara)
        print time.asctime(), 'sets are collected!'
        print len(uiid_set.intersection(uiid_set_only_samara))
        print time.asctime(), 'Start getting dicts!'


    uiid_dict, iid_d = get_dict(files, mypath, uiid_set, iid_set, verbose)

    del uiid_set
    del iid_set
    del uiid_set_only_samara
    del iid_set_only_samara

    if verbose:
        print 'len(uiid_dict)', len(uiid_dict)
        print 'len(iid_d)', len(iid_d)
        print time.asctime(), 'Dicts are collected!'

    out_f = 'iid_1day_samara_dict.txt'
    with open(out_f, 'w') as outfile:
        for iid in iid_d:
            tss = iid_d[iid].keys()
            tss.sort()
            for t in tss:
                for value in iid_d[iid][t]:
                    outfile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (iid, t[0], t[1], value.get("uiid"), value.get("name"), value.get("w"), json.dumps(value, ensure_ascii=False)))
    outfile.close()

    out_f = 'uiid_1day_samara_dict.txt'
    with open(out_f, 'w') as outfile:
        for uiid in uiid_dict:
            tss = uiid_dict[uiid].keys()
            tss.sort()
            for t in tss:
                for value in uiid_dict[uiid][t]:
                    outfile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (uiid, t[0], t[1], value.get("iid"), value.get("name"), value.get("w"), json.dumps(value, ensure_ascii=False)))
    outfile.close()

    
if __name__ == "__main__":
    main()