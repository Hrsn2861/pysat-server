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
    reason = models.CharField(max_length=256)
    apply_time = models.DateTimeField()
    judger = models.IntegerField(default=0)
    status = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'schoolapply'
        verbose_name_plural = 'schoolapplies'
        get_latest_by = 'id'

class SchoolApplyHelper:
    """SchoolApply Helper
    """

    @staticmethod
    def add_apply(user_id, school_id, reason):
        """add school
        """
        apply = SchoolApply(
            user_id=user_id,
            school_id=school_id,
            reason=reason,
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
            'reason' : apply.reason,
            'apply_time' : apply.apply_time,
            'judger' : apply.judger,
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
    def get_applies_filter(school_id, list_type):
        """get school's applies filter

        list_type:
        - 0 to show all
        - 1 to show solved
        - 2 to show pending
        """
        ret = {'school_id' : school_id}
        if type == 0:
            pass
        elif type == 1:
            ret['status__gt'] = 0
        elif type == 2:
            ret['status'] = 0
        else:
            return None
        return ret

    @staticmethod
    def get_applies_count(school_id, list_type):
        """get school's applies count
        """
        params = SchoolApplyHelper.get_applies_filter(school_id, list_type)
        if params is None:
            return 0
        return SchoolApply.objects.filter(**params).count()

    @staticmethod
    def get_applies(school_id, list_type, page):
        """get school's applies
        """
        params = SchoolApplyHelper.get_applies_filter(school_id, list_type)
        if params is None:
            return 0
        qs = SchoolApply.objects.filter(**params)
        qs.order_by('apply_time')
        qs = qs[(page - 1) * 20 : page * 20]
        applies = []
        for apply in qs:
            username = UserHelper.get_name_by_id(apply.user_id)
            judger = UserHelper.get_name_by_id(apply.judger)
            applies.append({
                'id' : apply.id,
                'username' : username,
                'reason' : apply.reason,
                'time' : apply.apply_time,
                'judger' : judger,
                'status' : apply.status
            })
        return applies

    @staticmethod
    def judge_apply(apply_id, judger, status):
        """judge an apply
        """
        qs = SchoolApply.objects.filter(id=apply_id, status=0)
        if qs.exists():
            apply = qs.last()
            apply.judger = judger
            apply.status = status
            apply.save()
            return True
        return False
