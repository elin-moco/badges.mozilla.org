from django.contrib.auth.models import User
import redis
from badger import Badge, Award
from badger.models import DeferredAward
from badgus.settings import MOZTECH_AWARD_RULES


def moztech_award_ceremony():
    r = redis.Redis('localhost')
    for slug, rule in MOZTECH_AWARD_RULES.items():
        try:
            badge = Badge.objects.get(slug=slug)
            print badge
            awardees = None
            if rule.type == 's':
                awardees = r.smembers(rule.key)
            elif rule.type == 'z':
                awardees = r.zrangebyscore(rule.key, rule.min, rule.max)
            elif rule.type == 'h':
                awardees = r.hmget(rule.key, rule.min)
            batch_award(badge, awardees)
        except RuntimeError as e:
            print e


def batch_award(badge, awardees):
    awardees = [u'%s' % x for x in awardees]
    print len(awardees)
    emails = filter_awarded(badge, awardees)
    print len(emails)
    users = User.objects.filter(email__in=emails)
    for user in users:
        emails.remove(user.email)
        a = Award(badge=badge, user=user)
        a.save()

    for email in emails:
        pass
        da = DeferredAward(badge=badge, email=email)
        da.save()


def filter_awarded(badge, awardees):
    awards = Award.objects.filter(badge=badge).select_related('user').values('user__email')
    awarded = set([x['user__email'] for x in awards])
    defawards = DeferredAward.objects.filter(badge=badge, email__isnull=False)
    awarded |= set(x.email for x in defawards)
    return set(awardees) - awarded