#Ballot API - Ballots for developers

**NOTE: THIS PROJECT IS NOT LIVE YET. SEE PROGRESS AT [GITHUB](https://github.com/sfbrigade/ballotapi).**

Use it here: http://www.ballotapi.com/api/ (doesn't work yet)

##Table of Contents
1. [What is Ballot API?](#what-is-ballot-api)
2. [Why make Ballot API?](#why-make-ballot-api)
3. [How do you use Ballot API?](#how-do-you-use-ballot-api)
4. [Current Status](#current-status)
5. [Authentication](#authentication)
6. [Response Formats](#response-formats)
7. [Object Formats](#object-formats)
  1. [Election](#election)
  2. [Precinct](#precinct)
  3. [Measure](#measure)
  4. [Choice](#choice)
8. [API Reference](#api-reference)
  1. [/elections/&lt;id&gt;](#electionsid)
  2. [/elections](#elections)
  3. [/precincts/&lt;id&gt;](#precinctsid)
  4. [/precincts](#precincts)
  5. [/measures/&lt;id&gt;](#measuresid)
  6. [/measures](#measures)
9. [How to self-host](#how-to-self-host)
10. [License](#license)
11. [Contributions](#contributions)

##<span id="what-is-ballot-api">What is Ballot API?</span>
Ballot API is a database that contains information for what is on voting
ballots for each election. You can query based on location to see the ballot for
that location. Alternatively, you can query based on measure to see the
precincts that contain that measure.

##<span id="why-make-ballot-api">Why make Ballot API?</span>
The purpose of this project is to make it easier to see what will be on your
ballot before you go vote. Most ballot databases are either local to their
particular jurisdiction (e.g. local county registrar of voters) or only contain
higher level measures (e.g. national measures/contests only). This project aims
to be a comprehensive source of ballot information for all levels of government.

##<span id="how-do-you-use-ballot-api">How do you use Ballot API?</span>
There are three ways to use the Ballot API. First, you can browse the database
by visiting http://www.ballotapi.com/api/ in a web browser. Second, you can
make API requests to http://www.ballotapi.com/api/ endpoints that are
documented below. Third, you can copy this repository to self-host the database
and make requests via either of the two methods described above to your
self-hosted repo (see "How to self-host" below on how to do this).

##<span id="current-status">Current Status</span>
This project is in active development. Please file [issues](https://github.com/sfbrigade/ballotapi/issues) if you find bugs or want to request changes.

* API docs - *done*
* Database schema - *done*
* Test cases
* API implementation (json) - *in development*
* API implementation (html)
* Demo webapp - *in development*
* Continuous integration
* Status reports
* Database population
* User experience refinement

##<span id="authentication">Authentication</span>
All requests are open to the public and do not need authentication.

##<span id="response-formats">Response Formats</span>
If you request an individual object (e.g. `/elections/123`), you will receive just that object (see [Object Formats](#object-formats)). If you request a list of objects (e.g. `/elections?dates=2014-01-01:2014-12-31`), you will recieve a paginated list of objects in the following format:

```
{
    "offset": 0, //where in the results this data list starts
    "data": [
        <json_object>,
        <json_object>,
        ...
    ]
}
```

Any API endpoint that returns a list of objects will accept optional `limit=<int>` and `offset=<int>` parameters in the request. See each endpoint for the default values of these parameters.

##<span id="object-formats">Object Formats</span>
There are three base object formats: Election, Precinct, and Measure. Inside the
Precinct object, the "geo" field contains a GeoJSON object. Inside the Measure
object, the "choices" field contains a list of Choice objects. The rest of the
fields in all base objects are either integers or strings.

###<span id="election">Election</span>
Election objects contains information on a particular election.

```
{
    "id": 123,     //unique id for this Election (integer)
    "date": "...", //date of the election (e.g. "2014-11-04") (YYYY-MM-DD)
    "info": "..."  //generic information on the election (string)
}
```

###<span id="precinct">Precinct</span>
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

###<span id="measure">Measure</span>
Measure objects contain information on ballot measures and contests.

```
{
    "id": 123,              //unique id for this Measure (integer)
    "election_id": 123,     //unique id for this Measure's Election (integer)
    "precincts": [...],     //list of Precinct ids that are (list of integers)
    "title": "...",         //title of the measure (string)
                            //(e.g. "Water and Rail Supervisor - District 23")
    "question": "...",      //question that the voter is asked to answer (string)
                            //(e.g. "Choose one of the following candidates.")
    "info": "...",          //generic information about the measure (string)
                            //(e.g. "This seat oversees the budgets of ...")
    "short_info": "...",    //<100 character version of the info field (string)
                            //(e.g. "This seat manages agriculture departments.")
    "type": "...",          //the type of measure (see Measure Type)
    "voting_method": "...", //the method of voting (see Voting Method)
    "threshold": "...",     //the threshold needed for a choice to win (see Threshold)
    "choices": [...],       //list of choices for the measure (list of Choice objects)
}
```

####<span id="measure-type">Measure Type</span>
These are the types of measure (i.e. what kind of question is being asked). They will be one of the following strings:

* "election" - voting is to elect a person or party
* "measure" - voting is to decide on a specific initiative or policy

####<span id="voting-method">Voting Method</span>
These are the voting methods for measures, which are the voting system used
for the choices. The API is agnostic to what kind of entity or contest is
actually being voted on (person, party, bond measure, etc.).

* "plurality" - choose one choice
* "approval" - choose all choices that you approve
* "instant-runoff" - choose first and second choices
* "ranked" - sort choices in order of preference (first is most preferred)

####<span id="threshold">Threshold</span>
These are the winning threshold requirements that the measure. The values in
this field are strings because thresholds are often not as simple as a given
number or percentage.

* "1/2 + 1" - A majority is required (i.e. more than 50% of votes)
* "2/3 + 1" - A two-thirds majority is required (i.e. more than 67% of votes)
* "max, &gt;30%" - The most voted for choice, and that choice has to win over 30% of all votes.
* *Need more. Please pull request!*

###<span id="choice">Choice</span>
Choice objects contain the details for each item in the choices list of the
Measure object. They do not have unique ids because they are always include in
the Measure object.

```
{
    "title": "...",       //title of the choice (e.g. "John Smith") (string)
    "info": "...",        //generic information about the choice (string)
}
```

##<span id="api-reference">API Reference</span>
All Ballot API endpoints respond to only GET requests (i.e. read-only). There
are json and html formats for every endpoint. You can specify which format by
appending ".json" or ".html" to the end of the endpoint.

###<span id="electionsid">/elections/&lt;id&gt;</span>
Return the Election object for the specified id.

Examples:

1. Elections 1:<br/>
http://www.ballotapi.com/api/elections/1

###<span id="elections">/elections</span>
Returns a list of Election objects. Can be filtered by id, location, or date.

####?ids=&lt;id&gt;[,&lt;id&gt;,...]
Return elections filtered to only these comma separated ids. This is just the
plural form of the `/elections/<id>` endpoint.

Examples:

1. Elections 1 and 2:<br/>
http://www.ballotapi.com/api/elections?ids=1,2

####?coords=&lt;latitude&gt;,&lt;longitude&gt;
Return only elections that include precincts that contain this location.

Examples:

1. All the elections for 100 Market St, San Francisco, CA (37.7942635,-122.3955861):<br/>
http://www.ballotapi.com/api/elections?coords=37.7942635,-122.3955861

####?election_dates=&lt;start_date&gt;[:&lt;end_date&gt;[,...]]
Return only elections within a certain date range. You can omit either the start
or end dates to leave that side open ended. Dates are inclusive, so results
include elections that happen on the start or end dates. You can also specify a
single date, which is the equivalent to specifying that date as both the start
and end date. You can also have multiple date ranges, separated by commas.

Examples:

1. The national elections in 2016 and 2020:<br/>
http://www.ballotapi.com/api/elections?election_dates=2016-11-04,2020-11-04

2. All the elections for 2014:<br/>
http://www.ballotapi.com/api/elections?election_dates=2014-01-01:2014-12-31

3. All elections after Nov 4th, 2014 for 100 Market St, San Francisco, CA:<br/>
http://www.ballotapi.com/api/elections?election_dates=2014-11-05:2050-11-05&coords=37.7942635,-122.3955861

####?limit=&lt;int&gt;
Limit results to a set number. By default, the limit value for elections is 100.

####?offset=&lt;int&gt;
Start the list of results at an offset. By default, the offset value is 0 (e.g.
start the results at the beginning).

###<span id="precinctsid">/precincts/&lt;id&gt;</span>
Return the Precinct object for the specified id.

Examples:

1. Precinct 1:<br/>
http://www.ballotapi.com/api/precincts/1

###<span id="precincts">/precincts</span>
Return a list of precincts. Can be filtered by id, election, election date,
location, or measure.

####?ids=&lt;id&gt;[,&lt;id&gt;,...]
Return precincts filtered to only these comma separated ids. This is just the
plural form of the `/precincts/<id>` endpoint.

Examples:

1. Precincts 1 and 2: http://www.ballotapi.com/api/precincts?ids=1,2

####?elections=&lt;id&gt;[,&lt;id&gt;,...]
Return only precincts that are part of these elections. Multiple elections can
be listed as comma separated ids, which will return precincts that contain any
of the listed elections (i.e. treated as OR).

Examples:

1. The precincts that contain Election 1:<br/>
http://www.ballotapi.com/api/precincts?elections=1

2. The precincts that contain Election 1 or 2 for 100 Market St, San Francisco, CA:<br/>
http://www.ballotapi.com/api/precincts?elections=1,2&coords=37.7942635,-122.3955861

####?election_dates=&lt;start_date&gt;[:&lt;end_date&gt;[,...]]
Return only precincts that belong to elections within a certain date range. You
can omit either the start or end dates to leave that side open ended. Dates are
inclusive, so results include elections that happen on the start or end dates.
You can also specify a single date, which is the equivalent to specifying that
date as both the start and end date. You can also have multiple date ranges,
separated by commas.

Examples:

1. All the precincts for elections in 2014:<br/>
http://www.ballotapi.com/api/precincts?election_dates=2014-01-01:2014-12-31

2. All the precincts for elections after Nov 4th, 2014 for 100 Market St, San Francisco, CA:<br/>
http://www.ballotapi.com/api/precincts?election_dates=2014-11-05:2050-11-05&coords=37.7942635,-122.3955861

####?coords=&lt;latitude&gt;,&lt;longitude&gt;
Return only precincts that contain this location.

Examples:

1. The Election 1 precinct for 100 Market St, San Francisco, CA:<br/>
http://www.ballotapi.com/api/precincts?elections=1&coords=37.7942635,-122.3955861

####?measures=&lt;id&gt;[,&lt;id&gt;,...]
Return only precincts that contain these measures. Multiple measures can be
listed as comma separated ids, which will return precincts that contain any of
the listed measures (i.e. treated as OR). Multiple measures parameters will
intersect the precincts returned by each measures parameter (i.e. treated as
AND).

Examples:

1. The precincts that contain Measure 2:<br/>
http://www.ballotapi.com/api/precincts?measures=2

2. The precincts that contain Measures 2 or 3, and contains Measure 1:<br/>
http://www.ballotapi.com/api/precincts?measures=2,3&measures=1

####?limit=&lt;int&gt;
Limit results to a set number. By default, the limit value for precincts is 50.

####?offset=&lt;int&gt;
Start the list of results at an offset. By default, the offset value is 0 (e.g.
start the results at the beginning).

###<span id="measuresid">/measures/&lt;id&gt;</span>
Return the Measure object for the specified id.

Examples:

1. Measure 1:<br/>
http://www.ballotapi.com/api/measures/1

###<span id="measures">/measures</span>
Return a list of measures. Can be filtered by id, election, election date,
location, or precinct.

####?ids=&lt;id&gt;[,&lt;id&gt;,...]
Return measures filtered to only these comma separated ids. This is just the
plural form of the `/measures/<id>` endpoint.

Examples:

1. Measures 1 and 2:<br/>
http://www.ballotapi.com/api/measures?ids=1,2

####?elections=&lt;id&gt;[,&lt;id&gt;,...]
Return only measures that are part of these elections. Multiple elections can
be listed as comma separated ids, which will return measures that contain any
of the listed elections (i.e. treated as OR).

Examples:

1. The measures that are in Election 1:<br/>
http://www.ballotapi.com/api/measures?elections=1

2. The measures that contain Election 1 or 2 for 100 Market St, San Francisco, CA:<br/>
http://www.ballotapi.com/api/measures?elections=1,2&coords=37.7942635,-122.3955861

####?election_dates=&lt;start_date&gt;[:&lt;end_date&gt;[,...]]
Return only measures that belong to elections within a certain date range. You
can omit either the start or end dates to leave that side open ended. Dates are
inclusive, so results include elections that happen on the start or end dates.
You can also specify a single date, which is the equivalent to specifying that
date as both the start and end date. You can also have multiple date ranges,
separated by commas.

Examples:

1. All the measures for elections in 2014:<br/>
http://www.ballotapi.com/api/measures?election_dates=2014-01-01:2014-12-31

2. All the measures for elections after Nov 4th, 2014 for 100 Market St, San Francisco, CA:<br/>
http://www.ballotapi.com/api/measures?election_dates=2014-11-05:2050-11-05&coords=37.7942635,-122.3955861

####?coords=&lt;latitude&gt;,&lt;longitude&gt;
Return only measures that have a precinct encompassing this location.

Examples:

1. The Election 1 measures for 100 Market St, San Francisco, CA:<br/>
http://www.ballotapi.com/api/measures?elections=1&coords=37.7942635,-122.3955861

####?precincts=&lt;id&gt;[,&lt;id&gt;,...]
Return only measures that are a part of these precincts. Multiple precincts can
be listed as comma separated ids, which will return measures that are a part of
any of the listed precincts (i.e. treated as OR). Multiple precincts parameters
will intersect the measures returned by each precincts parameter (i.e. treated
as AND).

Examples:

1. The measures that contain Precinct 1:<br/>
http://www.ballotapi.com/api/measures?precincts=1

2. The measures that are a part of Precinct 1 or 2, and a part of Precinct 3:<br/>
http://www.ballotapi.com/api/measures?precincts=1,2&precincts=3

####?limit=&lt;int&gt;
Limit results to a set number. By default, the limit value for measures is 100.

####?offset=&lt;int&gt;
Start the list of results at an offset. By default, the offset value is 0 (e.g.
start the results at the beginning).

##<span id="how-to-self-host">How to self-host</span>
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

##<span id="license">License</span>
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


##<span id="contributions">Contributions</span>
This project is hosted https://github.com/sfbrigade/ballotapi and maintained by
a team at Code for America. Want to contribute? Submit an issue or pull request!
