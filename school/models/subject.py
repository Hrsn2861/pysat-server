"""Models for Apply
"""
from django.db import models

from utils import getdate_now, date_to_string
from school.models.school import SchoolHelper

class Subject(models.Model):
    """Subject
    """
    title = models.CharField(max_length=256)
    description = models.TextField()
    school_id = models.IntegerField()
    create_time = models.DateTimeField()
    deadline = models.DateTimeField()

    class Meta:
        verbose_name = 'subject'
        verbose_name_plural = 'subjects'
        get_latest_by = 'id'

class SubjectHelper:
    """SchoolApply Helper
    """

    @staticmethod
    def add_subject(school_id, title, description, deadline):
        """add subject
        """
        subject = Subject(
            school_id=school_id,
            title=title,
            description=description,
            create_time=getdate_now(),
            deadline=deadline)
        subject.save()

    @staticmethod
    def mofidy_subject(subject_id, title=None, description=None, deadline=None):
        """modify subject
        """
        qs = Subject.objects.filter(id=subject_id)
        if qs.exists():
            subject = qs.last()
            if title is not None:
                subject.title = title
            if description is not None:
                subject.description = description
            if deadline is not None:
                subject.deadline = deadline
            subject.save()
            return True
        return False


    @staticmethod
    def get_subject_filter(school_id, listtype):
        """get school's subject filter

        listtype:
        - 0 to show all
        - 1 to show on-going
        - 2 to show overdue
        """
        ret = {'school_id' : school_id}
        if listtype == 0:
            pass
        elif listtype == 1:
            ret['deadline__gt'] = getdate_now()
        elif listtype == 2:
            ret['deadline__lte'] = getdate_now()
        else:
            return None
        return ret

    @staticmethod
    def get_subject_count(school_id, listtype):
        """get school's subject count
        """
        params = SubjectHelper.get_subject_filter(school_id, listtype)
        if params is None:
            return 0
        return Subject.objects.filter(**params).count()

    @staticmethod
    def get_subjects(school_id, listtype, page):
        """get school's subjects
        """
        params = SubjectHelper.get_subject_filter(school_id, listtype)
        if params is None:
            return []
        qs = Subject.objects.filter(**params)
        qs.order_by('-id')
        qs = qs[(page - 1) * 20 : page * 20]
        subjects = []
        for subject in qs:
            subjects.append({
                'id' : subject.id,
                'title' : subject.title,
                'description' : subject.description,
                'create_time' : date_to_string(subject.create_time),
                'deadline' : date_to_string(subject.deadline)
            })
        return subjects

    @staticmethod
    def get_subject_with_schoolid(subject_id):
        """get a subject
        """
        qs = Subject.objects.filter(id=subject_id)
        if qs.exists():
            subject = qs.last()
            return {
                'id' : subject.id,
                'title' : subject.title,
                'school_id' : subject.school_id,
                'description' : subject.description,
                'create_time' : date_to_string(subject.create_time),
                'deadline' : date_to_string(subject.deadline)
            }
        return None

    @staticmethod
    def get_subject(subject_id):
        """get a subject
        """
        qs = Subject.objects.filter(id=subject_id)
        if qs.exists():
            subject = qs.last()
            school = SchoolHelper.get_school(subject.school_id)
            if school is None:
                schoolname = '-'
            else:
                schoolname = school.get('schoolname')
            return {
                'id' : subject.id,
                'title' : subject.title,
                'schoolname' : schoolname,
                'description' : subject.description,
                'create_time' : date_to_string(subject.create_time),
                'deadline' : date_to_string(subject.deadline)
            }
        return None

    @staticmethod
    def get_subject_by_name(themename):
        """get a subject by name
        """
        qs = Subject.objects.filter(title=themename)
        if qs.exists():
            subject = qs.last()
            school = SchoolHelper.get_school(subject.school_id)
            if school is None:
                schoolname = '-'
            else:
                schoolname = school.get('schoolname')
            return {
                'id' : subject.id,
                'title' : subject.title,
                'schoolname' : schoolname,
                'description' : subject.description,
                'create_time' : date_to_string(subject.create_time),
                'deadline' : date_to_string(subject.deadline)
            }
        return None

    @staticmethod
    def delete_subject(subject_id):
        """delete a subject
        """
        qs = Subject.objects.filter(id=subject_id)
        if qs.exists():
            subject = qs.last()
        else:
            return False
        subject.delete()
        return True

    @staticmethod
    def modify_theme(subject_id, info):
        """modify user's info
        """
        if not isinstance(subject_id, int):
            return False
        subjects = Subject.objects.filter(id=subject_id)
        if subjects.exists():
            subject = subjects.last()
        else:
            return False

        title = info.get('title')
        description = info.get('description')
        deadline = info.get('deadline')

        if isinstance(title, str):
            subject.realname = title
        if isinstance(description, str):
            subject.description = description
        if isinstance(deadline, str):
            subject.deadline = deadline

        subject.save()
        return True
