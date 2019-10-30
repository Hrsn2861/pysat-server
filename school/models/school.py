"""Models for School
"""
from django.db import models

from user.models import UserHelper

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
    def add_school(user_id, schoolname, description):
        """add school
        """
        school = School(schoolname=schoolname, description=description, creator=user_id)
        school.save()
        return school.id

    @staticmethod
    def school_to_dict(school):
        """school to dict
        """
        return {
            'schoolname' : school.school_name,
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
            schools.append(SchoolHelper.school_to_dict(school))
        return schools

    @staticmethod
    def get_school(school_id):
        """get school
        """
        schools = School.objects.filter(id=school_id)
        if schools.exists():
            school = schools.last()
            return {
                'id' : school_id,
                'schoolname' : school.schoolname,
                'description' : school.description,
                'creator' : UserHelper.get_name_by_id(school.creator)
            }
        return None
