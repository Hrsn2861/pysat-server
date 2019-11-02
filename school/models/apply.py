"""Models for Apply
"""
from django.db import models

from utils import getdate_now
from user.models import UserHelper

class SchoolApply(models.Model):
    """Apply for join School
    """
    user_id = models.IntegerField()
    school_id = models.IntegerField()
    message = models.CharField(max_length=256)
    apply_time = models.DateTimeField()
    judge = models.IntegerField(default=0)
    status = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'schoolapply'
        verbose_name_plural = 'schoolapplies'
        get_latest_by = 'id'

class SchoolApplyHelper:
    """SchoolApply Helper
    """

    @staticmethod
    def add_apply(user_id, school_id, message):
        """add school
        """
        apply = SchoolApply(
            user_id=user_id,
            school_id=school_id,
            message=message,
            apply_time=getdate_now())
        apply.save()
        return True

    @staticmethod
    def apply_to_dict(apply):
        """apply to dict
        """
        print(apply, type(apply))
        if apply is None:
            return None
        data = {
            'userid' : apply.user_id,
            'schoolid' : apply.school_id,
            'message' : apply.message,
            'apply_time' : apply.apply_time,
            'judge' : apply.judge,
            'status' : apply.status
        }
        return data

    @staticmethod
    def get_apply_by_id(apply_id):
        """get apply by id
        """
        apply = SchoolApply.objects.filter(id=apply_id)
        if not apply.exists():
            return None
        return SchoolApplyHelper.apply_to_dict(apply.last())

    @staticmethod
    def get_apply(user_id, school_id):
        """get apply
        """
        apply = SchoolApply.objects.filter(user_id=user_id, school_id=school_id)
        if not apply.exists():
            return None
        return SchoolApplyHelper.apply_to_dict(apply.last())

    @staticmethod
    def get_applies_filter(school_id, listtype):
        """get school's applies filter

        listtype:
        - 0 to show all
        - 1 to show solved
        - 2 to show pending
        """
        ret = {'school_id' : school_id}
        if listtype == 0:
            pass
        elif listtype == 1:
            ret['status__gt'] = 0
        elif listtype == 2:
            ret['status'] = 0
        else:
            return None
        return ret

    @staticmethod
    def get_applies_count(school_id, listtype):
        """get school's applies count
        """
        params = SchoolApplyHelper.get_applies_filter(school_id, listtype)
        if params is None:
            return 0
        return SchoolApply.objects.filter(**params).count()

    @staticmethod
    def get_applies(school_id, listtype, page):
        """get school's applies
        """
        params = SchoolApplyHelper.get_applies_filter(school_id, listtype)
        if params is None:
            return 0
        qs = SchoolApply.objects.filter(**params)
        qs.order_by('apply_time')
        qs = qs[(page - 1) * 20 : page * 20]
        applies = []
        for apply in qs:
            username = UserHelper.get_name_by_id(apply.user_id)
            judge = UserHelper.get_name_by_id(apply.judge)
            applies.append({
                'id' : apply.id,
                'username' : username,
                'message' : apply.message,
                'time' : apply.apply_time,
                'judge' : judge,
                'status' : apply.status
            })
        return applies

    @staticmethod
    def judge_apply(apply_id, judge, status):
        """judge an apply
        """
        qs = SchoolApply.objects.filter(id=apply_id, status=0)
        if qs.exists():
            apply = qs.last()
            apply.judge = judge
            apply.status = status
            apply.save()
            return True
        return False
