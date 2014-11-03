#Ballot API - Ballots for developers

**NOTE: THIS PROJECT IS NOT LIVE YET. SEE CURRENT STATUS BELOW.**

Use it here: https://www.ballotapi.com/api/

##What is Ballot API?
Ballot API is a database that contains information for what is on voting
ballots for each election. You can query based on location to see the ballot for
that location. Alternatively, you can query based on measure to see the
precincts that contain that measure.

##Why make Ballot API?
The purpose of this project is to make it easier to see what will be on your
ballot before you go vote. Most ballot databases are either local to their
particular jurisdiction (e.g. local county registrar of voters) or only contain
higher level measures (e.g. national measures/contests only). This project aims
to be a comprehensive source of ballot information for all levels of government.

##How do you use the Ballot API?
There are three ways to use the Ballot API. First, you can browse the database
by visiting https://www.ballotapi.com/api/ in a web browser. Second, you can
make API requests to https://www.ballotapi.com/api/ endpoints that are
documented below. Third, you can copy this repository to self-host the database
and make requests via either of the two methods described above to your
self-hosted repo (see "How to self-host" below on how to do this).

##Current Status
This project is in active development. The goal is to complete this project by
the 2016 United States general election.

* API docs - *first draft done, needs review*
* Database schema
* Test cases
* API implementation (json)
* API implementation (html)
* Continuous integration
* Status reports
* Database population
* User experience refinement

##Authentication
All requests are open to the public and do not need authentication.

##Object Formats
There are three base object formats: Election, Precinct, and Measure. Inside the
Precinct object, the "geo" field contains a GeoJSON object. Inside the Measure
object, the "choices" field contains a list of Choice objects. The rest of the
fields in all base objects are either integers or strings.

###Election
Election objects contains information on a particular election.

```
{
    "id": 123,     //unique id for this Election (integer)
    "date": "...", //date of the election (e.g. "2014-11-04") (YYYY-MM-DD)
    "info": "..."  //generic information on the election (string)
}
```

###Precinct
Precinct objects contain information for a particular geographical area. They
are the lowest common denominator for ballot measures in a particular election,
so any location with that Precinct will have the same list of ballot measures.
NOTE: Precincts are unique across elections, so you cannot use the same Precinct
id for a different Election (since Precinct boundaries change over time). The
"info" field may be the same, but is not guaranteed to be. Tracking precinct
changes across Elections is outside of the scope of this project.

```
{
    "id": 123,          //unique id for this Precinct (integer)
    "election_id": 123, //unique id for this Precinct's Election (integer)
    "measures": [...],  //list of Measure ids that will be (list of integers)
    "confirmed": "...", //date the measures list was confirmed to be accurate (YYYY-MM-DD or null)
    "info": "...",      //generic information about the Precinct (string)
    "geo": {...}        //the boundary for this Precinct (GeoJSON object)
}
```

###Measure
Measure objects contain information on ballot measures and contests.

```
{
    "id": 123,          //unique id for this Measure (integer)
    "election_id": 123, //unique id for this Measure's Election (integer)
    "precincts": [...], //list of Precinct ids that are (list of integers)
    "title": "...",     //title of the measure (e.g. "Mayor") (string)
    "info": "...",      //generic information about the measure (string)
    "type": "...",      //the type of measure (see Measure Types)
    "choices": [...],   //list of choices for the measure (list of Choice objects)
}
```

####Measure Types
These are the types of measures, which are the voting system used for the
choices. The API is agnostic to what kind of entity or contest is actually being
voted on (person, party, bond measure, etc.).

* "plurality" - choose one choice
* "approval" - choose all choices that you approve
* "instant-runoff" - choose first and second choices
* "ranked" - sort choices in order of preference (first is most preferred)

###Choice
Choice objects contain the details for each item in the choices list of the
Measure object. They do not have unique ids because they are always include in
the Measure object.

```
{
    "title": "...", //title of the choice (e.g. "John Smith") (string)
    "info": "...",  //generic information about the choice (string)
}
```

##API Reference
All Ballot API endpoints respond to only GET requests (i.e. read-only). There
are json and html formats for every endpoint. You can specify which format by
appending ".json" or ".html" to the end of the endpoint.

###/elections
Returns a list of Election objects. Can be filtered by id, location, or date.

####ids=&lt;id&gt;[,&lt;id&gt;,...]
Return elections filtered to only these comma separated ids. This is just the
plural form of the `/elections/&lt;id&gt;` endpoint.

Examples:

1. Elections 123 and 234:<br/>
https://www.ballotapi.com/api/elections.html?ids=123,234

####ll=&lt;latitude&gt;,&lt;longitude&gt;
Return only elections that include precincts that contain this location. You can
also specify multiple `ll` arguments to form a geographic polygon area.

Examples:

1. All the elections for 100 Market St, San Francisco, CA (37.7942635,-122.3955861):<br/>
https://www.ballotapi.com/api/elections.html?ll=37.7942635,-122.3955861

2. All the elections for the state of Wyoming (roughly 45.0013129,-111.055124 to 41.001425,-104.0532252):<br/>
https://www.ballotapi.com/api/elections.html?ll=45.0013129,-111.055124&ll=45.0013129,-104.0532252&ll=41.001425,-104.0532252&ll=41.001425,-111.055124

####dates=&lt;start_date&gt;:&lt;end_date&gt;
Return only elections within a certain date range. You can omit either the start
or end dates to leave that side open ended. Dates are inclusive, so results
include elections that happen on the start or end dates.

Examples:

1. All the elections for 2014:<br/>
https://www.ballotapi.com/api/elections.html?dates=2014-01-01:2014-12-31

2. All elections after Nov 4th, 2014 for 100 Market St, San Francisco, CA:<br/>
https://www.ballotapi.com/api/elections.html?dates=2014-11-05:&ll=37.7942635,-122.3955861

###/elections/&lt;id&gt;
Return the Election object for the specified id.

Examples:

1. Elections 123:<br/>
https://www.ballotapi.com/api/elections/123.html

###/precincts
Return a list of precincts. Can be filtered by id, election, election date,
location, or measure.

####ids=&lt;id&gt;[,&lt;id&gt;,...]
Return precincts filtered to only these comma separated ids. This is just the
plural form of the `/precincts/<id>` endpoint.

Examples:

1. Precincts 123 and 234: https://www.ballotapi.com/api/precincts.html?ids=123,234

####election_ids=&lt;id&gt;[,&lt;id&gt;,...]
Return only precincts that are part of these elections. Multiple elections can
be listed as comma separated ids, which will return precincts that contain any
of the listed elections (i.e. treated as OR).

Examples:

1. The precincts that contain Election 123:<br/>
https://www.ballotapi.com/api/precincts.html?election_ids=123

2. The precincts that contain Election 123 or 234 for 100 Market St, San Francisco, CA:<br/>
https://www.ballotapi.com/api/precincts.html?election_ids=123,234&ll=37.7942635,-122.3955861

####election_dates=&lt;start_date&gt;:&lt;end_date&gt;
Return only precincts that belong to elections within a certain date range. You
can omit either the start or end dates to leave that side open ended. Dates are
inclusive, so results include elections that happen on the start or end dates.

Examples:

1. All the precincts for elections in 2014:<br/>
https://www.ballotapi.com/api/precincts.html?election_dates=2014-01-01:2014-12-31

2. All the precincts for elections after Nov 4th, 2014 for 100 Market St, San Francisco, CA:<br/>
https://www.ballotapi.com/api/precincts.html?election_dates=2014-11-05:&ll=37.7942635,-122.3955861

####ll=&lt;latitude&gt;,&lt;longitude&gt;
Return only precincts that contain this location. You can also specify multiple
`ll` arguments to form a geographic polygon area.

Examples:

1. The Election 123 precinct for 100 Market St, San Francisco, CA:<br/>
https://www.ballotapi.com/api/precincts.html?elections=123&ll=37.7942635,-122.3955861

2. All Election 123 and 456 precincts for the state of Wyoming:<br/>
https://www.ballotapi.com/api/precincts.html?elections=123,456&ll=45.0013129,-111.055124&ll=45.0013129,-104.0532252&ll=41.001425,-104.0532252&ll=41.001425,-111.055124

####measures=&lt;id&gt;[,&lt;id&gt;,...]
Return only precincts that contain these measures. Multiple measures can be
listed as comma separated ids, which will return precincts that contain any of
the listed measures (i.e. treated as OR). Multiple measures parameters will
intersect the precincts returned by each measures parameter (i.e. treated as
AND).

Examples:

1. The precincts that contain Measure 456:<br/>
https://www.ballotapi.com/api/precincts.html?measures=456

2. The precincts that contain Measures 456 or 567, and contains Measure 789:<br/>
https://www.ballotapi.com/api/precincts.html?measures=456,567&measures=789

###/precincts/&lt;id&gt;
Return the Precinct object for the specified id.

Examples:

1. Precinct 123:<br/>
https://www.ballotapi.com/api/precincts/123.html

###/measures
Return a list of measures. Can be filtered by id, election, election date,
location, or precinct.

####ids=&lt;id&gt;[,&lt;id&gt;,...]
Return measures filtered to only these comma separated ids. This is just the
plural form of the `/measures/<id>` endpoint.

Examples:

1. Measures 123 and 234:<br/>
https://www.ballotapi.com/api/measures.html?ids=123,234

####elections=&lt;id&gt;[,&lt;id&gt;,...]
Return only measures that are part of these elections. Multiple elections can
be listed as comma separated ids, which will return measures that contain any
of the listed elections (i.e. treated as OR).

Examples:

1. The measures that are in Election 123:<br/>
https://www.ballotapi.com/api/measures.html?elections=123

2. The measures that contain Election 123 or 234 for 100 Market St, San Francisco, CA:<br/>
https://www.ballotapi.com/api/measures.html?elections=123,234&ll=37.7942635,-122.3955861

####election_dates=&lt;start_date&gt;:&lt;end_date&gt;
Return only measures that belong to elections within a certain date range. You
can omit either the start or end dates to leave that side open ended. Dates are
inclusive, so results include elections that happen on the start or end dates.

Examples:

1. All the measures for elections in 2014:<br/>
https://www.ballotapi.com/api/measures.html?election_dates=2014-01-01:2014-12-31

2. All the measures for elections after Nov 4th, 2014 for 100 Market St, San Francisco, CA:<br/>
https://www.ballotapi.com/api/measures.html?election_dates=2014-11-05:&ll=37.7942635,-122.3955861

####ll=&lt;latitude&gt;,&lt;longitude&gt;
Return only measures that have a precinct within this location. You can also
specify multiple `ll` arguments to form a geographic polygon area.

Examples:

1. The Election 123 measures for 100 Market St, San Francisco, CA:<br/>
https://www.ballotapi.com/api/measures.html?elections=123&ll=37.7942635,-122.3955861

2. All Election 123 and 456 measures for the state of Wyoming:<br/>
https://www.ballotapi.com/api/measures.html?elections=123,456&ll=45.0013129,-111.055124&ll=45.0013129,-104.0532252&ll=41.001425,-104.0532252&ll=41.001425,-111.055124

####precincts=&lt;id&gt;[,&lt;id&gt;,...]
Return only measures that are a part of these precincts. Multiple precincts can
be listed as comma separated ids, which will return measures that are a part of
any of the listed precincts (i.e. treated as OR). Multiple precincts parameters
will intersect the measures returned by each precincts parameter (i.e. treated
as AND).

Examples:

1. The measures that contain Precinct 456:<br/>
https://www.ballotapi.com/api/measures.html?precincts=456

2. The measures that are a part of Precinct 456 or 567, and a part of Precinct 789:<br/>
https://www.ballotapi.com/api/measures.html?precincts=456,567&precincts=789

###/measures/&lt;id&gt;
Return the Measure object for the specified id.

Examples:

1. Measure 123:<br/>
https://www.ballotapi.com/api/measures/123.html

##How to self-host
Want to set up your own mirror of this API? Great! Here's how:

1. Download this repo.
2. Install the prerequisites:
  * PostgreSQL
  * PostGIS
  * Python
  * Psycopg
3. Add the database user.
4. Import the database.
5. Start the API server.
6. Try it out! http://localhost:8000/api/

To update to the latest version of the API, simply re-download this repo and
re-import the database.

##License
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to http://unlicense.org

###Exceptions
* The PageDown minified javascript library included in /index.html is released
under a BSD-style open source license. This is only used to format this README
documentation and is not required to actually run the API. Just delete
/index.html when you copy this repo to be 100% public domain.

##Contributions
This project is hosted https://github.com/diafygi/ballotapi and maintained by
a team at Code for America. Want to contribute?
