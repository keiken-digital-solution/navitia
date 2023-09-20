# coding=utf-8
# Copyright (c) 2001-2022, Hove and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
# the software to build cool stuff with public transport.
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

from __future__ import absolute_import, unicode_literals


import navitiacommon.type_pb2 as type_pb2
from jormungandr.olympic_site_params_manager import OlympicSiteParamsManager
from jormungandr.street_network.tests.streetnetwork_test_utils import make_pt_object
from jormungandr.instance import Instance

default_olympic_site_params = {
    "poi:BCD": {
        "departure": "default",
        "arrival": "default",
        "scenarios": {
            "default": {
                "stop_point:463685": {"attractivity": 1, "virtual_fallback": 10},
                "stop_point:463686": {"attractivity": 3, "virtual_fallback": 150},
            }
        },
    },
    "poi:EFG": {
        "departure": "departure_scenario",
        "arrival": "arrival_scenario",
        "scenarios": {
            "default": {
                "stop_point:463685": {"attractivity": 1, "virtual_fallback": 10},
                "stop_point:463686": {"attractivity": 3, "virtual_fallback": 150},
            },
            "departure_scenario": {
                "stop_point:463685": {"attractivity": 11, "virtual_fallback": 100},
                "stop_point:463686": {"attractivity": 30, "virtual_fallback": 15},
            },
            "arrival_scenario": {
                "stop_point:463685": {"attractivity": 12, "virtual_fallback": 99},
                "stop_point:463686": {"attractivity": 29, "virtual_fallback": 50},
            },
        },
    },
}


DEFAULT_OLYMPICS_FORBIDDEN_URIS = {
    "pt_object_olympics_forbidden_uris": ["nt:abc"],
    "poi_property_key": "olympic",
    "poi_property_value": "1234",
    "min_pt_duration": 15,
}


class FakeInstance(Instance):
    def __init__(self, name="fake_instance", olympics_forbidden_uris=None):
        super(FakeInstance, self).__init__(
            context=None,
            name=name,
            zmq_socket=None,
            street_network_configurations=[],
            ridesharing_configurations={},
            instance_equipment_providers=[],
            realtime_proxies_configuration=[],
            pt_planners_configurations={},
            zmq_socket_type=None,
            autocomplete_type='kraken',
            streetnetwork_backend_manager=None,
            external_service_provider_configurations=[],
            olympics_forbidden_uris=olympics_forbidden_uris,
        )


def test_get_departure_olympic_site_params():
    osp = OlympicSiteParamsManager("", "idfm")
    osp.olympic_site_params = default_olympic_site_params
    default_scenario = osp.get_dict_scenario("poi:BCD", "departure")
    attractivity_virtual_fallback = default_scenario["stop_point:463685"]
    assert attractivity_virtual_fallback.attractivity == 1
    assert attractivity_virtual_fallback.virtual_duration == 10

    attractivity_virtual_fallback = default_scenario["stop_point:463686"]
    assert attractivity_virtual_fallback.attractivity == 3
    assert attractivity_virtual_fallback.virtual_duration == 150

    default_scenario = osp.get_dict_scenario("poi:EFG", "departure")
    attractivity_virtual_fallback = default_scenario["stop_point:463685"]
    assert attractivity_virtual_fallback.attractivity == 11
    assert attractivity_virtual_fallback.virtual_duration == 100

    attractivity_virtual_fallback = default_scenario["stop_point:463686"]
    assert attractivity_virtual_fallback.attractivity == 30
    assert attractivity_virtual_fallback.virtual_duration == 15


def test_get_arrival_olympic_site_params():
    osp = OlympicSiteParamsManager("", "idfm")
    osp.olympic_site_params = default_olympic_site_params
    default_scenario = osp.get_dict_scenario("poi:BCD", "arrival")
    attractivity_virtual_fallback = default_scenario["stop_point:463685"]
    assert attractivity_virtual_fallback.attractivity == 1
    assert attractivity_virtual_fallback.virtual_duration == 10

    attractivity_virtual_fallback = default_scenario["stop_point:463686"]
    assert attractivity_virtual_fallback.attractivity == 3
    assert attractivity_virtual_fallback.virtual_duration == 150

    default_scenario = osp.get_dict_scenario("poi:EFG", "arrival")
    attractivity_virtual_fallback = default_scenario["stop_point:463685"]
    assert attractivity_virtual_fallback.attractivity == 12
    assert attractivity_virtual_fallback.virtual_duration == 99

    attractivity_virtual_fallback = default_scenario["stop_point:463686"]
    assert attractivity_virtual_fallback.attractivity == 29
    assert attractivity_virtual_fallback.virtual_duration == 50


def test_get_olympic_site_params_with_request_params_and_without_criteria():
    osp = OlympicSiteParamsManager("", "idfm")
    osp.olympic_site_params = default_olympic_site_params
    api_request = dict()
    api_request["_olympics_sites_attractivities[]"] = [('stop_point:24113', 3), ('stop_point:24131', 30)]
    api_request["_olympics_sites_virtual_fallback[]"] = [('stop_point:24113', 800), ('stop_point:24131', 820)]
    res = osp.get_olympic_site_params(None, None, api_request, None)
    assert "arrival" in res
    assert "departure" not in res
    attractivity_virtual_fallback = res["arrival"]["stop_point:24113"]
    assert attractivity_virtual_fallback.attractivity == 3
    assert attractivity_virtual_fallback.virtual_duration == 800

    attractivity_virtual_fallback = res["arrival"]["stop_point:24131"]
    assert attractivity_virtual_fallback.attractivity == 30
    assert attractivity_virtual_fallback.virtual_duration == 820


def test_get_olympic_site_params_with_request_params_and_departure_criteria():
    osp = OlympicSiteParamsManager("", "idfm")
    osp.olympic_site_params = default_olympic_site_params
    api_request = dict()
    api_request["_olympics_sites_attractivities[]"] = [('stop_point:24113', 3), ('stop_point:24131', 30)]
    api_request["_olympics_sites_virtual_fallback[]"] = [('stop_point:24113', 800), ('stop_point:24131', 820)]
    api_request["criteria"] = "departure_stop_attractivity"

    res = osp.get_olympic_site_params(None, None, api_request, None)
    assert "arrival" not in res
    assert "departure" in res
    attractivity_virtual_fallback = res["departure"]["stop_point:24113"]
    assert attractivity_virtual_fallback.attractivity == 3
    assert attractivity_virtual_fallback.virtual_duration == 800

    attractivity_virtual_fallback = res["departure"]["stop_point:24131"]
    assert attractivity_virtual_fallback.attractivity == 30
    assert attractivity_virtual_fallback.virtual_duration == 820


def test_get_olympic_site_params_with_request_params_and_arrival_criteria():
    osp = OlympicSiteParamsManager("", "idfm")
    osp.olympic_site_params = default_olympic_site_params
    api_request = dict()
    api_request["_olympics_sites_attractivities[]"] = [('stop_point:24113', 3), ('stop_point:24131', 30)]
    api_request["_olympics_sites_virtual_fallback[]"] = [('stop_point:24113', 800), ('stop_point:24131', 820)]
    api_request["criteria"] = "arrival_stop_attractivity"

    res = osp.get_olympic_site_params(None, None, api_request, None)
    assert "arrival" in res
    assert "departure" not in res
    attractivity_virtual_fallback = res["arrival"]["stop_point:24113"]
    assert attractivity_virtual_fallback.attractivity == 3
    assert attractivity_virtual_fallback.virtual_duration == 800

    attractivity_virtual_fallback = res["arrival"]["stop_point:24131"]
    assert attractivity_virtual_fallback.attractivity == 30
    assert attractivity_virtual_fallback.virtual_duration == 820


def test_get_olympic_site_params_without_request_params():
    osp = OlympicSiteParamsManager("", "idfm")
    osp.olympic_site_params = default_olympic_site_params
    api_request = dict()

    res = osp.get_olympic_site_params(None, None, api_request, None)
    assert "arrival" not in res
    assert "departure" not in res


def test_get_olympic_site_params_origin_poi_jo():
    osp = OlympicSiteParamsManager("", "idfm")
    osp.olympic_site_params = default_olympic_site_params
    api_request = dict()
    pt_origin_detail = make_pt_object(type_pb2.POI, 2, 3, "poi:BCD")
    property = pt_origin_detail.poi.properties.add()
    property.type = DEFAULT_OLYMPICS_FORBIDDEN_URIS["poi_property_key"]
    property.value = DEFAULT_OLYMPICS_FORBIDDEN_URIS["poi_property_value"]
    pt_destination_detail = make_pt_object(type_pb2.ADDRESS, 1, 2, "SA:BCD")
    instance = FakeInstance(olympics_forbidden_uris=DEFAULT_OLYMPICS_FORBIDDEN_URIS)

    res = osp.get_olympic_site_params(pt_origin_detail, pt_destination_detail, api_request, instance)
    assert "arrival" not in res
    assert "departure" in res

    assert res["departure"]["stop_point:463685"].attractivity == 1
    assert res["departure"]["stop_point:463685"].virtual_duration == 10

    assert res["departure"]['stop_point:463686'].attractivity == 3
    assert res["departure"]['stop_point:463686'].virtual_duration == 150


def test_get_olympic_site_params_arrival_poi_jo():
    osp = OlympicSiteParamsManager("", "idfm")
    osp.olympic_site_params = default_olympic_site_params
    api_request = dict()
    pt_origin_detail = make_pt_object(type_pb2.ADDRESS, 1, 2, "SA:BCD")

    pt_destination_detail = make_pt_object(type_pb2.POI, 2, 3, "poi:BCD")
    property = pt_destination_detail.poi.properties.add()
    property.type = DEFAULT_OLYMPICS_FORBIDDEN_URIS["poi_property_key"]
    property.value = DEFAULT_OLYMPICS_FORBIDDEN_URIS["poi_property_value"]
    instance = FakeInstance(olympics_forbidden_uris=DEFAULT_OLYMPICS_FORBIDDEN_URIS)

    res = osp.get_olympic_site_params(pt_origin_detail, pt_destination_detail, api_request, instance)
    assert "arrival" in res
    assert "departure" not in res

    assert res["arrival"]["stop_point:463685"].attractivity == 1
    assert res["arrival"]["stop_point:463685"].virtual_duration == 10

    assert res["arrival"]['stop_point:463686'].attractivity == 3
    assert res["arrival"]['stop_point:463686'].virtual_duration == 150


def test_get_olympic_site_params_departure_and_arrival_poi_jo():
    osp = OlympicSiteParamsManager("", "idfm")
    osp.olympic_site_params = default_olympic_site_params
    api_request = dict()

    pt_origin_detail = make_pt_object(type_pb2.POI, 1, 2, "poi:EFG")
    property = pt_origin_detail.poi.properties.add()
    property.type = DEFAULT_OLYMPICS_FORBIDDEN_URIS["poi_property_key"]
    property.value = DEFAULT_OLYMPICS_FORBIDDEN_URIS["poi_property_value"]

    pt_destination_detail = make_pt_object(type_pb2.POI, 2, 3, "poi:BCD")
    property = pt_destination_detail.poi.properties.add()
    property.type = DEFAULT_OLYMPICS_FORBIDDEN_URIS["poi_property_key"]
    property.value = DEFAULT_OLYMPICS_FORBIDDEN_URIS["poi_property_value"]

    instance = FakeInstance(olympics_forbidden_uris=DEFAULT_OLYMPICS_FORBIDDEN_URIS)

    res = osp.get_olympic_site_params(pt_origin_detail, pt_destination_detail, api_request, instance)
    assert "arrival" in res
    assert "departure" not in res

    assert res["arrival"]["stop_point:463685"].attractivity == 1
    assert res["arrival"]["stop_point:463685"].virtual_duration == 10

    assert res["arrival"]['stop_point:463686'].attractivity == 3
    assert res["arrival"]['stop_point:463686'].virtual_duration == 150


def test_build_olympic_site_params_empty_scenario():
    osp = OlympicSiteParamsManager("", "idfm")
    res = osp.get_dict_scenario(None, {})
    assert not res