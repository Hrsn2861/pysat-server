"""Models for School
"""
from django.db import models

from user.models import UserHelper
from user.models import PermissionHelper

class School(models.Model):
    """School
    """
    schoolname = models.CharField(max_length=128)
    description = models.TextField()
    creator = models.IntegerField()

    class Meta:
        verbose_name = 'school'
        verbose_name_plural = 'schools'
        get_latest_by = 'id'

class SchoolHelper:
    """School Helper
    """

    @staticmethod
    def add_school(user_id, schoolname, description, headmaster_id):
        """add school
        """
        school = School(schoolname=schoolname, description=description, creator=user_id)
        school.save()
        PermissionHelper.set_permission(headmaster_id, school.id, 4)
        return school.id

    @staticmethod
    def school_to_dict(school):
        """school to dict
        """
        return {
            'name' : school.school_name,
            'description' : school.description,
            'creator' : UserHelper.get_name_by_id(school.creator)
        }

    @staticmethod
    def get_school_filter(search_text=None):
        """get school filter
        """
        if search_text is None:
            return {}
        return {
            'schoolname__icontains' : search_text
        }

    @staticmethod
    def get_school_count(search_text=None):
        """get school count
        """
        params = SchoolHelper.get_school_filter(search_text)
        return School.objects.filter(**params).count()

    @staticmethod
    def get_school_list(page, search_text=None):
        """get school list
        """
        params = SchoolHelper.get_school_filter(search_text)
        qs = School.objects.filter(**params)
        qs = qs[(page - 1) * 20 : page * 20]
        schools = []
        for school in qs:
            schools.append(SchoolHelper.get_school(school.id))
        return schools

    @staticmethod
    def get_school(school_id):
        """get school
        """
        schools = School.objects.filter(id=school_id)
        headmaster_id = PermissionHelper.get_school_headmaster(school_id)
        if schools.exists():
            school = schools.last()
            return {
                'id' : school_id,
                'name' : school.schoolname,
                'description' : school.description,
                'headmaster' : UserHelper.get_name_by_id(headmaster_id),
                'population' : PermissionHelper.get_school_population(school_id)
            }
        return None

    @staticmethod
    def get_school_name(school_id):
        """get schoolname
        """
        schools = School.objects.filter(id=school_id)
        if schools.exists():
            school = schools.last()
            return school.schoolname
        return None

    @staticmethod
    def get_school_by_name(school_name):
        """get schoolname
        """
        schools = School.objects.filter(schoolname=school_name)
        if schools.exists():
            school = schools.last()
            headmaster_id = PermissionHelper.get_school_headmaster(school.id)
            return {
                'id' : school.id,
                'schoolname' : school.schoolname,
                'description' : school.description,
                'headmaster' : UserHelper.get_name_by_id(headmaster_id),
                'population' : PermissionHelper.get_school_population(school.id)
            }
        return None
