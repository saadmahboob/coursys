from django.conf.urls import url
from courselib.urlparts import POST_SLUG, COURSE_SLUG, USERID_SLUG

ta_patterns = [ # prefix /ta/
    url(r'^$', 'ta.views.view_postings'),
    url(r'^new_posting$', 'ta.views.edit_posting'),
    url(r'^descriptions/$', 'ta.views.descriptions'),
    url(r'^descriptions/new$', 'ta.views.new_description'),
    url(r'^offers/$', 'ta.views.instr_offers'),
    url(r'^' + POST_SLUG + '/$', 'ta.views.new_application'),
    url(r'^' + POST_SLUG + '/_myinfo$', 'ta.views.get_info'),
    url(r'^' + POST_SLUG + '/manual$', 'ta.views.new_application_manual'),
    url(r'^' + POST_SLUG + '/offers$', 'ta.views.instr_offers'),
    url(r'^' + POST_SLUG + '/admin$', 'ta.views.posting_admin'),
    url(r'^' + POST_SLUG + '/applicant_csv$', 'ta.views.generate_csv'),
    url(r'^' + POST_SLUG + '/applicant_csv_by_course$', 'ta.views.generate_csv_by_course'),
    url(r'^' + POST_SLUG + '/edit$', 'ta.views.edit_posting'),
    url(r'^' + POST_SLUG + '/bu$', 'ta.views.edit_bu'),
    url(r'^' + POST_SLUG + '/bu_formset$', 'ta.views.bu_formset'),
    url(r'^' + POST_SLUG + '/apps/$', 'ta.views.assign_tas'),
    url(r'^' + POST_SLUG + '/' + COURSE_SLUG + '$', 'ta.views.assign_bus'),
    url(r'^' + POST_SLUG + '/all_apps$', 'ta.views.view_all_applications'),
    url(r'^' + POST_SLUG + '/print_all_applications$', 'ta.views.print_all_applications'),
    url(r'^' + POST_SLUG + '/print_all_applications_by_course$', 'ta.views.print_all_applications_by_course'),
    url(r'^' + POST_SLUG + '/late_apps$', 'ta.views.view_late_applications'),
    url(r'^' + POST_SLUG + '/financial$', 'ta.views.view_financial'),
    url(r'^' + POST_SLUG + '/contact', 'ta.views.contact_tas'),
    #url(r'^contracts', 'ta.views.all_contracts'),
    url(r'^' + POST_SLUG + '/contracts/$', 'ta.views.all_contracts'),
    url(r'^' + POST_SLUG + '/contracts/csv$', 'ta.views.contracts_csv'),
    url(r'^' + POST_SLUG + '/contracts/new$', 'ta.views.new_contract'),
    url(r'^' + POST_SLUG + '/contracts/forms$', 'ta.views.contracts_forms'),
    url(r'^' + POST_SLUG + '/contracts/' + USERID_SLUG + '/$', 'ta.views.view_contract'),
    url(r'^' + POST_SLUG + '/contracts/' + USERID_SLUG + '/new$', 'ta.views.edit_contract'),
    url(r'^' + POST_SLUG + '/contracts/' + USERID_SLUG + '/edit$', 'ta.views.edit_contract'),
    url(r'^' + POST_SLUG + '/contracts/' + USERID_SLUG + '/form', 'ta.views.view_form'),
    url(r'^' + POST_SLUG + '/contracts/' + USERID_SLUG + '/offer', 'ta.views.preview_offer'),
    url(r'^' + POST_SLUG + '/contracts/' + USERID_SLUG + '/accept$', 'ta.views.accept_contract'),
    url(r'^' + POST_SLUG + '/application/' + USERID_SLUG + '$', 'ta.views.view_application'),
    url(r'^' + POST_SLUG + '/application/' + USERID_SLUG + '/update$', 'ta.views.update_application'),
    url(r'^' + POST_SLUG + '/application/' + USERID_SLUG + '/edit', 'ta.views.edit_application'),
]

tug_patterns = [ # prefix /tugs/
    url(r'^$', 'ta.views.all_tugs_admin'),
    url(r'^(?P<semester_name>\d+)$', 'ta.views.all_tugs_admin'),
]