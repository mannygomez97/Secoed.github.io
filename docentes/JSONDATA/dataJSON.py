import json


class core_enrol_get_users_courses:
    def __init__(self, id, shortname, fullname, displayname, enrolledusercount, idnumber, visible, summary,
                 summaryformat, format, showgrades, lang, enablecompletion, completionhascriteria,
                 completionusertracked, category, progress, completed,
                 startdate, enddate,
                 marker, lastaccess, isfavourite, hidden, overviewfiles):
        self.id = id
        self.fullname = fullname
        self.shortname = shortname
        self.displayname = displayname
        self.enrolledusercount = enrolledusercount
        self.idnumber = idnumber
        self.visible = visible
        self.summary = summary
        self.summaryformat = summaryformat
        self.format = format
        self.showgrades = showgrades
        self.lang = lang
        self.enablecompletion = enablecompletion
        self.completionhascriteria = completionhascriteria
        self.completionusertracked = completionusertracked
        self.category = category
        self.progress = progress
        self.completed = completed
        self.startdate = startdate
        self.enddate = enddate
        self.marker = marker
        self.lastaccess = lastaccess
        self.isfavourite = isfavourite
        self.hidden = hidden
        self.overviewfiles = overviewfiles

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<Curso: {self.fullname}>'


class gradereport_user_get_grade_items:
    def __init__(self, courseid, userid, userfullname, useridnumber, maxdepth, gradeitems):
        self.courseid = courseid
        self.userid = userid
        self.userfullname = userfullname
        self.useridnumber = useridnumber
        self.maxdepth = maxdepth
        self.gradeitems = gradeitems

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<usergrades: {self.courseid}>'


class gradeitems:
    def __init__(self, id, itemname, itemtype, itemmodule, iteminstance, itemnumber, idnumber, categoryid, outcomeid,
                 scaleid, locked, graderaw, gradedatesubmitted, gradedategraded, gradehiddenbydate, gradeneedsupdate,
                 gradeishidden, gradeislocked, gradeisoverridden, gradeformatted, grademin,
                 grademax, rangeformatted, percentageformatted, feedback, feedbackformat, cmid = None, weightraw = None,
                 status = None, weightformatted = None):
        self.id = id
        self.itemname = itemname
        self.itemtype = itemtype
        self.itemmodule = itemmodule
        self.iteminstance = iteminstance
        self.itemnumber = itemnumber
        self.idnumber = idnumber
        self.categoryid = categoryid
        self.outcomeid = outcomeid
        self.scaleid = scaleid
        self.locked = locked
        self.graderaw = graderaw
        self.gradedatesubmitted = gradedatesubmitted
        self.gradedategraded = gradedategraded
        self.gradehiddenbydate = gradehiddenbydate
        self.gradeneedsupdate = gradeneedsupdate
        self.gradeishidden = gradeishidden
        self.gradeislocked = gradeislocked
        self.gradeisoverridden = gradeisoverridden
        self.gradeformatted = gradeformatted
        self.grademin = grademin
        self.grademax = grademax
        self.rangeformatted = rangeformatted
        self.percentageformatted = percentageformatted
        self.feedback = feedback
        self.feedbackformat = feedbackformat
        self.weightraw = weightraw
        self.weightformatted = weightformatted
        self.status = status
        if graderaw is not None:
            self.nota = (graderaw * 100)/grademax
        else:
            self.nota = 0.00

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<gradeitems: {self.itemname}>'

class course_activities:
    def __init__(self, curso, actividades):
        self.curso = curso
        self.actividades = actividades

    def __repr__(self):
        return f'<curso: {self.curso}>'