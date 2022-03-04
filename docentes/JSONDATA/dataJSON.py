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


class Warnings:
    def __init__(self, item, itemid, warningcode, message):
        self.item = item
        self.itemid = itemid
        self.warningcode = warningcode
        self.message = message

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<message : {self.message}>'


class Statuses:
    def __init__(self, cmid, modname, instance, state, timecompleted, tracking, overrideby, valueused):
        self.cmid = cmid
        self.modname = modname
        self.instance = instance
        self.state = state
        self.timecompleted = timecompleted
        self.tracking = tracking
        self.overrideby = overrideby
        self.valueused = valueused

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<statuses : {self.modname}>'


class CursosActividades:
    def __init__(self, cursos, actividades, avisos):
        self.cursos = cursos
        self.actividades = actividades
        self.avisos = avisos
