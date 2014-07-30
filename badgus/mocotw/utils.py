from django.contrib.auth.models import User
import redis
from badger import Badge, Award
from badger.models import DeferredAward
from badgus.settings import MOZTECH_AWARD_RULES, MOZTECH_AUTHORS_FILE
import csv


def export_authors():
    with open(MOZTECH_AUTHORS_FILE, 'r') as authors_file:
        authors = csv.reader(authors_file, delimiter=',')
        authorBadges = {}
        authorSlugs = {}
        for author in authors:
            id = author[0].strip()
            email = author[1].strip()
            user = User.objects.filter(email=email)
            if user.exists():
                authorSlugs[id] = user[0].username
            awardCount = Award.objects.filter(user__email=email).count()
            defawardCount = DeferredAward.objects.filter(email=email).count()
            authorBadges[id] = awardCount + defawardCount
        print authorBadges
        r = redis.Redis('localhost')
        r.delete('moztech-author-badges')
        r.delete('moztech-author-badges-slug')
        r.hmset('moztech-author-badges', authorBadges)
        r.hmset('moztech-author-badges-slug', authorSlugs)


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
            if awardees:
                batch_award(badge, awardees)
        except Exception as e:
            print e


def batch_award(badge, awardees):
    awardees = [u'%s' % x for x in awardees if x]
    print 'Awardees: %s' % len(awardees)
    emails = filter_awarded(badge, awardees)
    print 'Filtered: %s' % len(emails)
    users = User.objects.filter(email__in=emails)
    creator = User.objects.get(pk=1)
    for user in users:
        emails.remove(user.email)
        a = Award(badge=badge, user=user, creator=creator)
        a.save()

    for email in emails:
        if email:
            da = DeferredAward(badge=badge, email=email, creator=creator)
            da.save()


def filter_awarded(badge, awardees):
    awards = Award.objects.filter(badge=badge).select_related('user').values('user__email')
    awarded = set([x['user__email'] for x in awards])
    defawards = DeferredAward.objects.filter(badge=badge, email__isnull=False)
    awarded |= set(x.email for x in defawards)
    return set(awardees) - awarded