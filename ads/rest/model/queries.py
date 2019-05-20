from flask_restplus import reqparse, inputs
from ads import settings

allJobs_query = reqparse.RequestParser()
allJobs_query.add_argument('q')
allJobs_query.add_argument(settings.OFFSET,
                           type=inputs.int_range(0, settings.MAX_OFFSET),
                           default=0)
allJobs_query.add_argument(settings.LIMIT,
                            type=inputs.int_range(0, settings.MAX_LIMIT),
                            default=10)
allJobs_query.add_argument(settings.SHOW_EXPIRED, choices=['true', 'false'], default='false')
allJobs_query.add_argument(settings.PLACE, action='append')


skillsandtraits_query = reqparse.RequestParser()
skillsandtraits_query.add_argument('q', required=True,
                                   location='args',
                                   help="Must provide an occupation name!")

skillsandtraits_query.add_argument(settings.SHOW_EXPIRED, choices=['true', 'false'], default='false')
skillsandtraits_query.add_argument(settings.PLACE, action='append')
