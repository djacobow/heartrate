#!/usr/local/bin/python3

import falcon

import measure
import statics

app = application = falcon.API()

one_user = measure.MeasureOneClient()
app.add_route('/api/v1/users/{userid}',one_user)
all_users = measure.MeasureAllClients()
app.add_route('/api/v1/users',all_users)
static_stuff = statics.StaticStuff()
app.add_route('/statics/{fname}',static_stuff)

