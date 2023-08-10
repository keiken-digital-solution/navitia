# Copyright (c) 2001-2023, Hove and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Hove (www.hove.com).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# channel `#navitia` on riot https://riot.im/app/#/room/#navitia:matrix.org
# https://groups.google.com/d/forum/navitia
# www.navitia.io
import logging


class PtJourneyFarePool(object):
    def __init__(
        self,
        future_manager,
        instance,
        request,
        request_id,
    ):
        self._future_manager = future_manager
        self._instance = instance
        self._request = request
        self._request_id = request_id
        self._backend = self._instance.get_pt_journey_fare(request['_pt_journey_fare'])
        self._fares_future = dict()
        self._logger = logging.getLogger(__name__)

    def async_compute_fare(self, pt_journeys, request_id):
        self._fares_future = self._future_manager.create_future(self._do, pt_journeys, request_id)

    def _do(self, pt_journeys, _request_id):
        return self._backend.get_pt_journey_fare(pt_journeys, _request_id)
