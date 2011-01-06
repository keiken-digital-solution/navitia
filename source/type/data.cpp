#include "data.h"

#include <boost/archive/text_oarchive.hpp>
#include <boost/archive/text_iarchive.hpp>
#include <boost/archive/binary_oarchive.hpp>
#include <boost/archive/binary_iarchive.hpp>
#include <fstream>

void Data::build_index(){
    stoppoint_of_stoparea.create(stop_areas, stop_points, &StopPoint::stop_area_idx);
    stop_area_by_name.create(stop_areas, &StopArea::name);
    
}

template<> Container<StopPoint> & Data::get() {return stop_points;}
template<> Container<StopArea> & Data::get() {return stop_areas;}
template<> Container<VehicleJourney> & Data::get() {return vehicle_journeys;}
template<> Container<Line> & Data::get() {return lines;}
template<> Container<ValidityPattern> & Data::get() {return validity_patterns;}
template<> Container<Route> & Data::get() {return routes;}

void Data::save(const std::string & filename) {
    std::ofstream ofs(filename.c_str());
    boost::archive::text_oarchive oa(ofs);
    oa << *this;
}

void Data::load(const std::string & filename) {
    std::ifstream ifs(filename.c_str());
    boost::archive::text_iarchive ia(ifs);
    ia >> *this;
}

void Data::save_bin(const std::string & filename) {
    std::ofstream ofs(filename.c_str(),  std::ios::out | std::ios::binary);
    boost::archive::binary_oarchive oa(ofs);
    oa << *this;
}

void Data::load_bin(const std::string & filename) {
    std::ifstream ifs(filename.c_str(),  std::ios::in | std::ios::binary);
    boost::archive::binary_iarchive ia(ifs);
    ia >> *this;
}