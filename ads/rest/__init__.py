from flask_restplus import Api, Namespace

api = Api(version='1.0', title='Backend Service for JobScanner',
          description='Serving JobScanner',
          default='Jobscanner Backend',
          default_label="An API for searching and retrieving job ads.")

ns_alljobs = Namespace('All job ads',
                       description='Finding the majority of Job ads')


ns_skillsandtraits = Namespace('Skills and Traits',
                               description='Find all Skills and traits per occupation')

ns_jobgeolocation = Namespace('heatmap or job count per kommun',
                       description='Generate job count of a specific job for every kommun')

ns_jobcount = Namespace('Specific job count',
                        description='specific job count for every lan and kommun')

api.add_namespace(ns_alljobs, '/')
api.add_namespace(ns_skillsandtraits, '/')
api.add_namespace(ns_jobgeolocation, '/job-geolocation')
api.add_namespace(ns_jobcount, '/jobcount')
