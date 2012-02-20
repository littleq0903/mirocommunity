# Miro Community - Easiest way to make a video website
#
# Copyright (C) 2009, 2010, 2011, 2012 Participatory Culture Foundation
#
# Miro Community is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Miro Community is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Miro Community. If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime, timedelta

from django.test import TestCase
from haystack import connections

from localtv.models import Video, Watch


class BaseTestCase(TestCase):
    def _clear_index(self):
        """Clears the search index."""
        backend = connections['default'].get_backend()
        backend.clear()

    def _update_index(self):
        """Updates the search index."""
        backend = connections['default'].get_backend()
        index = connections['default'].get_unified_index().get_index(Video)
        backend.update(index, index.index_queryset())
        
    def _rebuild_index(self):
        """Clears and then updates the search index."""
        self._clear_index()
        self._update_index()

    def create_video(self, name='Test.', status=Video.ACTIVE, site_id=1,
                     watches=0, **kwargs):
        """
        Factory function for creating videos. Supplies the following defaults:

        * name: 'Test'
        * status: :attr:`Video.ACTIVE`
        * site_id: 1

        In addition to kwargs for the video's fields, which are passed directly
        to :meth:`Video.objects.create`, takes a ``watches`` kwarg (defaults to
        0). If ``watches`` is greater than 0, that many :class:`.Watch`
        instances will be created, each successively one day further in the
        past.

        """
        video = Video.objects.create(name=name, status=status, site_id=site_id,
                                     **kwargs)
        for i in xrange(watches):
            Watch.objects.create(video=video, ip_address='0.0.0.0',
                                 timestamp=datetime.now() - timedelta(i))

        return video
