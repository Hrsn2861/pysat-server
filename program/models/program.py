"""models for program
"""
from django.db import models

from utils import getdate_now, getdate_none
from program.models import ProgramLikeHelper

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

    class Meta:
        verbose_name = 'program'
        verbose_name_plural = 'programs'
        get_latest_by = 'id'

class ProgramHelper:
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
        return {
            'id' : program.id,
            'name' : program.name,
            'author' : program.author,
            'code' : program.code,
            'doc' : program.doc,
            'submit_time' : program.submit_time,
            'status' : program.status,
            'judge' : program.judge,
            'judge_time' : judge_time,
            'upload_time' : upload_time,
            'downloads' : program.downloads,
            'likes' : program.likes
        }

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
    def add_program(author, name, code, doc):
        """add program
        """
        Program(
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
            likes=0
        ).save()
        return True

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
    def get_programs_count(params):
        """get programs count with params
        """
        qs = Program.objects.filter(**params)
        return qs.count()

    @staticmethod
    def get_programs(params, page):
        """get programs with params
        """
        qs = Program.objects.filter(**params)
        qs = qs.order_by('-id')
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
    def get_user_programs(user_id, page):
        """get user's programs
        """
        return ProgramHelper.get_programs({'author' : user_id}, page)

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

        program.status = 3
        program.upload_time = getdate_now()
        program.save()
        return True

    @staticmethod
    def like_program(prog_id):
        """when the program is liked
        """
        progs = Program.objects.filter(id=prog_id)
        if progs.exists():
            program = progs.last()
        else:
            return False

        program.likes = ProgramLikeHelper.count_like(prog_id)
        program.save()
        return True
