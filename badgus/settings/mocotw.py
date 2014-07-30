# -*- coding: utf-8 -*-

from . import base
import sys

INSTALLED_APPS = [
    'gunicorn', 
    'jingo_minify',
    'badgus.mocotw',
] + list(base.INSTALLED_APPS)


class AwardingRule:
    def __init__(self, key, min=-1, max=sys.maxint, type='z'):
        self.key = key
        self.min = min
        self.max = max
        self.type = type

MOZTECH_AWARD_RULES = {
    '謀智台客徽章': AwardingRule('moztech-author-emails', type='s'),
    '發文1篇': AwardingRule('moztech-author-posts', 1),
    '發文2篇': AwardingRule('moztech-author-posts', 2),
    '發文5篇': AwardingRule('moztech-author-posts', 5),
    '發文10篇': AwardingRule('moztech-author-posts', 10),
    '發文20篇': AwardingRule('moztech-author-posts', 20),
    '發文30篇': AwardingRule('moztech-author-posts', 30),
    '發文40篇': AwardingRule('moztech-author-posts', 40),
    '發文50篇': AwardingRule('moztech-author-posts', 50),
    '發文75篇': AwardingRule('moztech-author-posts', 75),
    '發文100篇': AwardingRule('moztech-author-posts', 100),
    '文章1則留言': AwardingRule('moztech-author-post-comments', 1),
    '文章3則留言': AwardingRule('moztech-author-post-comments', 3),
    '文章5則留言': AwardingRule('moztech-author-post-comments', 5),
    '文章10則留言': AwardingRule('moztech-author-post-comments', 10),
    '文章20則留言': AwardingRule('moztech-author-post-comments', 20),
    '文章50則留言': AwardingRule('moztech-author-post-comments', 50),
    '文章20個讚': AwardingRule('moztech-author-post-likes', 20),
    '文章50個讚': AwardingRule('moztech-author-post-likes', 50),
    '文章100個讚': AwardingRule('moztech-author-post-likes', 100),
    '文章200個讚': AwardingRule('moztech-author-post-likes', 200),
    '文章500個讚': AwardingRule('moztech-author-post-likes', 500),
    '文章1000個讚': AwardingRule('moztech-author-post-likes', 1000),
    '文章500瀏覽人次': AwardingRule('moztech-author-post-visits', 500),
    '文章1000瀏覽人次': AwardingRule('moztech-author-post-visits', 1000),
    '文章5000瀏覽人次': AwardingRule('moztech-author-post-visits', 5000),
    '文章10000瀏覽人次': AwardingRule('moztech-author-post-visits', 10000),
    '謀智台客文章破百': AwardingRule('moztech-nth-post-author', 100, type='h'),
    '謀智台客文章破兩百': AwardingRule('moztech-nth-post-author', 200, type='h'),
    '謀智台客文章破五百': AwardingRule('moztech-nth-post-author', 500, type='h'),
    '謀智台客文章破千': AwardingRule('moztech-nth-post-author', 1000, type='h'),
}

MOZTECH_AUTHORS_FILE = '/home/elin/sql/moztech_names.csv'
