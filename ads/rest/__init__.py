from flask_restplus import Api, Namespace

api = Api(version='1.0', title='Backend Service for JobScanner',
          description='Serving JobScanner',
          default='Jobscanner Backend',
          default_label="An API for searching and retrieving job ads.")

ns_alljobs = Namespace('All job ads',
                       description='Finding the majority of Job ads')


ns_skillsandtraits = Namespace('Skills and Traits',
                               description='Find all Skills and traits per occupation')

ns_jobgeolocation = Namespace('Job location for a specific job',
                       description='Generate job location for a specific job')

ns_jobgeocount = Namespace('Job count per kommun or lan',
                           description='Job count per kommun or lan for a specific job')


api.add_namespace(ns_alljobs, '/')
api.add_namespace(ns_skillsandtraits, '/')
api.add_namespace(ns_jobgeolocation, '/job-geolocation')
api.add_namespace(ns_jobgeocount, '/job-geocount')
