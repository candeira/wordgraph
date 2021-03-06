# Copyright 2014 Tennessee Leeuwenburg

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"Test of the Graphite JSON response object."
import json
import pytest
import py

import wordgraph
from tests.lib.compare import assertParagraph

def test_graphite_documentation():
    """Verify description of Graphite JSON response from Graphite docs.

    The Graphite JSON response is for a single timeseries with five,
    monotonically increasing data points with the series name 'entries'.

    There is no graph title for the response.
    """
    graphite_data = json.loads("""
[{
  "target": "entries",
  "datapoints": [
    [1.0, 1311836008],
    [2.0, 1311836009],
    [3.0, 1311836010],
    [5.0, 1311836011],
    [6.0, 1311836012]
  ]
}]
    """)

    graph = {'graphite_data': graphite_data}

    full_long = wordgraph.describe(graph, source='graphite')
    expected = """
    This graph shows the relationship between time and metric
    The x axis, time, ranges from 28 Jul 2011 06:53:28 to 28 Jul 2011 06:53:32
    The y axis, metric, ranges from 1.0 to 6.0
    It contains 1 series
    The entries series is loosely linear
    """

    assertParagraph(full_long, expected)


def test_titled_graphite_documentation():
    """Verify description of Graphite JSON response from Graphite docs for titled graph.

    Same as test_graphite_documentation, but graph has title.
    """
    graphite_data = json.loads("""
[{
  "target": "entries",
  "datapoints": [
    [1.0, 1311836008],
    [2.0, 1311836009],
    [3.0, 1311836010],
    [5.0, 1311836011],
    [6.0, 1311836012]
  ]
}]
    """)

    graph = {'title': 'Metric Over Time', 
             'graphite_data': graphite_data}

    full_long = wordgraph.describe(graph, source='graphite')

    expected = '''
    This graph, Metric Over Time, shows the relationship between time and metric.
    The x axis, time, ranges from 28 Jul 2011 06:53:28 to 28 Jul 2011 06:53:32.
    The y axis, metric, ranges from 1.0 to 6.0.
    It contains 1 series.
    The entries series is loosely linear
    '''

    assertParagraph(full_long, expected)


def test_server_requests():
    """Response data from Graphite server of fictional server requests.

    Fictional data represents server requests for four fictional web servers.
    Each server's request load are approximately linear.

    http://play.grafana.org/graphite/render?from=-15min&until=now&target=aliasByNode(scaleToSeconds(apps.fakesite.*.counters.requests.count%2C1)%2C2)&format=json
    """
    with open('tests/data/server_requests.json') as data:

        graph = {'graphite_data': json.load(data)}
        full_long = wordgraph.describe(graph, source='graphite')
        assert full_long is not None

def test_memory_usage():
    """Response data from Graphite server of fictional memory usage.

    Fictional data represents memory usage of a Graphite server.

    http://play.grafana.org/graphite/render?from=-15min&until=now&target=aliasByNode(integral(carbon.agents.ip-172-31-27-225-a.memUsage),3)&format=json
    """
    with open('tests/data/memory_usage.json') as data:
        graph = {'graphite_data': json.load(data)}
        full_long = wordgraph.describe(graph, source='graphite')
        expected = """
        This graph shows the relationship between time and metric
        The x axis, time, ranges from 04 Aug 2014 03:40:00 to 04 Aug 2014 03:54:00
        The y axis, metric, ranges from 44736512.0 to 671047680.0
        It contains 1 series
        """
        
        assertParagraph(full_long, expected)

