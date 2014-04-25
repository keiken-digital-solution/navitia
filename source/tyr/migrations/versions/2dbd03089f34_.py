# Copyright (c) 2001-2014, Canal TP and/or its affiliates. All rights reserved.
#   
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#  
# Hope you'll enjoy and contribute to this project,
#     powered by Canal TP (www.canaltp.fr).
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
# IRC #navitia on freenode
# https://groups.google.com/d/forum/navitia
# www.navitia.io

"""Add StopArea, StopPoint, Poi, Admin, Route, Line, Network tables

and a view to rule them all

Revision ID: 2dbd03089f34
Revises: 423e8da9d857
Create Date: 2014-01-30 12:39:11.839925

"""

# revision identifiers, used by Alembic.
revision = '2dbd03089f34'
down_revision = '423e8da9d857'

from alembic import op
import sqlalchemy as sa
import geoalchemy2 as ga


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stop_point',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uri', sa.Text(), nullable=False),
    sa.Column('coord', ga.Geography(geometry_type='POINT', srid=4326, spatial_index=False), nullable=True),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('external_code', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uri')
    )
    op.create_index('ix_stop_point_external_code', 'stop_point', ['external_code'], unique=False)
    op.create_table('line',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uri', sa.Text(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('external_code', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uri')
    )
    op.create_index('ix_line_external_code', 'line', ['external_code'], unique=False)
    op.create_table('poi',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uri', sa.Text(), nullable=False),
    sa.Column('coord', ga.Geography(geometry_type='POINT', srid=4326, spatial_index=False), nullable=True),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('external_code', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uri')
    )
    op.create_index('ix_poi_external_code', 'poi', ['external_code'], unique=False)
    op.create_table('route',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uri', sa.Text(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('external_code', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uri')
    )
    op.create_index('ix_route_external_code', 'route', ['external_code'], unique=False)
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uri', sa.Text(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('external_code', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uri')
    )
    op.create_index('ix_admin_external_code', 'admin', ['external_code'], unique=False)
    op.create_table('network',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uri', sa.Text(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('external_code', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uri')
    )
    op.create_index('ix_network_external_code', 'network', ['external_code'], unique=False)
    op.create_table('stop_area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uri', sa.Text(), nullable=False),
    sa.Column('coord', ga.Geography(geometry_type='POINT', srid=4326, spatial_index=False), nullable=True),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('external_code', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uri')
    )
    op.create_index('ix_stop_area_external_code', 'stop_area', ['external_code'], unique=False)
    op.create_table('rel_stop_area_instance',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('instance_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['instance_id'], ['instance.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['object_id'], ['stop_area.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('object_id', 'instance_id')
    )
    op.create_table('rel_poi_instance',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('instance_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['instance_id'], ['instance.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['object_id'], ['poi.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('object_id', 'instance_id')
    )
    op.create_table('rel_network_instance',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('instance_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['instance_id'], ['instance.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['object_id'], ['network.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('object_id', 'instance_id')
    )
    op.create_table('rel_line_instance',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('instance_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['instance_id'], ['instance.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['object_id'], ['line.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('object_id', 'instance_id')
    )
    op.create_table('rel_admin_instance',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('instance_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['object_id'], ['admin.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['instance_id'], ['instance.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('object_id', 'instance_id')
    )
    op.create_table('rel_stop_point_instance',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('instance_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['instance_id'], ['instance.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['object_id'], ['stop_point.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('object_id', 'instance_id')
    )
    op.create_table('rel_route_instance',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('instance_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['instance_id'], ['instance.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['object_id'], ['route.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('object_id', 'instance_id')
    )

    op.execute("""
        CREATE VIEW ptobject AS
            SELECT id, uri, external_code, name, 'stop_area' as type FROM stop_area UNION
            SELECT id, uri, external_code, name, 'stop_point' as type FROM stop_point UNION
            SELECT id, uri, external_code, name, 'poi' as type FROM poi UNION
            SELECT id, uri, external_code, name, 'admin' as type FROM admin UNION
            SELECT id, uri, external_code, name, 'line' as type FROM line UNION
            SELECT id, uri, external_code, name, 'route' as type FROM route UNION
            SELECT id, uri, external_code, name, 'network' as type FROM network
                      ;""")
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.execute("DROP VIEW ptobject CASCADE;")
    op.drop_table('rel_route_instance')
    op.drop_table('rel_stop_point_instance')
    op.drop_table('rel_admin_instance')
    op.drop_table('rel_line_instance')
    op.drop_table('rel_network_instance')
    op.drop_table('rel_poi_instance')
    op.drop_table('rel_stop_area_instance')
    op.drop_index('ix_stop_area_external_code', 'stop_area')
    op.drop_table('stop_area')
    op.drop_index('ix_network_external_code', 'network')
    op.drop_table('network')
    op.drop_index('ix_admin_external_code', 'admin')
    op.drop_table('admin')
    op.drop_index('ix_route_external_code', 'route')
    op.drop_table('route')
    op.drop_index('ix_poi_external_code', 'poi')
    op.drop_table('poi')
    op.drop_index('ix_line_external_code', 'line')
    op.drop_table('line')
    op.drop_index('ix_stop_point_external_code', 'stop_point')
    op.drop_table('stop_point')
    ### end Alembic commands ###
