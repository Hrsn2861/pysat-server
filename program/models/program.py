"""models for program
"""
from django.db import models

from utils import getdate_now, getdate_none, date_to_string
from school.models import SubjectHelper
from school.models import SchoolHelper
from program.models.downloadlog import DownloadLogHelper
from program.models.like import LikeHelper

class Program(models.Model):
    """Program Model
    """
    name = models.CharField(max_length=128)
    author = models.IntegerField()
    code = models.TextField()
    doc = models.TextField()
    submit_time = models.DateTimeField()
    status = models.IntegerField()
    judge = models.IntegerField()
    judge_time = models.DateTimeField()
    upload_time = models.DateTimeField()
    downloads = models.IntegerField()
    likes = models.IntegerField()
    schoolid = models.IntegerField(default=0)
    subjectid = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'program'
        verbose_name_plural = 'programs'
        get_latest_by = 'id'

class ProgramHelper:
    #pylint: disable-msg=too-many-public-methods
    """Program Helper
    """
    @staticmethod
    def program_to_dict(program):
        """transform a program object into dict
        """
        judge_time = program.judge_time
        if judge_time == getdate_none():
            judge_time = None
        upload_time = program.upload_time
        if upload_time == getdate_none():
            upload_time = None
        ProgramHelper.refresh(program.id)
        return {
            'id' : program.id,
            'name' : program.name,
            'author' : program.author,
            'code' : program.code,
            'doc' : program.doc,
            'submit_time' : date_to_string(program.submit_time),
            'status' : program.status,
            'judge' : program.judge,
            'judge_time' : date_to_string(judge_time),
            'upload_time' : date_to_string(upload_time),
            'downloads' : program.downloads,
            'likes' : program.likes,
            'schoolid' : program.schoolid,
            "subjectid" : program.subjectid
        }

    @staticmethod
    def prog_filter(program, username, downloaded, liked, schoolname):
        """match the list data
        """
        school = SchoolHelper.get_school(program.get('schoolid'))
        if school is None:
            schoolname = None
        else:
            schoolname = school.get('schoolname')
        if program.get('schoolid') == 0:
            schoolname = '在野'

        subject = SubjectHelper.get_subject(program.get('subjectid'))
        if subject is None:
            subjectname = None
        else:
            subjectname = subject.get('title')
        info = {
            'id' : program.get('id'),
            'name' : program.get('name'),
            'author' : username,
            'author_school_name' : schoolname,
            'theme_name' : subjectname,
            'status' : program.get('status'),
            'downloads' : program.get('downloads'),
            'likes' : program.get('likes'),
            'upload_time' : program.get('upload_time'),
            'submit_time' : program.get('submit_time'),
            'judge_time' : program.get('judge_time'),
            'downloaded' : downloaded,
            'liked' : liked
        }
        return info

    @staticmethod
    def judge_program(prog_id, status, admin_id):
        """judge program
        """
        progs = Program.objects.filter(id=prog_id)
        if progs.exists():
            program = progs.last()
        else:
            return False

        program.judge = admin_id
        program.status = status
        program.judge_time = getdate_now()

        program.save()
        return True

    @staticmethod
    def add_program(author, name, code, doc, schoolid, subjectid):
        # pylint: disable-msg=too-many-arguments
        """add program
        """
        program = Program(
            author=author,
            name=name,
            code=code,
            doc=doc,
            submit_time=getdate_now(),
            judge=0,
            status=0,
            judge_time=getdate_none(),
            upload_time=getdate_none(),
            downloads=0,
            likes=0,
            schoolid=schoolid,
            subjectid=subjectid
        )
        program.save()
        return program.id

    @staticmethod
    def get_program(prog_id):
        """get program by id
        """
        programs = Program.objects.filter(id=prog_id)
        if programs.exists():
            program = programs.last()
            return ProgramHelper.program_to_dict(program)
        return None

    @staticmethod
    def get_program_by_name(title):
        """get a program by title
        """
        programs = Program.objects.filter(name=title)
        if programs.exists():
            program = programs.last()
            return ProgramHelper.program_to_dict(program)
        return None

    @staticmethod
    def get_programs_count(params):
        """get programs count with params
        """
        qs = Program.objects.filter(**params)
        return qs.count()

    @staticmethod
    def get_programs(params, page, listtype):
        """get programs with params
        """
        qs = Program.objects.filter(**params)
        if listtype == 0:
            qs = qs.order_by('-upload_time')
        elif listtype == 1:
            qs = qs.order_by('-downloads')
        elif listtype == 2:
            qs = qs.order_by('-likes')
        elif listtype == 3:
            qs = qs.order_by('-id')
        else:
            return []
        programs = qs[(page - 1) * 20 : page * 20]
        ret = []
        for program in programs:
            ret.append(ProgramHelper.program_to_dict(program))
        return ret

    @staticmethod
    def get_user_programs_count(user_id):
        """get user's programs count
        """
        return ProgramHelper.get_programs_count({'author' : user_id})

    @staticmethod
    def get_school_programs_count(schoolid):
        """get school's programs count
        """
        return ProgramHelper.get_programs_count({'schoolid' : schoolid})

    @staticmethod
    def get_subject_programs_count(subjectid):
        """get subject's programs count
        """
        return ProgramHelper.get_programs_count({'subjectid' : subjectid})

    @staticmethod
    def get_user_programs(user_id, page, listtype):
        """get user's programs
        """
        return ProgramHelper.get_programs({'author' : user_id}, page, listtype)

    @staticmethod
    def get_school_programs(schoolid, page, listtype):
        """get school's programs
        """
        return ProgramHelper.get_programs({'schoolid' : schoolid}, page, listtype)

    @staticmethod
    def get_subject_programs(subjectid, page, listtype):
        """get subject's programs
        """
        return ProgramHelper.get_programs({'subjectid' : subjectid}, page, listtype)

    @staticmethod
    def get_onstar_programs(page, listtype):
        """get status == 5 programs
        """
        return ProgramHelper.get_programs({'status' : 5}, page, listtype)

    @staticmethod
    def get_inqueue_programs(page, listtype):
        """get status == 4 programs
        """
        return ProgramHelper.get_programs({'status' : 4}, page, listtype)

    @staticmethod
    def get_judge_programs(page, listtype):
        """get status == 0 programs
        """
        return ProgramHelper.get_programs({
            'status__gt' : -1,
            'status__lt' : 3
            }, page, listtype)

    @staticmethod
    def get_programs_between_status(status_up, status_low, page, listtype):
        """get programs by status list
        """
        return ProgramHelper.get_programs({
            'status__gt' : status_low,
            'status__lt' : status_up
        }, page, listtype)

    @staticmethod
    def get_programs_school(stauts_up, status_low, schoolid, subjectid, page, listtype):
        # pylint: disable-msg=too-many-arguments
        """get programs by status list with school and subject
        """
        fillter_dict = {
            'status__gt' : status_low,
            'status__lt' : stauts_up,
            'schoolid' : schoolid,
            'subjectid' : subjectid
        }
        if schoolid is None:
            del fillter_dict['schoolid']
        if subjectid is None:
            del fillter_dict['subjectid']
        return ProgramHelper.get_programs(fillter_dict, page, listtype)

    @staticmethod
    def get_programs_school_count(stauts_up, status_low, schoolid, subjectid):
        # pylint: disable-msg=too-many-arguments
        """get programs by status list with school and subject
        """
        fillter_dict = {
            'status__gt' : status_low,
            'status__lt' : stauts_up,
            'schoolid' : schoolid,
            'subjectid' : subjectid
        }
        if schoolid is None:
            del fillter_dict['schoolid']
        if subjectid is None:
            del fillter_dict['subjectid']
        return ProgramHelper.get_programs_count(fillter_dict)

    @staticmethod
    def get_programs_between_status_count(stauts_up, status_low):
        """get programs by status list
        """
        return ProgramHelper.get_programs_count({
            'status__gt' : status_low,
            'status__lt' : stauts_up
        })

    @staticmethod
    def judging(prog_id):
        """when the prgram is judging
        """
        progs = Program.objects.filter(id=prog_id)
        if progs.exists():
            program = progs.last()
        else:
            return False

        program.status = 1
        program.save()
        return True

    @staticmethod
    def upload(prog_id):
        """when the prgram is uploaded
        """
        progs = Program.objects.filter(id=prog_id)
        if progs.exists():
            program = progs.last()
        else:
            return False

        program.status = 5
        program.upload_time = getdate_now()
        program.save()
        return True

    @staticmethod
    def set_likes(prog_id, like_count):
        """when the program is liked
        """
        progs = Program.objects.filter(id=prog_id)
        program = progs.last()

        program.likes = like_count
        program.save()
        return True

    @staticmethod
    def set_downloads(prog_id, download_count):
        """when the program is
        """
        progs = Program.objects.filter(id=prog_id)
        program = progs.last()

        program.downloads = download_count
        program.save()
        return True

    @staticmethod
    def count_user_downloadlog(user_id):
        """count user's program downloads
        """
        ret = 0
        progs = Program.objects.filter(**{
            'author' : user_id
        })
        for prog in progs:
            ret += prog.downloads

        return ret

    @staticmethod
    def refresh(program_id):
        """refresh
        """
        count = DownloadLogHelper.count_downloadlog(program_id)
        likes = LikeHelper.count_like(program_id)
        ProgramHelper.set_downloads(program_id, count)
        ProgramHelper.set_likes(program_id, likes)

    @staticmethod
    def change_status(program_id, source, target):
        """change the status
        """
        program = ProgramHelper.get_program(program_id)
        if program.get('status') != source:
            return False
        program = Program.objects.filter(id=program_id)
        prog = program.last()
        prog.status = target

        prog.save()
        return True
