# -*- coding: utf-8 -*-
import os

gettext = lambda s: s
_ = gettext


CMS_REDIRECTS = True
CMS_SEO_FIELDS = True
CMS_SHOW_START_DATE = True
CMS_SHOW_END_DATE = True

CMS_TEMPLATES = (
    ('_cms/single-column.html', 'Single Column - Standard Template'),
    ('_cms/two-column.html', 'Two Column - Standard Template'),
    ('_cms/home.html', 'One Pager - Home Template'),
)

CONTENT_PLUGINS = [
    'TextPlugin',
    'LinkPlugin'
]
CONTENT_PLUGINS.extend([
    'AppshotPlugin',
    'BoxedPlugin',
    'FAQMultiListPlugin',
    'FilerFilePlugin',
    'FilerImagePlugin',
    'FilerSVGPlugin',
    'MapPlugin',
    'SingleProductPlugin',
    'SnippetPlugin',
    'TextPlugin',
    'YouTubePlugin',
])

CMS_PLACEHOLDER_CONF = {
    'main_content': {
        #'plugins': ['TextPlugin', 'PicturePlugin'],
        #'text_only_plugins': ['LinkPlugin'],
        'extra_context': {"width": 640},
        'name': _("Content"),
    },
    'sidebar': {
        "plugins": ['TextPlugin', 'LinkPlugin'],
        "extra_context": {"width": 280},
        'name': _("Right Column"),
        'limits': {
            'global': 2,
            'TeaserPlugin': 1,
            'LinkPlugin': 1,
        },
    },
    'content_right': {
        #"plugins": CONTENT_PLUGINS,
        'name': "Main Content",
        'limits': {
            'global': 20,
            #'TeaserPlugin': 1,
        },
    },
    'content_left': {
        #"plugins": CONTENT_PLUGINS,
        'name': "Secondary Content",
        'limits': {
            'global': 20,
        },
    },
    'cms_onepage.html main_content': {
        "plugins": ['EmbeddedPagesPlugin', ]
    },

    'footer_popup_contact': {
        "plugins": ['TextPlugin', ]
    },
    'footer_popup_media': {
        "plugins": ['TextPlugin', ]
    },
    'footer_popup_bar': {
        "plugins": ['TextPlugin', ]
    },
    'footer_popup_haus': {
        "plugins": ['TextPlugin', ]
    },
}

COLUMN_WIDTH_CHOICES = (
    ('3', "1/4"),
    ('4', "1/3"),
    ('6', "1/2"),
    ('8', "2/3"),
    ('9', "3/4"),
    ('12', "1/1")
)


CMS_PLUGIN_PROCESSORS = ()

########## TEXT EDITOR CONFIGURATION
CKEDITOR_SETTINGS = {
    'language': '{{ language }}',
    'uiColor': '#ffffff',
    'toolbar_CMS': [
        ['Undo', 'Redo'],
        ['cmsplugins', 'ShowBlocks'],
        #['Format', 'Styles'],
        ['Styles',],
        ['Cut','Copy','Paste','PasteText', '-', 'Find','Replace'],
        ['NumberedList', 'BulletedList',],
        ['Source',],
        ['Bold',]
        #['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
    ],
    'startupOutlineBlocks': True,
    'skin': 'moono',

    'stylesSet': [

        # alternative to 'format' selector
        {'name': 'Paragraph', 'element': 'p',},
        {'name': 'Heading 1 (only _one_ per page!)', 'element': 'h1',},
        {'name': 'Heading 2', 'element': 'h2',},
        {'name': 'Heading 3', 'element': 'h3',},
        #{'name': 'Heading 4', 'element': 'h4',},
        {'name': 'Highlight', 'element': 'p', 'attributes': { 'class': 'marker highlight' }},
        #{'name': 'Dimmed', 'element': 'p', 'attributes': { 'class': 'dimmed' }},
        #{'name': 'Address', 'element': 'address',},

        #{'name': 'Cited Work', 'element': 'cite',},
        #{'name': 'Inline Quotation', 'element': 'q',},



        # custom elements
        #{'name': 'Italic Title',
        #'element': 'h2',
        #'styles': {
        #    'font-style': 'italic'
        #}},

    ]

}




TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(SITE_ROOT, 'templates'),
            os.path.join(SITE_ROOT, 'base', 'templates'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                # social auth
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                #
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                #'sekizai.context_processors.sekizai',
            ),
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'admin_tools.template_loaders.Loader',
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    'django.template.loaders.eggs.Loader',
                ]),
            ],
        },
    },
]

