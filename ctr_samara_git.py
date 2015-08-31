__author__ = 's-lomakina'
import json

"""
input files with user's history format:
iid \t time_start, time_end, uiid, event type, widget name, json(all other information about event from log)
"""


def count_main_shows_clicks_simple(f):
    """
    Shows:
    Use 'services'/'mts-my-options' w.displays ONLY
    divide into:
        - with 'samara.mts' in puri
        - with 'lk.ssl' in puri
        - with any other url in puri
        - with empty/without puri


    Clicks:
    Use 'services'/'mts-my-options' event.click ONLY
    with check, what puri the widget had before click event (use dictionary):
    divide into:
        - with 'samara.mts' in puri
        - with 'lk.ssl' in puri
        - with any other url in puri
        - with empty/without puri

    """

    count_dict = {}
    with open(f, 'r') as input_f:
        for line in input_f:
            iid, t_s, t_e, uuid, event, widget, other_j = line.rstrip('\n\r').split('\t')
            js = json.loads(other_j)
            count_dict.setdefault(iid,
                                  {"widget_displayed": {"services": False, "mts-my-options": False}, "display_count": 0,
                                   "click_count": 0,
                                   'seen_samara': False,

                                   "lk_widget_display_count": 0,
                                   "lk_widget_display": {"services": False, "mts-my-options": False},
                                   "lk_widget_click_count": 0,

                                   "other_puri_widget_display_count": 0,
                                   "other_puri_widget_display": {"services": False, "mts-my-options": False},
                                   "other_puri_widget_click_count": 0,

                                   "no_puri_widget_display_count": 0,
                                   "no_puri_widget_display": {"services": False, "mts-my-options": False},
                                   "no_puri_widget_click_count": 0})

            if widget == 'services':
                if event == 'widget.display':
                    puri = js.get("puri")
                    if puri:
                        if "samara.mts" in puri:
                            count_dict[iid]["seen_samara"] = True
                            count_dict[iid]["widget_displayed"][widget] = True
                            count_dict[iid]["display_count"] += 1
                        elif "lk." in puri:
                            count_dict[iid]["widget_displayed"][widget] = False
                            count_dict[iid]["other_puri_widget_display"][widget] = False
                            count_dict[iid]["no_puri_widget_display"][widget] = False

                            count_dict[iid]["lk_widget_display"][widget] = True
                            count_dict[iid]["lk_widget_display_count"] += 1
                        else:
                            count_dict[iid]["widget_displayed"][widget] = False
                            count_dict[iid]["lk_widget_display"][widget] = False
                            count_dict[iid]["no_puri_widget_display"][widget] = False

                            count_dict[iid]["other_puri_widget_display"][widget] = True
                            count_dict[iid]["other_puri_widget_display_count"] += 1
                    else:
                        # we do not know, where was the widget (samara/lk/anywhere)
                        count_dict[iid]["widget_displayed"][widget] = False
                        count_dict[iid]["lk_widget_display"][widget] = False
                        count_dict[iid]["other_puri_widget_display"][widget] = False

                        count_dict[iid]["no_puri_widget_display_count"] += 1
                        count_dict[iid]["no_puri_widget_display"][widget] = True

                elif event == "event.click":
                    if count_dict[iid]["widget_displayed"][widget]:
                        count_dict[iid]["click_count"] += 1
                    elif count_dict[iid]["lk_widget_display"][widget]:
                        count_dict[iid]["lk_widget_click_count"] += 1
                    elif count_dict[iid]["other_puri_widget_display"][widget]:
                        count_dict[iid]["other_puri_widget_click_count"] += 1
                    elif count_dict[iid]["no_puri_widget_display"][widget]:
                        count_dict[iid]["no_puri_widget_click_count"] += 1

                else:
                    puri = js.get("puri")
                    if puri:
                        if "samara.mts" in puri:
                            count_dict[iid]["seen_samara"] = True
            elif widget == 'mts-my-options':
                if event == 'widget.display':
                    puri = js.get("puri")
                    if puri:
                        if "samara.mts" in puri:
                            count_dict[iid]["seen_samara"] = True
                            count_dict[iid]["widget_displayed"][widget] = True
                            count_dict[iid]["display_count"] += 1
                        elif "lk." in puri:
                            count_dict[iid]["widget_displayed"][widget] = False
                            count_dict[iid]["other_puri_widget_display"][widget] = False
                            count_dict[iid]["no_puri_widget_display"][widget] = False

                            count_dict[iid]["lk_widget_display"][widget] = True
                            count_dict[iid]["lk_widget_display_count"] += 1
                        else:
                            count_dict[iid]["widget_displayed"][widget] = False
                            count_dict[iid]["lk_widget_display"][widget] = False
                            count_dict[iid]["no_puri_widget_display"][widget] = False

                            count_dict[iid]["other_puri_widget_display"][widget] = True
                            count_dict[iid]["other_puri_widget_display_count"] += 1
                    else:
                        # we do not know, where was the widget (samara/lk/anywhere)
                        count_dict[iid]["widget_displayed"][widget] = False
                        count_dict[iid]["lk_widget_display"][widget] = False
                        count_dict[iid]["other_puri_widget_display"][widget] = False

                        count_dict[iid]["no_puri_widget_display_count"] += 1
                        count_dict[iid]["no_puri_widget_display"][widget] = True

                elif event == "event.click":
                    if count_dict[iid]["widget_displayed"][widget]:
                        count_dict[iid]["click_count"] += 1
                    elif count_dict[iid]["lk_widget_display"][widget]:
                        count_dict[iid]["lk_widget_click_count"] += 1
                    elif count_dict[iid]["other_puri_widget_display"][widget]:
                        count_dict[iid]["other_puri_widget_click_count"] += 1
                    elif count_dict[iid]["no_puri_widget_display"][widget]:
                        count_dict[iid]["no_puri_widget_click_count"] += 1
                else:
                    puri = js.get("puri")
                    if puri:
                        if "samara.mts" in puri:
                            count_dict[iid]["seen_samara"] = True
            else:
                puri = js.get("puri")
                if puri:
                    if "samara.mts" in puri:
                        count_dict[iid]["seen_samara"] = True
    return count_dict


def make_check_samara(f):
    """
    Go through all user's history and add the user(iid/uiid) to set, if he had 'samara' event.
    """
    samara_set = set()
    with open(f, 'r') as input_f:
        for line in input_f:
            iid, t_s, t_e, uuid, event, widget, other_j = line.rstrip('\n\r').split('\t')
            js = json.loads(other_j)
            for v in js.values():
                if 'samara.mts' in str(v):
                    samara_set.add(iid)
    return samara_set


def count_shows_clicks_lk_simple(f, check_samara=True):
    """
    Shows:
    Use 'mts-my-options' w.displays ONLY
    divide into:
        - with 'samara.mts' in puri
        - with 'lk.ssl' in puri
        - with any other url in puri
        - with empty/without puri


    Clicks:
    Use 'mts-my-options' event.click ONLY
    with check, what puri the widget had before click event (use dictionary):
    divide into:
        - with 'samara.mts' in puri
        - with 'lk.ssl' in puri
        - with any other url in puri
        - with empty/without puri

    TO DO - add check for ussd_status
    """
    if check_samara:
        samara_set = make_check_samara(f)
        print 'Iids, seen Samara! ', len(samara_set)

    other_puri = open('other_puri.txt', 'w')
    count_dict = {}
    with open(f, 'r') as input_f:
        for line in input_f:
            iid, t_s, t_e, uuid, event, widget, other_j = line.rstrip('\n\r').split('\t')
            js = json.loads(other_j)
            count_dict.setdefault(iid,
                                  {"samara_widget_displayed": {"services": False, "mts-my-options": False}, "samara_display_count": 0,
                                   "samara_click_count": 0,
                                   'seen_samara': False,

                                   "lk_widget_display_count": 0,
                                   "lk_widget_display": {"services": False, "mts-my-options": False},
                                   "lk_widget_click_count": 0,

                                   "not_samara_lk_widget_display_count": 0,
                                   "not_samara_lk_widget_display": {"services": False, "mts-my-options": False},
                                   "not_samara_lk_widget_click_count": 0,

                                   "not_samara_other_puri_widget_display_count": 0,
                                   "not_samara_other_puri_widget_display": {"services": False, "mts-my-options": False},
                                   "not_samara_other_puri_widget_click_count": 0,

                                   "not_samara_no_puri_widget_display_count": 0,
                                   "not_samara_no_puri_widget_display": {"services": False, "mts-my-options": False},
                                   "not_samara_no_puri_widget_click_count": 0,

                                   "other_puri_widget_display_count": 0,
                                   "other_puri_widget_display": {"services": False, "mts-my-options": False},
                                   "other_puri_widget_click_count": 0,

                                   "no_puri_widget_display_count": 0,
                                   "no_puri_widget_display": {"services": False, "mts-my-options": False},
                                   "no_puri_widget_click_count": 0})
            if check_samara:
                #Check all users. If he is in samara_set - get flag to count_dict - 'seen_samara': True
                if iid in samara_set:
                    count_dict[iid]["seen_samara"] = True
                    samara_set.remove(iid)

            if widget == 'mts-my-options':
                if event == 'widget.display':
                    puri = js.get("puri")
                    if puri:
                        if "samara.mts" in puri:
                            count_dict[iid]["seen_samara"] = True
                            count_dict[iid]["lk_widget_display"][widget] = False
                            count_dict[iid]["other_puri_widget_display"][widget] = False
                            count_dict[iid]["no_puri_widget_display"][widget] = False
                            count_dict[iid]["not_samara_lk_widget_display"][widget] = False
                            count_dict[iid]["not_samara_other_puri_widget_display"][widget] = False
                            count_dict[iid]["not_samara_no_puri_widget_display"][widget] = False

                            count_dict[iid]["samara_widget_displayed"][widget] = True
                            count_dict[iid]["samara_display_count"] += 1

                        elif 'lk.' in puri:
                            if check_samara:
                                samara = count_dict[iid]["seen_samara"]
                                if samara:
                                    count_dict[iid]["samara_widget_displayed"][widget] = False
                                    count_dict[iid]["other_puri_widget_display"][widget] = False
                                    count_dict[iid]["no_puri_widget_display"][widget] = False
                                    count_dict[iid]["not_samara_lk_widget_display"][widget] = False
                                    count_dict[iid]["not_samara_other_puri_widget_display"][widget] = False
                                    count_dict[iid]["not_samara_no_puri_widget_display"][widget] = False

                                    count_dict[iid]["lk_widget_display"][widget] = True
                                    count_dict[iid]["lk_widget_display_count"] += 1
                                else:
                                    count_dict[iid]["lk_widget_display"][widget] = False
                                    count_dict[iid]["samara_widget_displayed"][widget] = False
                                    count_dict[iid]["other_puri_widget_display"][widget] = False
                                    count_dict[iid]["no_puri_widget_display"][widget] = False
                                    count_dict[iid]["not_samara_other_puri_widget_display"][widget] = False
                                    count_dict[iid]["not_samara_no_puri_widget_display"][widget] = False

                                    count_dict[iid]["not_samara_lk_widget_display"][widget] = True
                                    count_dict[iid]["not_samara_lk_widget_display_count"] += 1
                            else:
                                count_dict[iid]["samara_widget_displayed"][widget] = False
                                count_dict[iid]["other_puri_widget_display"][widget] = False
                                count_dict[iid]["no_puri_widget_display"][widget] = False
                                count_dict[iid]["not_samara_lk_widget_display"][widget] = False
                                count_dict[iid]["not_samara_other_puri_widget_display"][widget] = False
                                count_dict[iid]["not_samara_no_puri_widget_display"][widget] = False

                                count_dict[iid]["lk_widget_display"][widget] = True
                                count_dict[iid]["lk_widget_display_count"] += 1
                        else:
                            other_puri.write("%s\n" % puri)
                            if check_samara:
                                samara = count_dict[iid]["seen_samara"]
                                if samara:
                                    count_dict[iid]["lk_widget_display"][widget] = False
                                    count_dict[iid]["samara_widget_displayed"][widget] = False
                                    count_dict[iid]["no_puri_widget_display"][widget] = False
                                    count_dict[iid]["not_samara_lk_widget_display"][widget] = False
                                    count_dict[iid]["not_samara_no_puri_widget_display"][widget] = False
                                    count_dict[iid]["not_samara_other_puri_widget_display"][widget] = False

                                    count_dict[iid]["other_puri_widget_display"][widget] = True
                                    count_dict[iid]["other_puri_widget_display_count"] += 1
                                else:
                                    count_dict[iid]["lk_widget_display"][widget] = False
                                    count_dict[iid]["other_puri_widget_display"][widget] = False
                                    count_dict[iid]["samara_widget_displayed"][widget] = False
                                    count_dict[iid]["no_puri_widget_display"][widget] = False
                                    count_dict[iid]["not_samara_lk_widget_display"][widget] = False
                                    count_dict[iid]["not_samara_no_puri_widget_display"][widget] = False

                                    count_dict[iid]["not_samara_other_puri_widget_display"][widget] = True
                                    count_dict[iid]["not_samara_other_puri_widget_display_count"] += 1
                            else:
                                count_dict[iid]["lk_widget_display"][widget] = False
                                count_dict[iid]["samara_widget_displayed"][widget] = False
                                count_dict[iid]["no_puri_widget_display"][widget] = False
                                count_dict[iid]["not_samara_lk_widget_display"][widget] = False
                                count_dict[iid]["not_samara_no_puri_widget_display"][widget] = False
                                count_dict[iid]["not_samara_other_puri_widget_display"][widget] = False

                                count_dict[iid]["other_puri_widget_display"][widget] = True
                                count_dict[iid]["other_puri_widget_display_count"] += 1

                    else:
                        if check_samara:
                            samara = count_dict[iid]["seen_samara"]
                            if samara:
                                count_dict[iid]["lk_widget_display"][widget] = False
                                count_dict[iid]["other_puri_widget_display"][widget] = False
                                count_dict[iid]["samara_widget_displayed"][widget] = False
                                count_dict[iid]["not_samara_lk_widget_display"][widget] = False
                                count_dict[iid]["not_samara_no_puri_widget_display"][widget] = False
                                count_dict[iid]["not_samara_other_puri_widget_display"][widget] = False

                                count_dict[iid]["no_puri_widget_display"][widget] = True
                                count_dict[iid]["no_puri_widget_display_count"] += 1

                            else:
                                count_dict[iid]["lk_widget_display"][widget] = False
                                count_dict[iid]["samara_widget_displayed"][widget] = False
                                count_dict[iid]["other_puri_widget_display"][widget] = False
                                count_dict[iid]["no_puri_widget_display"][widget] = False
                                count_dict[iid]["not_samara_lk_widget_display"][widget] = False
                                count_dict[iid]["not_samara_other_puri_widget_display"][widget] = False

                                count_dict[iid]["not_samara_no_puri_widget_display"][widget] = True
                                count_dict[iid]["not_samara_no_puri_widget_display_count"] += 1
                        else:
                            count_dict[iid]["other_puri_widget_display"][widget] = False
                            count_dict[iid]["lk_widget_display"][widget] = False
                            count_dict[iid]["samara_widget_displayed"][widget] = False
                            count_dict[iid]["not_samara_lk_widget_display"][widget] = False
                            count_dict[iid]["not_samara_no_puri_widget_display"][widget] = False
                            count_dict[iid]["not_samara_other_puri_widget_display"][widget] = False

                            count_dict[iid]["no_puri_widget_display"][widget] = True
                            count_dict[iid]["no_puri_widget_display_count"] += 1
                elif event == "event.click":
                    if count_dict[iid]["lk_widget_display"][widget]:
                        count_dict[iid]["lk_widget_click_count"] += 1
                    elif count_dict[iid]["samara_widget_displayed"][widget]:
                        count_dict[iid]["samara_click_count"] += 1
                    elif count_dict[iid]["not_samara_lk_widget_display"][widget]:
                        count_dict[iid]["not_samara_lk_widget_click_count"] += 1
                    elif count_dict[iid]["other_puri_widget_display"][widget]:
                        count_dict[iid]["other_puri_widget_click_count"] += 1
                    elif count_dict[iid]["no_puri_widget_display"][widget]:
                        count_dict[iid]["no_puri_widget_click_count"] += 1
                    elif count_dict[iid]["not_samara_no_puri_widget_display"][widget]:
                        count_dict[iid]["not_samara_no_puri_widget_click_count"] += 1
                    elif count_dict[iid]["not_samara_other_puri_widget_display"][widget]:
                        count_dict[iid]["not_samara_other_puri_widget_click_count"] += 1
    other_puri.close()
    return count_dict


def count_clicks(count_dict, t='lk'):
    if t == 'lk':
        print 'Count lk!'
        samara_widgets = 0
        samara_clicks = 0

        lk_widgets = 0
        lk_clicks = 0
        not_samara_lk_widgets = 0
        not_samara_lk_clicks = 0

        other_puri_widgets = 0
        other_puri_clicks = 0
        not_samara_other_puri_widgets = 0
        not_samara_other_puri_clicks = 0

        no_puri_widgets = 0
        no_puri_clicks = 0
        not_samara_no_puri_widgets = 0
        not_samara_no_puri_clicks = 0

        samara_count_iid = set()
        not_samara_lk_count_iid = set()
        lk_count_iid = set()
        other_count_iid = set()
        not_samara_other_count_iid = set()
        no_puri_count_iid = set()
        not_samara_no_puri_count_iid = set()

        all_clicks= 0
        all_shows = 0
        n = 0
        for iid in count_dict:
            if count_dict[iid]["samara_display_count"] > 0 or count_dict[iid]["samara_click_count"] > 0:
                samara_count_iid.add(iid)
            if count_dict[iid]["lk_widget_display_count"] > 0 or count_dict[iid]["lk_widget_click_count"] > 0:
                if n < 1:
                    print 'lk_count_iid +1!'
                    n+=1
                lk_count_iid.add(iid)
            if count_dict[iid]["not_samara_lk_widget_display_count"] > 0 or count_dict[iid]["not_samara_lk_widget_click_count"] > 0:
                not_samara_lk_count_iid.add(iid)
            if count_dict[iid]["other_puri_widget_display_count"] > 0 or count_dict[iid]["other_puri_widget_click_count"] > 0:
                other_count_iid.add(iid)
            if count_dict[iid]["no_puri_widget_display_count"] > 0 or count_dict[iid]["no_puri_widget_click_count"] > 0:
                no_puri_count_iid.add(iid)
            if count_dict[iid]["not_samara_no_puri_widget_display_count"] > 0 or count_dict[iid]["not_samara_no_puri_widget_click_count"] > 0:
                not_samara_no_puri_count_iid.add(iid)
            if count_dict[iid]["not_samara_other_puri_widget_display_count"] > 0 or count_dict[iid]["not_samara_other_puri_widget_click_count"] > 0:
                not_samara_other_count_iid.add(iid)


            samara_widgets += count_dict[iid]["samara_display_count"]
            samara_clicks += count_dict[iid]["samara_click_count"]

            lk_widgets += count_dict[iid]["lk_widget_display_count"]
            lk_clicks += count_dict[iid]["lk_widget_click_count"]
            not_samara_lk_widgets += count_dict[iid]["not_samara_lk_widget_display_count"]
            not_samara_lk_clicks += count_dict[iid]["not_samara_lk_widget_click_count"]

            other_puri_widgets += count_dict[iid]["other_puri_widget_display_count"]
            other_puri_clicks += count_dict[iid]["other_puri_widget_click_count"]
            not_samara_other_puri_widgets += count_dict[iid]["not_samara_other_puri_widget_display_count"]
            not_samara_other_puri_clicks += count_dict[iid]["not_samara_other_puri_widget_click_count"]


            no_puri_widgets += count_dict[iid]["no_puri_widget_display_count"]
            no_puri_clicks +=  count_dict[iid]["no_puri_widget_click_count"]
            not_samara_no_puri_widgets += count_dict[iid]["not_samara_no_puri_widget_display_count"]
            not_samara_no_puri_clicks +=  count_dict[iid]["not_samara_no_puri_widget_click_count"]


            all_clicks = samara_clicks + lk_clicks + other_puri_clicks + no_puri_clicks + not_samara_lk_clicks + not_samara_other_puri_clicks + not_samara_no_puri_clicks
            all_shows = samara_widgets + not_samara_lk_widgets + lk_widgets + other_puri_widgets + no_puri_widgets + not_samara_other_puri_widgets + not_samara_no_puri_widgets

        return samara_widgets, samara_clicks, lk_widgets, lk_clicks, \
               not_samara_lk_widgets, not_samara_lk_clicks,\
               not_samara_other_puri_widgets, not_samara_other_puri_clicks, \
               other_puri_widgets, other_puri_clicks, no_puri_widgets, no_puri_clicks, \
               not_samara_no_puri_widgets,not_samara_no_puri_clicks,  \
               all_clicks, all_shows, \
               len(samara_count_iid), len(lk_count_iid), len(not_samara_lk_count_iid), len(other_count_iid), len(no_puri_count_iid), \
               len(not_samara_other_count_iid), len(not_samara_no_puri_count_iid), \
               len(lk_count_iid.intersection(samara_count_iid)),len(lk_count_iid.intersection(not_samara_lk_count_iid)), \
               len(lk_count_iid.intersection(other_count_iid)), len(lk_count_iid.intersection(no_puri_count_iid)),\
               len(lk_count_iid.intersection(not_samara_other_count_iid)), len(lk_count_iid.intersection(not_samara_no_puri_count_iid)),\
               len(samara_count_iid.intersection(not_samara_lk_count_iid)), len(samara_count_iid.intersection(other_count_iid)), len(samara_count_iid.intersection(no_puri_count_iid)), \
               len(not_samara_lk_count_iid.intersection(other_count_iid)), len(not_samara_lk_count_iid.intersection(no_puri_count_iid)), \
               len(other_count_iid.intersection(no_puri_count_iid)),\
               len(lk_count_iid.difference(samara_count_iid, not_samara_lk_count_iid, other_count_iid, no_puri_count_iid, not_samara_other_count_iid, not_samara_no_puri_count_iid )), \
               len(samara_count_iid.difference(lk_count_iid, not_samara_lk_count_iid, other_count_iid, no_puri_count_iid, not_samara_other_count_iid, not_samara_no_puri_count_iid)), \
               len(not_samara_lk_count_iid.difference(samara_count_iid, lk_count_iid, other_count_iid, no_puri_count_iid, not_samara_other_count_iid, not_samara_no_puri_count_iid)), \
               len(other_count_iid.difference(samara_count_iid, lk_count_iid, not_samara_lk_count_iid, no_puri_count_iid, not_samara_other_count_iid, not_samara_no_puri_count_iid)), \
               len(no_puri_count_iid.difference(samara_count_iid, lk_count_iid, not_samara_lk_count_iid, other_count_iid, not_samara_other_count_iid, not_samara_no_puri_count_iid)),\
               len(not_samara_other_count_iid.difference(samara_count_iid, lk_count_iid, not_samara_lk_count_iid, other_count_iid, no_puri_count_iid, not_samara_no_puri_count_iid)),\
               len(not_samara_no_puri_count_iid.difference(samara_count_iid, lk_count_iid, not_samara_lk_count_iid, other_count_iid, no_puri_count_iid, not_samara_other_count_iid))

    else:
        samara_widgets = 0
        samara_clicks = 0
        lk_widgets = 0
        lk_clicks = 0
        other_puri_widgets = 0
        other_puri_clicks = 0
        no_puri_widgets = 0
        no_puri_clicks = 0

        samara_count_iid = set()
        lk_count_iid = set()
        other_count_iid = set()
        no_puri_count_iid = set()

        all_clicks= 0
        all_shows = 0

        for iid in count_dict:
            if count_dict[iid]["display_count"] > 0 or count_dict[iid]["click_count"] > 0:
                samara_count_iid.add(iid)
            if count_dict[iid]["lk_widget_display_count"] > 0 or count_dict[iid]["lk_widget_click_count"] > 0:
                lk_count_iid.add(iid)
            if count_dict[iid]["other_puri_widget_display_count"] > 0 or count_dict[iid][
                "other_puri_widget_click_count"] > 0:
                other_count_iid.add(iid)
            if count_dict[iid]["no_puri_widget_display_count"] > 0 or count_dict[iid]["no_puri_widget_click_count"] > 0:
                no_puri_count_iid.add(iid)

            samara_widgets += count_dict[iid]["display_count"]
            samara_clicks += count_dict[iid]["click_count"]
            lk_widgets += count_dict[iid]["lk_widget_display_count"]
            lk_clicks += count_dict[iid]["lk_widget_click_count"]
            other_puri_widgets += count_dict[iid]["other_puri_widget_display_count"]
            other_puri_clicks += count_dict[iid]["other_puri_widget_click_count"]
            no_puri_widgets += count_dict[iid]["no_puri_widget_display_count"]
            no_puri_clicks += count_dict[iid]["no_puri_widget_click_count"]

            all_clicks = samara_clicks + lk_clicks + other_puri_clicks + no_puri_clicks
            all_shows = samara_widgets + lk_widgets + other_puri_widgets + no_puri_widgets

        return samara_widgets, samara_clicks, lk_widgets, lk_clicks, \
               other_puri_widgets, other_puri_clicks, no_puri_widgets, no_puri_clicks, \
               all_clicks, all_shows, \
               len(samara_count_iid), len(lk_count_iid), len(other_count_iid), len(no_puri_count_iid), \
               len(samara_count_iid.intersection(lk_count_iid)), len(samara_count_iid.intersection(other_count_iid)), \
               len(samara_count_iid.intersection(no_puri_count_iid)),\
               len(lk_count_iid.intersection(other_count_iid)), \
               len(lk_count_iid.intersection(no_puri_count_iid)), \
               len(other_count_iid.intersection(no_puri_count_iid)), \
               len(samara_count_iid.difference(lk_count_iid, other_count_iid, no_puri_count_iid)), \
               len(lk_count_iid.difference(samara_count_iid, other_count_iid, no_puri_count_iid)), \
               len(other_count_iid.difference(samara_count_iid, lk_count_iid, no_puri_count_iid)), \
               len(no_puri_count_iid.difference(samara_count_iid, lk_count_iid, other_count_iid))


def main():
    verbose = True
    """
    file_iid_samara, file_iid - outfiles from iid_uiid_sets_dicts.
    """
    file_iid_samara = 'iid_samara_1day_samara_dict.txt'
    file_iid = 'iid_1day_samara_dict.txt'
    # file_iid_samara = 'test_iid_1d.txt'
    # file_iid = 'test_iid_1d.txt'
    if verbose:
        print 'count_main_shows_clicks_simple'
    main_count_dict = count_main_shows_clicks_simple(file_iid_samara)
    if verbose:
        print 'len(main_count_dict.keys()), ', len(main_count_dict.keys())
    good_widgets, good_clicks, lk_widgets, lk_clicks, \
    other_puri_widgets, other_puri_clicks, \
    no_puri_widgets, no_puri_clicks,\
    all_clicks, all_shows, \
    good_count_iid, lk_count_iid, other_count_iid, no_puri_count_iid,\
    good_count_and_lk_count_iid, good_count_and_other_count_iid,good_count_and_no_puri_count_iid, \
    lk_count_iid_and_other_count_iid, lk_count_iid_and_no_puri_count_iid, \
    other_count_iid_and_no_puri_count_iid, \
    uniq_good_count_iid, uniq_lk_count_iid, \
    uniq_other_count_iid, uniq_no_puri_count_iid = count_clicks(main_count_dict, t='main')

    print "good_widgets - %s, \ngood_clicks - %s,\nlk_widgets - %s,\nlk_clicks - %s,\n\
    other_puri_widgets - %s,\nother_puri_clicks - %s,\n\
    no_puri_widgets - %s,\nno_puri_clicks - %s,\n\
    all_clicks - %s,\nall_shows - %s,\n\
    good_count_iid - %s,\nlk_count_iid - %s,\nother_count_iid - %s,\nno_puri_count_iid - %s,\n\
    good_count_and_lk_count_iid - %s,\ngood_count_and_other_count_iid - %s,\ngood_count_iid_and_other_count_iid - %s,\n\
    lk_count_iid_and_other_count_iid - %s,\nlk_count_iid_and_no_puri_count_iid - %s,\n\
    other_count_iid_and_no_puri_count_iid - %s,\n\
    uniq_good_count_iid - %s,\nuniq_lk_count_iid - %s,\n\
    uniq_other_count_iid - %s,\nuniq_no_puri_count_iid - %s" % (good_widgets, good_clicks, lk_widgets, lk_clicks,
                                                              other_puri_widgets, other_puri_clicks,
                                                              no_puri_widgets, no_puri_clicks,
                                                              all_clicks, all_shows,
                                                              good_count_iid, lk_count_iid, other_count_iid,
                                                              no_puri_count_iid,
                                                              good_count_and_lk_count_iid,
                                                              good_count_and_other_count_iid,
                                                              good_count_and_no_puri_count_iid,
                                                              lk_count_iid_and_other_count_iid,
                                                              lk_count_iid_and_no_puri_count_iid,
                                                              other_count_iid_and_no_puri_count_iid,
                                                              uniq_good_count_iid, uniq_lk_count_iid,
                                                              uniq_other_count_iid, uniq_no_puri_count_iid)

    if good_widgets > 0:
        print 'ctr good_widgets - %s\n' % ((float(good_clicks) / good_widgets) * 100)
    if all_shows > 0:
        print 'ctr all_shows - %s\n' % ((float(all_clicks) / all_shows) * 100)
    if lk_widgets > 0:
        print 'ctr lk - %s\n' % ((float(lk_clicks) / lk_widgets) * 100)

    if other_puri_widgets > 0:
        print 'ctr other_puri_widgets - %s\n' % ((float(other_puri_clicks) / other_puri_widgets) * 100)
    if no_puri_widgets > 0:
        print 'ctr no_puri_widgets - %s\n' % ((float(no_puri_clicks) / no_puri_widgets) * 100)
    if good_widgets > 0:
        print 'ctr ~good - %s\n' % ((float(good_clicks + no_puri_clicks + other_puri_clicks) / (good_widgets + no_puri_widgets + other_puri_widgets)) * 100)


    print 'count_shows_clicks_lk_simple, Check samara!'
    lk_count_dict = count_shows_clicks_lk_simple(file_iid, check_samara=False)
    print 'len(lk_count_dict.keys()), ', len(lk_count_dict.keys())
    samara_widgets, samara_clicks, lk_widgets, lk_clicks,\
    not_samara_lk_widgets, not_samara_lk_clicks,\
    not_samara_other_puri_widgets, not_samara_other_puri_clicks,\
    other_puri_widgets, other_puri_clicks, no_puri_widgets, no_puri_clicks,\
    not_samara_no_puri_widgets, not_samara_no_puri_clicks,\
    all_clicks, all_shows,\
    samara_count_iid, lk_count_iid, not_samara_lk_count_iid, other_count_iid, no_puri_count_iid,\
    not_samara_other_count_iid, not_samara_no_puri_count_iid,\
    lk_count_and_samara_count_iid, lk_count_and_not_samara_lk_count_iid,\
    lk_count_and_other_count_iid, lk_count_and_no_puri_count_iid,\
    lk_count_and_not_samara_other_count_iid, lk_count_and_not_samara_no_puri_count_iid,\
    samara_count_and_not_samara_lk_count_iid, samara_count_and_other_count_iid,\
    samara_count_and_no_puri_count_iid,\
    not_samara_lk_count_and_other_count_iid, not_samara_lk_count_and_no_puri_count_iid,\
    other_count_and_no_puri_count_iid, lk_count_iid, uniq_samara_count_iid, uniq_not_samara_lk_count_iid,\
    uniq_other_count_iid, uniq_no_puri_count_iid, uniq_not_samara_other_count_iid, uniq_not_samara_no_puri_count_iid = count_clicks(lk_count_dict, t='lk')

    print "samara_widgets - %s, \nsamara_clicks - %s,\n lk_widgets - %s,\n lk_clicks - %s, \n " \
          "not_samara_lk_widgets - %s,\n not_samara_lk_clicks - %s, \n" \
          "not_samara_other_puri_widgets, - %s,\n not_samara_other_puri_clicks - %s, \n" \
          "other_puri_widgets - %s, \nother_puri_clicks - %s,\n no_puri_widgets - %s,\n no_puri_clicks - %s,  " \
          "not_samara_no_puri_widgets - %s, \nnot_samara_no_puri_clicks - %s,\n " \
          "all_clicks - %s, \nall_shows - %s,  " \
          "samara_count_iid - %s, \nlk_count_iid - %s, \nnot_samara_lk_count_iid - %s, \nother_count_iid - %s, \nno_puri_count_iid - %s, \n " \
          "not_samara_other_count_iid - %s, \nnot_samara_no_puri_count_iid - %s, \n" \
          "lk_count_and_samara_count_iid - %s,\nlk_count_and_not_samara_lk_count_iid - %s,\n  " \
          "lk_count_and_other_count_iid - %s,\n lk_count_and_no_puri_count_iid - %s,\n " \
          "lk_count_and_not_samara_other_count_iid - %s,\n lk_count_and_not_samara_no_puri_count_iid - %s,\n " \
          "samara_count_and_not_samara_lk_count_iid - %s,\n samara_count_and_other_count_iid - %s, \nsamara_count_and_no_puri_count_iid - %s,\n  " \
          "not_samara_lk_count_and_other_count_iid - %s,\n not_samara_lk_count_and_no_puri_count_iid - %s,  \n" \
          "other_count_and_no_puri_count_iid - %s, \nlk_count_iid - %s, \nuniq_samara_count_iid - %s,\n uniq_not_samara_lk_count_iid - %s,\n " \
          "uniq_other_count_iid - %s, \nuniq_no_puri_count_iid - %s,\n uniq__not_samara_other_count_iid - %s, \nuniq_not_samara_no_puri_count_iid - %s\n" % (
          samara_widgets, samara_clicks, lk_widgets, lk_clicks,
          not_samara_lk_widgets, not_samara_lk_clicks,
          not_samara_other_puri_widgets, not_samara_other_puri_clicks,
          other_puri_widgets, other_puri_clicks, no_puri_widgets, no_puri_clicks,
          not_samara_no_puri_widgets, not_samara_no_puri_clicks,
          all_clicks, all_shows,
          samara_count_iid, lk_count_iid, not_samara_lk_count_iid, other_count_iid, no_puri_count_iid,
          not_samara_other_count_iid, not_samara_no_puri_count_iid,
          lk_count_and_samara_count_iid, lk_count_and_not_samara_lk_count_iid,
          lk_count_and_other_count_iid, lk_count_and_no_puri_count_iid,
          lk_count_and_not_samara_other_count_iid, lk_count_and_not_samara_no_puri_count_iid,
          samara_count_and_not_samara_lk_count_iid, samara_count_and_other_count_iid,
          samara_count_and_no_puri_count_iid,
          not_samara_lk_count_and_other_count_iid, not_samara_lk_count_and_no_puri_count_iid,
          other_count_and_no_puri_count_iid, lk_count_iid, uniq_samara_count_iid, uniq_not_samara_lk_count_iid,
          uniq_other_count_iid, uniq_no_puri_count_iid, uniq_not_samara_other_count_iid, uniq_not_samara_no_puri_count_iid)

    if lk_widgets > 0:
        print 'ctr lk_widgets - %s\n' % ((float(lk_clicks) / lk_widgets) * 100)
    if samara_widgets > 0:
        print 'ctr samara_widgets - %s\n' % ((float(samara_clicks) / samara_widgets) * 100)
    if not_samara_lk_widgets > 0:
        print 'ctr not_samara_lk_widgets - %s\n' % ((float(not_samara_lk_clicks) / not_samara_lk_widgets) * 100)
    if other_puri_widgets > 0:
        print 'ctr other_puri_widgets - %s\n' % ((float(other_puri_clicks) / other_puri_widgets) * 100)
    if no_puri_widgets > 0:
        print 'ctr no_puri_widgets - %s\n' % ((float(no_puri_clicks) / no_puri_widgets) * 100)
    if not_samara_other_puri_widgets > 0:
        print 'ctr not_samara_other_puri_widgets - %s\n' % ((float(not_samara_other_puri_clicks) / not_samara_other_puri_widgets) * 100)
    if not_samara_no_puri_widgets > 0:
        print 'ctr not_samara_no_puri_widgets - %s\n' % ((float(not_samara_no_puri_clicks) / not_samara_no_puri_widgets) * 100)

    if all_shows > 0:
        print 'ctr all_shows - %s\n' % ((float(all_clicks) / all_shows) * 100)



if __name__ == "__main__":
    main()